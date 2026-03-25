<template>
  <view class="page-container detail-page">
    <!-- 自定义导航栏 -->
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content" :style="{ paddingRight: navRightPadding + 'px' }">
        <view class="nav-back" @tap="goBack">
          <text>← 返回</text>
        </view>
      </view>
    </view>

    <view v-if="game" class="detail-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <!-- 封面 -->
      <view class="cover-area">
        <image class="cover-img" :src="game.cover || '/static/icons/placeholder.svg'" mode="aspectFill" />
        <view class="cover-overlay">
          <view class="cover-title-row">
            <text class="cover-title">{{ game.name }}</text>
            <view class="cover-fav" :class="{ active: isFav }" @tap="toggleFav">
              <text>{{ isFav ? '♥ 已收藏' : '♡ 收藏' }}</text>
            </view>
          </view>
          <text class="cover-subtitle">{{ game.nameEn }}</text>
        </view>
      </view>

      <!-- 信息卡片 -->
      <view class="info-card">
        <view class="info-row">
          <view class="info-item">
            <text class="info-icon">👥</text>
            <text class="info-label">人数</text>
            <text class="info-value">{{ game.players[0] }}-{{ game.players[1] }}</text>
          </view>
          <view class="info-item">
            <text class="info-icon">⏱️</text>
            <text class="info-label">时长</text>
            <text class="info-value">{{ game.duration[0] }}-{{ game.duration[1] }}分</text>
          </view>
          <view class="info-item">
            <text class="info-icon">📊</text>
            <text class="info-label">难度</text>
            <text class="info-value">{{ game.difficulty }}</text>
          </view>
          <view class="info-item">
            <text class="info-icon">⭐</text>
            <text class="info-label">BGG</text>
            <text class="info-value accent">{{ game.bggScore }}</text>
          </view>
        </view>
        <view class="info-tags">
          <text v-for="tag in game.tags" :key="tag" class="tag-item">{{ tag }}</text>
        </view>
        <text class="info-desc">{{ game.description }}</text>
      </view>

      <!-- 一分钟速学 -->
      <view v-if="rules" class="rules-zone">
        <text class="section-title">📖 一分钟速学</text>

        <RuleSection stepNumber="1" title="配件清单" hint="游戏包含哪些部件" :items="rules.quickLearn.components"
          listStyle="bullet" />

        <RuleSection stepNumber="2" title="初始设置" hint="开始游戏前的准备工作" :items="normalizedSetupItems" listStyle="bullet" />

        <RuleSection stepNumber="3" title="胜利条件" hint="如何赢得这场游戏" :text="rules.quickLearn.winCondition" />

        <RuleSection stepNumber="4" title="核心回合流程" hint="每个回合做什么" :items="normalizedTurnFlowItems"
          listStyle="none" />
      </view>

      <!-- FAQ -->
      <view v-if="faqList.length" class="faq-zone">
        <text class="section-title">❓ 常见问题 & 疑难裁决</text>

        <!-- FAQ 内搜索 -->
        <view class="faq-search">
          <input class="faq-search-input" type="text" v-model="faqKeyword" placeholder="搜索问题关键词..."
            placeholder-class="faq-placeholder" />
        </view>

        <view class="faq-list">
          <FaqItem v-for="(faq, idx) in filteredFaqs" :key="idx" :item="faq" />
        </view>

        <view v-if="filteredFaqs.length === 0" class="faq-empty">
          <text>没有匹配的问题</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { useGameStore } from '@/stores/game'
import { useUserStore } from '@/stores/user'
import RuleSection from '@/components/RuleSection.vue'
import FaqItem from '@/components/FaqItem.vue'

const gameStore = useGameStore()
const userStore = useUserStore()

const gameId = ref('')
const statusBarHeight = ref(44)
const navRightPadding = ref(16)
const faqKeyword = ref('')

const game = ref(null)
const rules = ref(null)
const faqList = ref([])

onLoad(async (options) => {
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44

  // 适配微信右上角胶囊，避免右侧按钮被系统区域遮挡
  try {
    const menuButtonRect = uni.getMenuButtonBoundingClientRect
      ? uni.getMenuButtonBoundingClientRect()
      : null
    if (menuButtonRect && sysInfo.windowWidth) {
      const capsuleWidth = sysInfo.windowWidth - menuButtonRect.left
      navRightPadding.value = 16 + Math.max(capsuleWidth, 0)
    }
  } catch {
    navRightPadding.value = 16
  }

  userStore.init()

  gameId.value = options.id || ''

  // 并行请求游戏详情、规则、FAQ
  const [gameData, rulesData, faqData] = await Promise.all([
    gameStore.fetchGameDetail(gameId.value),
    gameStore.fetchRules(gameId.value),
    gameStore.fetchFaq(gameId.value)
  ])

  game.value = gameData
  rules.value = rulesData
  faqList.value = faqData || []
})

