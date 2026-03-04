import { defineStore } from 'pinia'
import { get } from '@/utils/api'

export const useGameStore = defineStore('game', {
    state: () => ({
        // 游戏列表数据（从后端获取）
        allGames: [],
        loading: false,
        error: null,

        // 搜索 & 筛选（本地状态，用于构建请求参数）
        keyword: '',
        filters: {
            playerCount: null,
            duration: null,       // [min, max]
            difficulty: null
        },

        // 分页
        total: 0,
        page: 1,
        pageSize: 50,

        // 单个游戏缓存
        _gameCache: {},    // { id: gameData }
        _rulesCache: {},   // { id: rulesData }
        _faqCache: {}      // { id: faqData }
    }),

    getters: {
        // 搜索 + 筛选后的游戏列表（直接使用后端返回的数据）
        filteredGames(state) {
            return state.allGames
        },

        hotGames(state) {
            return state.allGames.filter(g => g.hot)
        },

        recommendedGames(state) {
            return state.allGames.filter(g => g.recommended)
        },

        // 获取缓存的游戏详情
        getGameById: (state) => (id) => {
            return state._gameCache[id] || state.allGames.find(g => g.id === id) || null
        },

        // 获取缓存的规则
        getRulesById: (state) => (id) => {
            return state._rulesCache[id] || null
        },

        // 获取缓存的 FAQ
        getFaqsById: (state) => (id) => {
            return state._faqCache[id] || []
        }
    },

    actions: {
        /**
         * 从后端获取游戏列表（带搜索/筛选）
         */
        async fetchGames() {
            this.loading = true
            this.error = null
            try {
                const params = {
                    keyword: this.keyword || null,
                    playerCount: this.filters.playerCount,
                    difficulty: this.filters.difficulty,
                    page: this.page,
                    pageSize: this.pageSize
                }
                // 时长筛选
                if (this.filters.duration) {
                    params.durationMin = this.filters.duration[0]
                    params.durationMax = this.filters.duration[1]
                }

                const res = await get('/api/games', params)
                this.allGames = res.data
                this.total = res.total
            } catch (e) {
                this.error = e.message
                console.error('fetchGames error:', e)
            } finally {
                this.loading = false
            }
        },

        /**
         * 获取单个游戏详情
         */
        async fetchGameDetail(id) {
            if (this._gameCache[id]) return this._gameCache[id]
            try {
                const data = await get(`/api/games/${id}`)
                this._gameCache[id] = data
                return data
            } catch (e) {
                console.error('fetchGameDetail error:', e)
                return null
            }
        },

        /**
         * 获取游戏规则
         */
        async fetchRules(id) {
            if (this._rulesCache[id]) return this._rulesCache[id]
            try {
                const data = await get(`/api/games/${id}/rules`)
                this._rulesCache[id] = data
                return data
            } catch (e) {
                console.error('fetchRules error:', e)
                return null
            }
        },

        /**
         * 获取游戏 FAQ
         */
        async fetchFaq(id) {
            if (this._faqCache[id]) return this._faqCache[id]
            try {
                const data = await get(`/api/games/${id}/faq`)
                this._faqCache[id] = data
                return data
            } catch (e) {
                console.error('fetchFaq error:', e)
                return []
            }
        },

        setKeyword(kw) {
            this.keyword = kw
            this.page = 1
            this.fetchGames()
        },

        setFilter(key, value) {
            this.filters[key] = value
            this.page = 1
            this.fetchGames()
        },

        clearFilters() {
            this.keyword = ''
            this.filters = { playerCount: null, duration: null, difficulty: null }
            this.page = 1
            this.fetchGames()
        }
    }
})
