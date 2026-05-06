<template>
  <view class="page-container profile-page">
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <text class="nav-title">👤 我的</text>
      </view>
    </view>

    <view class="profile-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">

      <!-- 我的收藏 -->
      <view class="section">
        <view class="section-header-row">
          <text class="section-title">❤️ 我的收藏</text>
          <text class="section-count">{{ collectedGames.length }} 款</text>
        </view>
        <view v-if="collectedGames.length > 0" class="compact-list">
          <view v-for="game in collectedGames" :key="game.id" class="compact-item" @tap="goDetail(game.id)">
            <image class="compact-thumb" :src="game.thumb || '/static/icons/placeholder.svg'" mode="aspectFill" lazy-load />
            <view class="compact-info">
              <text class="compact-name">{{ game.name }}</text>
              <text class="compact-meta">{{ game.nameEn }} · ⭐{{ game.bggScore }}</text>
            </view>
            <text class="compact-arrow">›</text>
          </view>
        </view>
        <view v-else class="empty-mini">
          <text>暂无收藏，去探索页面收藏喜欢的桌游吧</text>
        </view>
      </view>

      <!-- 反馈入口 -->
      <view class="section">
        <text class="section-title">💬 反馈与建议</text>
        <view class="feedback-cards">
          <view class="feedback-card" @tap="openFeedback('correct')">
            <text class="fb-icon">📝</text>
            <text class="fb-name">规则指正</text>
            <text class="fb-hint">发现规则错误？告诉我们</text>
          </view>
          <view class="feedback-card" @tap="openFeedback('wish')">
            <text class="fb-icon">⭐</text>
            <text class="fb-name">心愿单</text>
            <text class="fb-hint">想看哪款桌游的规则</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 反馈弹窗 -->
    <view class="feedback-mask" v-if="showFeedback" @tap="showFeedback = false" />
    <view class="feedback-panel" :class="{ show: showFeedback }">
      <text class="feedback-title">
        {{ feedbackType === 'correct' ? '📝 规则指正' : '⭐ 心愿单求更' }}
      </text>
      <textarea class="feedback-textarea" v-model="feedbackContent"
        :placeholder="feedbackType === 'correct' ? '请描述规则错误的内容和正确裁决...' : '请输入你希望收录的桌游名称...'" maxlength="500" />
      <view class="feedback-submit" @tap="submitFeedback">
        <text>提交反馈</text>
      </view>
    </view>

    <!-- 自定义 TabBar -->
    <CustomTabBar :current="3" />
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onShow, onShareAppMessage, onShareTimeline } from '@dcloudio/uni-app'
import { useGameStore } from '@/stores/game'
import { useUserStore } from '@/stores/user'
import { applyTheme } from '@/utils/theme'
import { post } from '@/utils/api'
import CustomTabBar from '@/components/CustomTabBar.vue'
import { enableWeChatOfficialShare, buildPageSharePayload, buildTimelineSharePayload, buildShareImages } from '@/utils/share'
import { getStatusBarHeight } from '@/utils/system'

const gameStore = useGameStore()
const userStore = useUserStore()
const statusBarHeight = ref(44)
const showFeedback = ref(false)
const feedbackType = ref('correct')
const feedbackContent = ref('')
const FEEDBACK_STORAGE_KEY = 'bgaide_feedbacks'

