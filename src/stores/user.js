import { defineStore } from 'pinia'

const STORAGE_KEY_COLLECTIONS = 'bgaide_collections'
const STORAGE_KEY_HISTORY = 'bgaide_history'
const MAX_HISTORY = 20

export const useUserStore = defineStore('user', {
    state: () => ({
        collections: [],    // 收藏的游戏 ID 数组
        recentViews: []     // 最近浏览 { id, name, thumb, time }
    }),

    getters: {
        isCollected: (state) => (gameId) => {
            return state.collections.includes(gameId)
        }
    },

    actions: {
        // 初始化：从本地缓存恢复
        init() {
            try {
                const c = uni.getStorageSync(STORAGE_KEY_COLLECTIONS)
                if (c) this.collections = JSON.parse(c)
                const h = uni.getStorageSync(STORAGE_KEY_HISTORY)
                if (h) this.recentViews = JSON.parse(h)
            } catch (e) {
                console.warn('UserStore init error:', e)
            }
        },

        // 切换收藏
        toggleCollection(gameId) {
            const idx = this.collections.indexOf(gameId)
            if (idx > -1) {
                this.collections.splice(idx, 1)
            } else {
                this.collections.push(gameId)
            }
            this._saveCollections()
        },

        // 记录浏览
        addHistory(game) {
            // 去重：移除已存在的记录
            this.recentViews = this.recentViews.filter(v => v.id !== game.id)
            // 插入到最前
            this.recentViews.unshift({
                id: game.id,
                name: game.name,
                thumb: game.thumb,
                time: Date.now()
            })
            // 限制条数
            if (this.recentViews.length > MAX_HISTORY) {
                this.recentViews = this.recentViews.slice(0, MAX_HISTORY)
            }
            this._saveHistory()
        },

        _saveCollections() {
            uni.setStorageSync(STORAGE_KEY_COLLECTIONS, JSON.stringify(this.collections))
        },

        _saveHistory() {
            uni.setStorageSync(STORAGE_KEY_HISTORY, JSON.stringify(this.recentViews))
        }
    }
})