const isFav = computed(() => userStore.isCollected(gameId.value))

function stripLeadingOrderPrefix(text) {
  const value = String(text || '').trim()
  if (!value) return value
  return value
    .replace(/^第\s*\d+\s*[步项]\s*[-:：.、]?\s*/, '')
    .replace(/^\d+\s*[.．、]\s*/, '')
    .trim()
}

const normalizedSetupItems = computed(() => {
  const setup = rules.value?.quickLearn?.setup || []
  return setup.map(stripLeadingOrderPrefix)
})

const normalizedTurnFlowItems = computed(() => {
  const flow = rules.value?.quickLearn?.turnFlow || []
  return flow.map(stripLeadingOrderPrefix)
})

const filteredFaqs = computed(() => {
  if (!faqKeyword.value) return faqList.value
  const kw = faqKeyword.value.toLowerCase()
  return faqList.value.filter(
    f => f.q.toLowerCase().includes(kw) || f.a.toLowerCase().includes(kw)
  )
})

function toggleFav() {
  userStore.toggleCollection(gameId.value)
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.detail-page {
  padding-bottom: 60rpx;
}

/* 导航栏 */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1rpx solid var(--color-divider);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 88rpx;
  padding: 0 32rpx;
}

.nav-back {
  font-size: 28rpx;
  color: var(--color-accent);
  font-weight: 500;
}

/* 封面 */
.cover-area {
  position: relative;
  width: 100%;
  height: 420rpx;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.cover-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40rpx 32rpx 28rpx;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
}

.cover-title {
  flex: 1;
  min-width: 0;
  font-size: 44rpx;
  font-weight: 800;
  color: #fff;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.3);
}

.cover-title-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.cover-fav {
  flex-shrink: 0;
  height: 52rpx;
  padding: 0 18rpx;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.2);
  border: 2rpx solid rgba(255, 255, 255, 0.35);
  color: #fff;
  display: inline-flex;
  align-items: center;
  font-size: 22rpx;
  font-weight: 700;
  backdrop-filter: blur(8px);

  &:active {
    transform: scale(0.96);
  }

  &.active {
    background: rgba(225, 112, 85, 0.28);
    border-color: rgba(225, 112, 85, 0.65);
  }
}

.cover-subtitle {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.8);
  margin-top: 4rpx;
  display: block;
}

/* 信息卡片 */
.info-card {
  margin: -30rpx 32rpx 24rpx;
  padding: 28rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  position: relative;
  z-index: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6rpx;
}

.info-icon {
  font-size: 36rpx;
}

.info-label {
  font-size: 22rpx;
  color: var(--color-text-tertiary);
}

.info-value {
  font-size: 28rpx;
  font-weight: 700;
  color: var(--color-text-primary);

  &.accent {
    color: var(--color-accent);
  }
}

.info-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 20rpx;
}

.tag-item {
  padding: 6rpx 18rpx;
  border-radius: var(--radius-full);
  font-size: 22rpx;
  color: var(--color-text-secondary);
  background: var(--color-bg-primary);
}

.info-desc {
  display: block;
  margin-top: 20rpx;
  font-size: 28rpx;
  color: var(--color-text-secondary);
  line-height: 1.7;
}

/* 规则速学 */
.rules-zone {
  padding: 0 32rpx;
  margin-bottom: 32rpx;

  .section-title {
    margin-bottom: 20rpx;
  }
}

/* FAQ */
.faq-zone {
  padding: 0 32rpx;

  .section-title {
    margin-bottom: 16rpx;
  }
}

.faq-search {
  margin-bottom: 16rpx;
}

.faq-search-input {
  height: 72rpx;
  padding: 0 24rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  border: 2rpx solid var(--color-border);
  font-size: 26rpx;
  color: var(--color-text-primary);
}

.faq-placeholder {
  color: var(--color-text-tertiary);
}

.faq-empty {
  text-align: center;
  padding: 40rpx;
  color: var(--color-text-tertiary);
  font-size: 26rpx;
}
</style>
