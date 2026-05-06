<template>
  <view class="page-container home-page">
    <!-- 自定义导航栏 -->
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-logo">
          <text class="logo-icon">🐰</text>
          <text class="logo-text">探索桌游宇宙</text>
        </view>
      </view>
    </view>

    <!-- 搜索栏 -->
    <view class="search-wrapper" :style="{ marginTop: (statusBarHeight + 44) + 'px' }">
      <view class="search-row">
        <view class="search-flex">
          <SearchBar v-model="keyword" @search="onSearch" />
        </view>
        <view class="filter-btn" @tap="showFilter = true">
          <text>⚙️</text>
        </view>
      </view>
    </view>

    <!-- 推荐横幅 -->
    <view v-if="!keyword" class="recommend-section">
      <text class="section-title">🔥 热门推荐</text>
      <intersection-observer @intersect="onHotGameIntersect">
        <scroll-view class="recommend-scroll" scroll-x enable-flex>
          <view v-for="game in hotGames" :key="game.id" class="recommend-card" @tap="goDetail(game.id)">
            <view class="recommend-cover">
              <image :src="game.thumb || '/static/icons/placeholder.svg'" mode="aspectFill" class="recommend-img" lazy-load />
            </view>
            <text class="recommend-name">{{ game.name }}</text>
            <view class="recommend-meta">
              <text>⭐ {{ game.bggScore }}</text>
            </view>
          </view>
        </scroll-view>
      </intersection-observer>
    </view>

    <!-- 游戏列表 -->
    <view class="games-section">
      <view class="section-header-row">
        <text class="section-title">{{ keyword ? '搜索结果' : '全部桌游' }}</text>
        <text class="game-count">{{ filteredGames.length }} 款</text>
      </view>
      <view class="games-grid">
        <GameCard v-for="game in filteredGames" :key="game.id" :game="game" />
      </view>
      <view v-if="filteredGames.length === 0" class="empty-state">
        <text class="empty-icon">🎯</text>
        <text class="empty-text">没有找到匹配的桌游</text>
        <text class="empty-hint">试试其他关键词或调整筛选条件</text>
      </view>
    </view>

    <!-- 筛选面板 -->
    <FilterPanel :visible="showFilter" @close="showFilter = false" @filter="onFilter" />

    <!-- 自定义 TabBar -->
    <CustomTabBar :current="1" />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onShow, onShareAppMessage, onShareTimeline } from '@dcloudio/uni-app'
import { useGameStore } from '@/stores/game'
import { useUserStore } from '@/stores/user'
import SearchBar from '@/components/SearchBar.vue'
import FilterPanel from '@/components/FilterPanel.vue'
import GameCard from '@/components/GameCard.vue'
import CustomTabBar from '@/components/CustomTabBar.vue'
import { applyTheme, getTheme } from '@/utils/theme'
import { enableWeChatOfficialShare, buildPageSharePayload, buildTimelineSharePayload, buildShareImages } from '@/utils/share'
import { getStatusBarHeight } from '@/utils/system'

const gameStore = useGameStore()
const userStore = useUserStore()

const keyword = ref('')
const showFilter = ref(false)
const statusBarHeight = ref(44)

// 获取状态栏高度 & 加载数据
onMounted(() => {
  statusBarHeight.value = getStatusBarHeight(44)
  userStore.init()
  applyTheme(getTheme())
  enableWeChatOfficialShare()
  // 从后端拉取游戏列表
  gameStore.fetchGames()
})

onShow(() => {
  uni.hideTabBar({ animation: false })
  userStore.syncCollectionsFromServer()
  userStore.flushCollectionOps()
})

const filteredGames = computed(() => gameStore.filteredGames)
const hotGames = computed(() => gameStore.hotGames)

function onSearch(kw) {
  gameStore.setKeyword(kw)
}

function onFilter(filters) {
  gameStore.applyFilters({
    playerCount: filters.playerCount,
    duration: filters.duration,
    difficulty: filters.difficulty,
    gameType: filters.gameType
  })
}

function goDetail(id) {
  uni.navigateTo({ url: `/pages/game-detail/index?id=${id}` })
}

function onHotGameIntersect(event) {
  // IntersectionObserver callback for native performance mode
}

onShareAppMessage(() => buildPageSharePayload({
  title: 'BGaide 桌游探索｜找规则、找推荐、找灵感',
  path: '/pages/home/index',
  imageUrl: buildShareImages('/static/icons/placeholder.svg')
}))

onShareTimeline(() => buildTimelineSharePayload({
  title: 'BGaide 桌游探索｜找规则、找推荐、找灵感',
  query: '',
  imageUrl: buildShareImages('/static/icons/placeholder.svg')
}))
</script>

<style lang="scss" scoped>
.home-page {
  padding-bottom: 120rpx;
}

/* 自定义导航栏 */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: var(--color-bg-secondary);
  backdrop-filter: blur(20px);
  border-bottom: 1rpx solid var(--color-divider);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 88rpx;
  padding: 0 32rpx;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.logo-icon {
  font-size: 40rpx;
}

.logo-text {
  font-size: 36rpx;
  font-weight: 800;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.filter-btn {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  background: var(--color-bg-card);
  border: 2rpx solid var(--color-border);
  font-size: 36rpx;
  flex-shrink: 0;

  &:active {
    opacity: 0.7;
  }
}

/* 搜索 */
.search-wrapper {
  padding: 24rpx 32rpx 16rpx;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.search-flex {
  flex: 1;
}

/* 推荐横幅 */
.recommend-section {
  padding: 16rpx 0 8rpx;

  .section-title {
    padding: 0 32rpx;
  }
}

.recommend-scroll {
  white-space: nowrap;
  padding: 16rpx 32rpx;
}

.recommend-card {
  display: inline-flex;
  flex-direction: column;
  width: 220rpx;
  margin-right: 20rpx;

  &:active {
    opacity: 0.8;
  }
}

.recommend-cover {
  width: 220rpx;
  height: 180rpx;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.recommend-img {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #a29bfe, #6c5ce7);
}

.recommend-name {
  font-size: 26rpx;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-top: 10rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recommend-meta {
  font-size: 22rpx;
  color: var(--color-accent);
  margin-top: 4rpx;
}

/* 游戏列表 */
.games-section {
  padding: 16rpx 32rpx;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.game-count {
  font-size: 26rpx;
  color: var(--color-text-tertiary);
}

.games-grid {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
}

.empty-icon {
  font-size: 80rpx;
  margin-bottom: 24rpx;
}

.empty-text {
  font-size: 30rpx;
  color: var(--color-text-secondary);
  font-weight: 600;
}

.empty-hint {
  font-size: 26rpx;
  color: var(--color-text-tertiary);
  margin-top: 8rpx;
}
</style>
