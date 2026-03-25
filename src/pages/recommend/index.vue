<template>
  <view class="page-container recommend-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>
    <view class="bg-orb orb-c"></view>
    <view class="star-layer star-layer-a"></view>
    <view class="star-layer star-layer-b"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <text class="nav-title">星轨宇宙</text>
      </view>
    </view>

    <scroll-view class="recommend-body" scroll-y :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <!-- Hero / Logo Section -->
      <view class="hero-section">
        <view class="hero-banner">
          <image
            v-if="!logoError"
            class="hero-logo"
            src="/static/icons/star-orbit-logo.png"
            mode="aspectFill"
            @error="onLogoError"
          />
          <view v-else class="hero-logo-fallback">
            <text class="fallback-title">星轨宇宙</text>
            <text class="fallback-subtitle">STAR ORBIT BOARD GAME</text>
          </view>
          <view class="hero-overlay">
            <text class="hero-title">星轨桌游</text>
            <text class="hero-desc">穿梭星轨，漫游桌游浩瀚宇宙。</text>
          </view>
        </view>
      </view>

      <!-- Carousel Section (Top 3) -->
      <view class="carousel-section" v-if="topGames.length > 0">
        <swiper
          class="recommend-swiper"
          circular
          autoplay
          :interval="4000"
          :duration="500"
          indicator-dots
          indicator-active-color="#ffb142"
          indicator-color="rgba(0,0,0,0.2)"
        >
          <swiper-item
            v-for="game in topGames"
            :key="game.id"
            @tap="goDetail(game.id)"
          >
            <view class="swiper-content">
              <image class="swiper-image" :src="game.thumb || '/static/icons/placeholder.svg'" mode="aspectFill" />
              <view class="swiper-overlay">
                <text class="swiper-name">{{ game.name }}</text>
                <view class="swiper-meta">
                  <text>👥 {{ formatPlayers(game) }}</text>
                  <text>⏱ {{ formatDuration(game) }}</text>
                </view>
              </view>
            </view>
          </swiper-item>
        </swiper>
      </view>

      <!-- Hot List Section -->
      <view class="list-section">
        <view class="section-head">
          <view class="head-left">
            <text class="section-emoji">🔥</text>
            <text class="section-title">派对热门榜单</text>
          </view>
          <view class="explore-btn" @tap="goExplore">
            全部桌游 <text class="arrow">></text>
          </view>
        </view>

        <view class="featured-grid">
          <view
            v-for="game in listGames"
            :key="game.id"
            class="featured-card"
            @tap="goDetail(game.id)"
          >
            <image class="featured-cover" :src="game.thumb || '/static/icons/placeholder.svg'" mode="aspectFill" lazy-load />
            <view class="featured-info">
              <text class="featured-name">{{ game.name }}</text>
              <view class="featured-tags">
                <text class="tag-item">👥 {{ formatPlayers(game) }}</text>
                <text class="tag-item">⏱ {{ formatDuration(game) }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- Bottom padding for tabbar -->
      <view class="safe-bottom"></view>
    </scroll-view>

    <CustomTabBar :current="0" />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { get } from '@/utils/api'
import { applyTheme, getTheme } from '@/utils/theme'
import CustomTabBar from '@/components/CustomTabBar.vue'

const statusBarHeight = ref(44)
const logoError = ref(false)
const sourceGames = ref([])
const managedRecommendIds = ref([])

onMounted(() => {
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44
  applyTheme(getTheme())
  fetchRecommendPageData()
})

onShow(() => {
  uni.hideTabBar({ animation: false })
})

// 分离前三大作和后续列表
const partyGames = computed(() => {
  const games = sourceGames.value || []

  if (managedRecommendIds.value.length) {
    const idOrder = managedRecommendIds.value.map((id) => String(id))
    const idSet = new Set(idOrder)
    const manualGames = games
      .filter((g) => idSet.has(String(g.id)))
      .sort((a, b) => idOrder.indexOf(String(a.id)) - idOrder.indexOf(String(b.id)))

    const remain = games.filter((g) => !idSet.has(String(g.id)))
    return [...manualGames, ...remain]
  }

  return games
    .filter((g) => g.gameType === '毛线聚会' || g.recommended || g.hot)
    .sort((a, b) => Number(b.bggScore || 0) - Number(a.bggScore || 0))
})

const topGames = computed(() => {
  return partyGames.value.slice(0, 3)
})

const listGames = computed(() => {
  const firstBatch = partyGames.value.slice(3, 9)
  if (firstBatch.length >= 4) return firstBatch
  
  // 如果聚会游戏不够，用其他游戏补齐
  const remain = (sourceGames.value || []).filter(
    (g) => !partyGames.value.some((p) => p.id === g.id)
  )
  return [...firstBatch, ...remain].slice(0, 6)
})

async function fetchRecommendPageData() {
  await fetchAllGames()
  await fetchManagedRecommendIds()
}

async function fetchAllGames() {
  const pageSize = 100
  let page = 1
  let total = 0
  const result = []

  try {
    do {
      const res = await get('/api/games', { page, pageSize })
      const list = Array.isArray(res?.data) ? res.data : []
      total = Number(res?.total || 0)
      result.push(...list)
      page += 1
      if (!list.length) break
    } while (result.length < total)

    sourceGames.value = result
  } catch (error) {
    console.error('fetchAllGames error:', error)
    sourceGames.value = []
  }
}

async function fetchManagedRecommendIds() {
  try {
    const res = await get('/api/games/recommendations')
    managedRecommendIds.value = Array.isArray(res?.gameIds)
      ? res.gameIds.map((id) => String(id))
      : []
  } catch (error) {
    // 接口未配置时自动回退到原有推荐策略
    managedRecommendIds.value = []
  }
}

function onLogoError() {
  logoError.value = true
}

function formatPlayers(game) {
  if (!game) return '-'
  if (Array.isArray(game.players) && game.players.length >= 2) {
    return `${game.players[0]}-${game.players[1]}人`
  }
  if (typeof game.players === 'string' || typeof game.players === 'number') {
    return String(game.players)
  }
  return '-'
}

function formatDuration(game) {
  if (!game) return '-'
  if (Array.isArray(game.duration) && game.duration.length >= 2) {
    return `${game.duration[0]}-${game.duration[1]}分钟`
  }
  if (typeof game.duration === 'string' || typeof game.duration === 'number') {
    return String(game.duration)
  }
  return '-'
}

function goDetail(id) {
  uni.navigateTo({ url: `/pages/game-detail/index?id=${id}` })
}

function goExplore() {
  uni.switchTab({ url: '/pages/home/index' })
}
</script>

<style lang="scss" scoped>
.recommend-page {
  position: relative;
  overflow: hidden;
  height: 100vh;
  background: radial-gradient(circle at 20% 10%, #1a2238 0%, #10141f 45%, #090b12 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80rpx);
  pointer-events: none;
  opacity: 0.6;
}

.star-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.star-layer-a {
  background-image:
    radial-gradient(3rpx 3rpx at 8% 18%, rgba(255, 255, 255, 0.8), transparent),
    radial-gradient(2rpx 2rpx at 28% 62%, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(2rpx 2rpx at 50% 30%, rgba(171, 218, 255, 0.75), transparent),
    radial-gradient(3rpx 3rpx at 74% 45%, rgba(255, 255, 255, 0.65), transparent),
    radial-gradient(2rpx 2rpx at 88% 76%, rgba(171, 218, 255, 0.7), transparent);
  opacity: 0.6;
  animation: twinkleSlow 6s ease-in-out infinite;
}

.star-layer-b {
  background-image:
    radial-gradient(2rpx 2rpx at 14% 80%, rgba(255, 255, 255, 0.75), transparent),
    radial-gradient(3rpx 3rpx at 34% 16%, rgba(171, 218, 255, 0.8), transparent),
    radial-gradient(2rpx 2rpx at 61% 68%, rgba(255, 255, 255, 0.7), transparent),
    radial-gradient(2rpx 2rpx at 81% 24%, rgba(171, 218, 255, 0.75), transparent),
    radial-gradient(3rpx 3rpx at 93% 54%, rgba(255, 255, 255, 0.65), transparent);
  opacity: 0.4;
  animation: twinkleFast 4.2s ease-in-out infinite;
}

.orb-a {
  width: 500rpx;
  height: 500rpx;
  top: -100rpx;
  left: -150rpx;
  background: radial-gradient(circle, rgba(162, 210, 255, 0.15), transparent);
}

.orb-b {
  width: 600rpx;
  height: 600rpx;
  right: -200rpx;
  top: 20%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05), transparent);
}

.orb-c {
  width: 400rpx;
  height: 400rpx;
  bottom: 10%;
  left: 10%;
  background: radial-gradient(circle, rgba(162, 210, 255, 0.1), transparent);
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(15, 16, 19, 0.8);
  backdrop-filter: blur(20px);
}

.nav-content {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 32rpx;
}

.nav-title {
  font-size: 34rpx;
  font-weight: 800;
  color: #fff;
  letter-spacing: 2rpx;
}

.recommend-body {
  height: 100vh;
  box-sizing: border-box;
}

.hero-section {
  padding: 24rpx 32rpx 8rpx;
  animation: fadeInDown 0.8s ease-out;
}

.hero-banner {
  position: relative;
  width: 100%;
  height: 430rpx;
  border-radius: 30rpx;
  overflow: hidden;
  box-shadow: 0 28rpx 68rpx rgba(0, 0, 0, 0.5), 0 0 56rpx rgba(145, 203, 255, 0.18);
}

.hero-logo {
  width: 100%;
  height: 100%;
  background: #151923;
  transform: scale(1.01);
}

.hero-logo-fallback {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #2d3436, #1a1c23);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
  .fallback-title {
    color: #fff;
    font-size: 56rpx;
    font-weight: 900;
    letter-spacing: 4rpx;
  }
  
  .fallback-subtitle {
    color: rgba(255,255,255,0.5);
    font-size: 20rpx;
    margin-top: 10rpx;
    letter-spacing: 2rpx;
  }
}

.hero-overlay {
  position: absolute;
  inset: auto 0 0 0;
  padding: 56rpx 28rpx 26rpx;
  background: linear-gradient(to top, rgba(7, 9, 15, 0.92) 0%, rgba(7, 9, 15, 0) 100%);
}

.hero-title {
  display: block;
  font-size: 44rpx;
  font-weight: 900;
  background: linear-gradient(to right, #ffffff, #c9e9ff);
  -webkit-background-clip: text;
  color: transparent;
}

.hero-desc {
  display: block;
  font-size: 24rpx;
  color: rgba(255,255,255,0.78);
  margin-top: 8rpx;
  letter-spacing: 1rpx;
}

.carousel-section {
  margin: 30rpx 32rpx;
  border-radius: 32rpx;
  overflow: hidden;
  box-shadow: 0 20rpx 40rpx rgba(0,0,0,0.3);
  transform: translateZ(0); /* Safari border-radius fix */
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.recommend-swiper {
  height: 420rpx;
  border-radius: 32rpx;
  background: #1a1c23;
}

.swiper-content {
  position: relative;
  width: 100%;
  height: 100%;
}

.swiper-image {
  width: 100%;
  height: 100%;
}

.swiper-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 60rpx 30rpx 40rpx;
  background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
  display: flex;
  flex-direction: column;
}

.swiper-name {
  color: #fff;
  font-size: 38rpx;
  font-weight: 900;
  text-shadow: 0 4rpx 8rpx rgba(0,0,0,0.5);
}

.swiper-meta {
  display: flex;
  gap: 20rpx;
  margin-top: 12rpx;
  color: rgba(255,255,255,0.8);
  font-size: 24rpx;
}

.list-section {
  padding: 0 32rpx 40rpx;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24rpx;
}

.head-left {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.section-emoji {
  font-size: 34rpx;
}

.section-title {
  font-size: 34rpx;
  font-weight: 800;
  color: #fff;
}

.explore-btn {
  font-size: 24rpx;
  color: rgba(255,255,255,0.6);
  display: flex;
  align-items: center;
  padding: 10rpx 0;
  
  .arrow {
    margin-left: 6rpx;
    font-size: 20rpx;
  }
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
}

.featured-card {
  position: relative;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24rpx;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.featured-cover {
  width: 100%;
  height: 220rpx;
  background: #1a1c23;
}

.featured-info {
  padding: 20rpx;
}

.featured-name {
  font-size: 28rpx;
  font-weight: 800;
  color: #fff;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  height: 78rpx;
}

.featured-tags {
  display: flex;
  justify-content: space-between;
  margin-top: 16rpx;
}

.tag-item {
  font-size: 22rpx;
  color: rgba(255,255,255,0.6);
  background: rgba(255,255,255,0.05);
  padding: 4rpx 12rpx;
  border-radius: 8rpx;
}

.safe-bottom {
  height: 180rpx;
}

/* 推荐页专属 TabBar：覆盖全局浅色风格，和星空背景统一 */
:deep(.custom-tabbar) {
  background: linear-gradient(180deg, rgba(10, 14, 24, 0.7) 0%, rgba(8, 12, 20, 0.92) 100%) !important;
  border-top: 1rpx solid rgba(160, 206, 255, 0.24);
  box-shadow: 0 -8rpx 30rpx rgba(0, 0, 0, 0.45);
}

:deep(.custom-tabbar .tab-label) {
  color: rgba(219, 235, 255, 0.62);
}

:deep(.custom-tabbar .tab-label.active) {
  color: #d9efff;
}

:deep(.custom-tabbar .tab-icon-wrap.active) {
  background: rgba(153, 211, 255, 0.22);
  box-shadow: 0 0 20rpx rgba(153, 211, 255, 0.35);
}

:deep(.custom-tabbar .tab-indicator) {
  background: #a9d8ff;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-30rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes twinkleSlow {
  0%, 100% { opacity: 0.42; }
  50% { opacity: 0.72; }
}

@keyframes twinkleFast {
  0%, 100% { opacity: 0.26; }
  50% { opacity: 0.56; }
}
</style>