function getLocalFeedbackQueue() {
  try {
    const raw = uni.getStorageSync(FEEDBACK_STORAGE_KEY) || '[]'
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

function setLocalFeedbackQueue(list) {
  uni.setStorageSync(FEEDBACK_STORAGE_KEY, JSON.stringify(list))
}

function shouldSyncFeedback(item) {
  if (!item || !item.type || !item.content) return false
  if (item.unsynced === true) return true
  // 兼容旧版本本地反馈（没有 unsynced 字段）
  return item.unsynced === undefined
}

function getNetworkType() {
  return new Promise((resolve) => {
    uni.getNetworkType({
      success: (res) => resolve(res.networkType),
      fail: () => resolve('unknown')
    })
  })
}

async function syncUnsyncedFeedbacks() {
  const queue = getLocalFeedbackQueue()
  if (!queue.length) return

  const networkType = await getNetworkType()
  if (networkType === 'none') return

  const nextQueue = []
  for (const item of queue) {
    if (!shouldSyncFeedback(item)) {
      nextQueue.push(item)
      continue
    }

    try {
      await post('/api/user/feedback', {
        type: String(item.type).trim(),
        content: String(item.content).trim()
      })
    } catch {
      nextQueue.push({ ...item, unsynced: true })
    }
  }

  setLocalFeedbackQueue(nextQueue)
}

onMounted(() => {
  statusBarHeight.value = getStatusBarHeight(44)
  userStore.init()
  applyTheme()
  enableWeChatOfficialShare()
})

onShow(() => {
  uni.hideTabBar({ animation: false })
  syncUnsyncedFeedbacks()
  userStore.syncCollectionsFromServer()
  userStore.flushCollectionOps()
  hydrateCollectedGames()
})

const collectedGames = computed(() => {
  return userStore.collections
    .map(id => gameStore.getGameById(id))
    .filter(Boolean)
})



function goDetail(id) {
  uni.navigateTo({ url: `/pages/game-detail/index?id=${id}` })
}

async function hydrateCollectedGames() {
  const missingIds = userStore.collections.filter(id => !gameStore.getGameById(id))
  if (!missingIds.length) return
  await Promise.all(missingIds.map(id => gameStore.fetchGameDetail(id)))
}

function openFeedback(type) {
  feedbackType.value = type
  feedbackContent.value = ''
  showFeedback.value = true
}

async function submitFeedback() {
  if (!feedbackContent.value.trim()) {
    uni.showToast({ title: '请输入反馈内容', icon: 'none' })
    return
  }

  const payload = {
    type: feedbackType.value,
    content: feedbackContent.value.trim()
  }

  try {
    await post('/api/user/feedback', payload)
    syncUnsyncedFeedbacks()
  } catch (e) {
    // 网络失败时本地兜底，避免用户输入丢失
    const feedbacks = getLocalFeedbackQueue()
    feedbacks.push({
      type: payload.type,
      content: payload.content,
      time: Date.now(),
      unsynced: true
    })
    setLocalFeedbackQueue(feedbacks)
  }

  showFeedback.value = false
  uni.showToast({ title: '感谢反馈！', icon: 'success' })
}

hydrateCollectedGames()

onShareAppMessage(() => buildPageSharePayload({
  title: 'BGaide 我的收藏｜把喜欢的桌游存起来',
  path: '/pages/profile/index',
  imageUrl: buildShareImages('/static/icons/profile.png')
}))

onShareTimeline(() => buildTimelineSharePayload({
  title: 'BGaide 我的收藏｜把喜欢的桌游存起来',
  query: '',
  imageUrl: buildShareImages('/static/icons/profile.png')
}))
</script>

<style lang="scss" scoped>
.profile-page {
  padding-bottom: 120rpx;
}

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
  height: 88rpx;
  padding: 0 32rpx;
}

.nav-title {
  font-size: 36rpx;
  font-weight: 800;
  color: var(--color-text-primary);
}

.profile-body {
  padding: 24rpx 32rpx;
}



/* 通用 section */
.section {
  margin-bottom: 32rpx;
}

.section-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.section-count {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
}

/* 紧凑列表 */
.compact-list {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 2rpx solid var(--color-border);
}

.compact-item {
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  gap: 20rpx;
  border-bottom: 1rpx solid var(--color-divider);

  &:last-child {
    border-bottom: none;
  }

  &:active {
    background: var(--color-accent-bg);
  }
}

.compact-thumb {
  width: 80rpx;
  height: 80rpx;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, #a29bfe, #6c5ce7);
  flex-shrink: 0;
}

.compact-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.compact-name {
  font-size: 28rpx;
  font-weight: 600;
  color: var(--color-text-primary);
}

.compact-meta {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
}

.compact-arrow {
  font-size: 32rpx;
  color: var(--color-text-tertiary);
  flex-shrink: 0;
}

.empty-mini {
  padding: 40rpx;
  text-align: center;
  color: var(--color-text-tertiary);
  font-size: 26rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 2rpx solid var(--color-border);
}

/* 反馈 */
.feedback-cards {
  display: flex;
  gap: 16rpx;
}

.feedback-card {
  flex: 1;
  padding: 28rpx 20rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  border: 2rpx solid var(--color-border);
  box-shadow: var(--shadow-sm);

  &:active {
    transform: scale(0.97);
  }
}

.fb-icon {
  font-size: 40rpx;
}

.fb-name {
  font-size: 28rpx;
  font-weight: 600;
  color: var(--color-text-primary);
}

.fb-hint {
  font-size: 22rpx;
  color: var(--color-text-tertiary);
  text-align: center;
}

/* 反馈弹窗 */
.feedback-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-bg-overlay);
  z-index: 1000;
}

.feedback-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  padding: 32rpx 32rpx calc(32rpx + env(safe-area-inset-bottom));
  transform: translateY(100%);
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1);
  z-index: 1001;

  &.show {
    transform: translateY(0);
  }
}

.feedback-title {
  font-size: 34rpx;
  font-weight: 700;
  color: var(--color-text-primary);
  display: block;
  margin-bottom: 24rpx;
}

.feedback-textarea {
  width: 100%;
  height: 240rpx;
  padding: 20rpx;
  font-size: 28rpx;
  color: var(--color-text-primary);
  background: var(--color-bg-card);
  border: 2rpx solid var(--color-border);
  border-radius: var(--radius-md);
  box-sizing: border-box;
}

.feedback-submit {
  margin-top: 24rpx;
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  border-radius: var(--radius-md);
  color: #fff;
  font-size: 30rpx;
  font-weight: 600;
}
</style>
