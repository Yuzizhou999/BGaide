import { defineStore } from 'pinia'

const STORAGE_KEY_SCORER = 'bgaide_scorer'
const STORAGE_KEY_ADV_SCORER = 'bgaide_adv_scorer'
const STORAGE_KEY_TIMER = 'bgaide_timer'
const STORAGE_KEY_PUNISHMENT = 'bgaide_punishment'

const PRESET_PUNISHMENTS = [
    { id: 'p1', text: '请用播音主持的语气说一句：“接下来局势由我掌控。”', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p2', text: '给自己起一个中二称号，并保持一轮。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p3', text: '模仿一种小动物 5 秒。', level: 'light', socialFriendly: false, needAction: true, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p4', text: '用夸张语气介绍一下自己，像在参加选秀。', level: 'light', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p5', text: '随机夸一位玩家一句，但要夸得像广告词。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p6', text: '接下来 1 分钟，说话不能带“我”字。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p7', text: '请做一个“我很震惊”的表情并保持 5 秒。', level: 'light', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p8', text: '用客服语气回答下一位玩家的一个问题。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p9', text: '请用电影预告片旁白介绍当前牌局。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p10', text: '随机说出 3 个词，并用它们造一个离谱句子。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p11', text: '接下来一轮，你的每句话前面都要加“根据我的观察”。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p12', text: '对空气鞠躬，并说“感谢大家的支持”。', level: 'light', socialFriendly: true, needAction: true, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p13', text: '模仿一个你想象中的反派笑声。', level: 'light', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p14', text: '用古风语气说一句最普通的话，比如“把牌给我看看”。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p15', text: '请把自己的心情用天气预报方式播报出来。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p16', text: '给左手和右手各取一个名字，并用它们打招呼。', level: 'light', socialFriendly: true, needAction: true, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p17', text: '用 3 个表情的感觉表演你现在的状态。', level: 'light', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },
    { id: 'p18', text: '请用体育解说语气描述刚刚发生的一件小事。', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p19', text: '学机器人说一句：“系统判断你们都很可疑。”', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p20', text: '随机点一位玩家，认真地说：“我一直很看好你。”', level: 'light', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '破冰', canSkip: true, source: 'preset' },

    { id: 'p21', text: '站起来走一圈“胜利者步伐”。', level: 'medium', socialFriendly: false, needAction: true, needSpeech: false, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p22', text: '用慢动作完成一次坐下或起立。', level: 'medium', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p23', text: '模仿偶像登场，给自己设计一句出场台词。', level: 'medium', socialFriendly: false, needAction: true, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p24', text: '假装自己是 NPC，说一句发布任务的话。', level: 'medium', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p25', text: '表演“抽到好牌但故作冷静”的样子 5 秒。', level: 'medium', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p26', text: '给本局所有玩家各起一个绰号。', level: 'medium', socialFriendly: false, needAction: false, needSpeech: true, players: '4-8', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p27', text: '请即兴演一段“我明明很强却不得不低调”。', level: 'medium', socialFriendly: false, needAction: true, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p28', text: '随机选一个物品，把它介绍成传说级装备。', level: 'medium', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p29', text: '请用新闻联播语气播报自己刚才的失误。', level: 'medium', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p30', text: '下一次轮到你时，先摆一个造型再行动。', level: 'medium', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p31', text: '模仿一位老师点名时的语气，念一位玩家名字。', level: 'medium', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p32', text: '现场表演一个“糟了但不能慌”的表情包动作。', level: 'medium', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p33', text: '请给自己配一段 5 秒钟的动画片反派台词。', level: 'medium', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p34', text: '随机选择一位玩家，对他进行 10 秒“过度正式”的赞美。', level: 'medium', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '熟人局', canSkip: true, source: 'preset' },
    { id: 'p35', text: '假装自己是侦探，分析一下谁最可疑，要求非常认真。', level: 'medium', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },

    { id: 'p36', text: '接下来一轮，你发言前都要先说：“经过我严密的推理……”。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p37', text: '下一回合开始前，请把双手交叉放好 10 秒。', level: 'tabletop', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p38', text: '本轮你称呼所有玩家都要加上“尊敬的”。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p39', text: '下一次行动前，必须先喊一句属于自己的口号。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p40', text: '本轮结束前，你不能主动解释自己。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p41', text: '接下来一轮，你只能用不超过 6 个字来发言。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p42', text: '下一轮中，你每次发言都要像在法庭辩论。', level: 'tabletop', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p43', text: '本轮请保持“神秘高人”人设，说话越玄越好。', level: 'tabletop', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p44', text: '下一次轮到你时，先点评一句牌局形势再操作。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p45', text: '接下来一轮，你要把自己当成最终 Boss 来说话。', level: 'tabletop', socialFriendly: false, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p46', text: '本轮发言时，必须用“我有一个大胆的想法”开头。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p47', text: '下一次被别人质疑时，你只能微笑，不能立刻反驳。', level: 'tabletop', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p48', text: '本轮你获得称号“局势搅拌机”，并要主动认领这个称号。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '欢乐局', canSkip: true, source: 'preset' },
    { id: 'p49', text: '下一次操作前，请先给自己的行动起一个技能名。', level: 'tabletop', socialFriendly: true, needAction: false, needSpeech: true, players: 'all', scene: '推理局', canSkip: true, source: 'preset' },
    { id: 'p50', text: '在下一轮结束前，你要一直保持“我已经看穿一切”的表情。', level: 'tabletop', socialFriendly: true, needAction: true, needSpeech: false, players: 'all', scene: '推理局', canSkip: true, source: 'preset' }
]

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
        },

        // 趣味惩罚
        punishment: {
            level: 'all',
            socialFriendlyOnly: false,
            scene: 'all',
            customItems: [],
            history: []
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

                const p = uni.getStorageSync(STORAGE_KEY_PUNISHMENT)
                if (p) {
                    const saved = JSON.parse(p)
                    this.punishment = { ...this.punishment, ...saved }
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

        // === 趣味惩罚 ===
        setPunishmentLevel(level) {
            this.punishment.level = level
            this._savePunishment()
        },

        setPunishmentSocialFriendlyOnly(enabled) {
            this.punishment.socialFriendlyOnly = !!enabled
            this._savePunishment()
        },

        setPunishmentScene(scene) {
            this.punishment.scene = scene || 'all'
            this._savePunishment()
        },

        addCustomPunishment(text, level = 'light') {
            const content = String(text || '').trim()
            if (!content) return false

            const item = {
                id: `c_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
                text: content,
                level,
                socialFriendly: true,
                needAction: false,
                needSpeech: true,
                players: 'all',
                scene: '欢乐局',
                canSkip: true,
                source: 'custom'
            }

            this.punishment.customItems.unshift(item)
            this._savePunishment()
            return true
        },

        removeCustomPunishment(id) {
            this.punishment.customItems = this.punishment.customItems.filter(x => x.id !== id)
            this._savePunishment()
        },

        _getPunishmentPool(options = {}) {
            const level = options.level || 'all'
            const socialFriendlyOnly = !!options.socialFriendlyOnly
            const scene = options.scene || 'all'
            const allItems = [...PRESET_PUNISHMENTS, ...this.punishment.customItems]
            return allItems.filter((x) => {
                if (level !== 'all' && x.level !== level) return false
                if (socialFriendlyOnly && !x.socialFriendly) return false
                if (scene !== 'all' && x.scene !== scene) return false
                return true
            })
        },

        drawPunishment(options = {}) {
            const pool = this._getPunishmentPool(options)
            if (!pool.length) return null

            const lastId = this.punishment.history[0]?.id
            const filtered = pool.length > 1 ? pool.filter(x => x.id !== lastId) : pool
            const picked = filtered[Math.floor(Math.random() * filtered.length)]

            this.punishment.history.unshift({
                id: picked.id,
                text: picked.text,
                level: picked.level,
                time: Date.now(),
                source: picked.source
            })
            this.punishment.history = this.punishment.history.slice(0, 30)
            this._savePunishment()
            return picked
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
        },
        _savePunishment() {
            uni.setStorageSync(STORAGE_KEY_PUNISHMENT, JSON.stringify(this.punishment))
        }
    }
})
