import { defineStore } from 'pinia'

const STORAGE_KEY_SCORER = 'bgaide_scorer'
const STORAGE_KEY_ADV_SCORER = 'bgaide_adv_scorer'
const STORAGE_KEY_TIMER = 'bgaide_timer'

export const useToolsStore = defineStore('tools', {
    state: () => ({
        // 万能计分板
        scorer: {
            players: []   // { name: string, score: number }
        },

        // 高级计分器（七大奇迹模板）
        advancedScorer: {
            players: []
            // 每位: { name, military, coin, wonder, civic, commercial, science, guild, total }
        },

        // 计时器
        timer: {
            mode: 'countdown',  // 'countdown' | 'stopwatch'
            targetSeconds: 60,
            elapsedSeconds: 0,
            isRunning: false,
            lastTickTime: null   // 用于切出/切回补偿
        }
    }),

    actions: {
        // === 初始化 ===
        init() {
            try {
                const s = uni.getStorageSync(STORAGE_KEY_SCORER)
                if (s) this.scorer = JSON.parse(s)
                const a = uni.getStorageSync(STORAGE_KEY_ADV_SCORER)
                if (a) this.advancedScorer = JSON.parse(a)
                const t = uni.getStorageSync(STORAGE_KEY_TIMER)
                if (t) {
                    const saved = JSON.parse(t)
                    this.timer = { ...this.timer, ...saved }
                    // 如果切出前在运行，补偿时间差
                    if (this.timer.isRunning && this.timer.lastTickTime) {
                        const diff = Math.floor((Date.now() - this.timer.lastTickTime) / 1000)
                        this.timer.elapsedSeconds += diff
                    }
                }
            } catch (e) {
                console.warn('ToolsStore init error:', e)
            }
        },

        // === 万能计分板 ===
        addPlayer(name) {
            this.scorer.players.push({ name, score: 0 })
            this._saveScorer()
        },

        removePlayer(index) {
            this.scorer.players.splice(index, 1)
            this._saveScorer()
        },

        updateScore(index, delta) {
            this.scorer.players[index].score += delta
            this._saveScorer()
        },

        resetScorer() {
            this.scorer.players = []
            this._saveScorer()
        },

        // === 高级计分器 ===
        addAdvPlayer(name) {
            this.advancedScorer.players.push({
                name,
                military: 0, coin: 0, wonder: 0,
                civic: 0, commercial: 0, science: 0, guild: 0,
                total: 0
            })
            this._saveAdvScorer()
        },

        removeAdvPlayer(index) {
            this.advancedScorer.players.splice(index, 1)
            this._saveAdvScorer()
        },

        updateAdvScore(playerIndex, field, value) {
            const p = this.advancedScorer.players[playerIndex]
            p[field] = Number(value) || 0
            p.total = p.military + p.coin + p.wonder + p.civic + p.commercial + p.science + p.guild
            this._saveAdvScorer()
        },

        resetAdvScorer() {
            this.advancedScorer.players = []
            this._saveAdvScorer()
        },

        // === 计时器 ===
        setTimerMode(mode) {
            this.timer.mode = mode
            this.timer.elapsedSeconds = 0
            this.timer.isRunning = false
            this._saveTimer()
        },

        setTargetSeconds(s) {
            this.timer.targetSeconds = s
            this._saveTimer()
        },

        tickTimer() {
            this.timer.elapsedSeconds++
            this.timer.lastTickTime = Date.now()
            this._saveTimer()
        },

        startTimer() {
            this.timer.isRunning = true
            this.timer.lastTickTime = Date.now()
            this._saveTimer()
        },

        pauseTimer() {
            this.timer.isRunning = false
            this._saveTimer()
        },

        resetTimer() {
            this.timer.elapsedSeconds = 0
            this.timer.isRunning = false
            this.timer.lastTickTime = null
            this._saveTimer()
        },

        // === 持久化 ===
        _saveScorer() {
            uni.setStorageSync(STORAGE_KEY_SCORER, JSON.stringify(this.scorer))
        },
        _saveAdvScorer() {
            uni.setStorageSync(STORAGE_KEY_ADV_SCORER, JSON.stringify(this.advancedScorer))
        },
        _saveTimer() {
            uni.setStorageSync(STORAGE_KEY_TIMER, JSON.stringify(this.timer))
        }
    }
})
