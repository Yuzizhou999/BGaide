import { defineStore } from 'pinia'
import { get, post } from '@/utils/api'

const STORAGE_KEY_COLLECTIONS = 'bgaide_collections'
const STORAGE_KEY_VISITOR_ID = 'bgaide_visitor_id'
const STORAGE_KEY_COLLECTION_OPS = 'bgaide_collection_ops'

function createVisitorId() {
    return `v_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`
}

function safeParseArray(raw) {
    if (!raw) return []
    try {
        const parsed = JSON.parse(raw)
        return Array.isArray(parsed) ? parsed : []
    } catch {
        return []
    }
}

export const useUserStore = defineStore('user', {
    state: () => ({
        collections: [],    // 收藏的游戏 ID 数组
        visitorId: '',
        pendingCollectionOps: [],
        syncingCollections: false
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
                this.collections = safeParseArray(uni.getStorageSync(STORAGE_KEY_COLLECTIONS))

                const cachedVisitorId = uni.getStorageSync(STORAGE_KEY_VISITOR_ID)
                if (cachedVisitorId) {
                    this.visitorId = String(cachedVisitorId)
                } else {
                    this.visitorId = createVisitorId()
                    uni.setStorageSync(STORAGE_KEY_VISITOR_ID, this.visitorId)
                }

                this.pendingCollectionOps = safeParseArray(
                    uni.getStorageSync(STORAGE_KEY_COLLECTION_OPS)
                )
            } catch (e) {
                console.warn('UserStore init error:', e)
            }

            // 恢复后尝试与服务端同步
            this.syncCollectionsFromServer()
            this.flushCollectionOps()
        },

        // 切换收藏
        toggleCollection(gameId) {
            if (!gameId) return
            const idx = this.collections.indexOf(gameId)
            let collected = false
            if (idx > -1) {
                this.collections.splice(idx, 1)
                collected = false
            } else {
                this.collections.push(gameId)
                collected = true
            }
            this._saveCollections()

            this.pendingCollectionOps.push({
                gameId,
                collected,
                time: Date.now()
            })
            this._saveCollectionOps()
            this.flushCollectionOps()
        },

        _saveCollections() {
            uni.setStorageSync(STORAGE_KEY_COLLECTIONS, JSON.stringify(this.collections))
        },

        _saveCollectionOps() {
            uni.setStorageSync(STORAGE_KEY_COLLECTION_OPS, JSON.stringify(this.pendingCollectionOps))
        },

        async syncCollectionsFromServer() {
            if (!this.visitorId) return
            try {
                const res = await get('/api/user/collections', { visitorId: this.visitorId })
                const serverSet = new Set(Array.isArray(res.gameIds) ? res.gameIds : [])

                // 本地未同步操作优先，避免拉取覆盖用户刚点击的收藏状态
                for (const op of this.pendingCollectionOps) {
                    if (!op || !op.gameId) continue
                    if (op.collected) serverSet.add(op.gameId)
                    else serverSet.delete(op.gameId)
                }

                this.collections = Array.from(serverSet)
                this._saveCollections()
            } catch (e) {
                console.warn('syncCollectionsFromServer error:', e)
            }
        },

        async flushCollectionOps() {
            if (this.syncingCollections || !this.visitorId || !this.pendingCollectionOps.length) return

            this.syncingCollections = true
            const nextOps = []
            for (const op of this.pendingCollectionOps) {
                if (!op || !op.gameId) continue
                try {
                    await post('/api/user/collections', {
                        visitorId: this.visitorId,
                        gameId: op.gameId,
                        collected: !!op.collected
                    })
                } catch (e) {
                    nextOps.push(op)
                }
            }

            this.pendingCollectionOps = nextOps
            this._saveCollectionOps()
            this.syncingCollections = false
        }
    }
})
