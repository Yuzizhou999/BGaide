<template>
  <view class="page-container tools-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>
    <view class="bg-orb orb-c"></view>

    <!-- 自定义导航栏 -->
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <text class="nav-title">🛠️ 工具箱</text>
      </view>
    </view>

    <view class="tools-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <view class="hero-card">
        <text class="hero-title">一套趁手小工具</text>
        <text class="hero-desc">从选先手到计分再到趣味挑战，开局就能用，操作都很轻快。</text>
      </view>

      <view class="tools-grid">
        <view class="tool-card" @tap="goTo('tools-first-player')">
          <view class="tool-icon-wrap dice">
            <text class="tool-icon">🎯</text>
          </view>
          <text class="tool-name">起始玩家</text>
          <text class="tool-hint">摇号决定谁先开始</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-spin-bottle')">
          <view class="tool-icon-wrap bottle">
            <text class="tool-icon">🍾</text>
          </view>
          <text class="tool-name">转瓶子</text>
          <text class="tool-hint">赛博转瓶决定先手</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-scorer')">
          <view class="tool-icon-wrap score">
            <text class="tool-icon">📊</text>
          </view>
          <text class="tool-name">万能计分板</text>
          <text class="tool-hint">多人简单加减分</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-advanced-scorer')">
          <view class="tool-icon-wrap advanced">
            <text class="tool-icon">🏛️</text>
          </view>
          <text class="tool-name">高级计分器</text>
          <text class="tool-hint">七大奇迹模板求和</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-timer')">
          <view class="tool-icon-wrap timer">
            <text class="tool-icon">⏱️</text>
          </view>
          <text class="tool-name">桌游计时器</text>
          <text class="tool-hint">正/倒计时 + 震动</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-punishment')">
          <view class="tool-icon-wrap punish">
            <text class="tool-icon">🎭</text>
          </view>
          <text class="tool-name">趣味惩罚</text>
          <text class="tool-hint">随机挑战 + 全屏特效</text>
        </view>

        <view class="tool-card" @tap="goTo('tools-ai')">
          <view class="tool-icon-wrap ai">
            <text class="tool-icon">🤖</text>
          </view>
          <text class="tool-name">桌游 AI 助手</text>
          <text class="tool-hint">规则答疑 + 开局建议</text>
        </view>
      </view>
    </view>

    <!-- 自定义 TabBar -->
    <CustomTabBar :current="2" />
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { applyTheme, getTheme } from '@/utils/theme'
import CustomTabBar from '@/components/CustomTabBar.vue'

const statusBarHeight = ref(44)

onMounted(() => {
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44
  applyTheme(getTheme())
})

onShow(() => {
  uni.hideTabBar({ animation: false })
})

function goTo(page) {
  uni.navigateTo({ url: `/pages/${page}/index` })
}
</script>

<style lang="scss" scoped>
.tools-page {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding-bottom: 120rpx;
  background: linear-gradient(180deg, #fffdf8 0%, #fff7ec 62%, #fff5e9 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(52rpx);
  pointer-events: none;
}

.orb-a {
  width: 420rpx;
  height: 420rpx;
  top: -120rpx;
  left: -130rpx;
  background: radial-gradient(circle, rgba(255, 169, 95, 0.22), rgba(255, 169, 95, 0));
}

.orb-b {
  width: 360rpx;
  height: 360rpx;
  top: 280rpx;
  right: -120rpx;
  background: radial-gradient(circle, rgba(225, 112, 85, 0.18), rgba(225, 112, 85, 0));
}

.orb-c {
  width: 340rpx;
  height: 340rpx;
  bottom: 60rpx;
  left: -100rpx;
  background: radial-gradient(circle, rgba(255, 220, 145, 0.22), rgba(255, 220, 145, 0));
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(22px);
  border-bottom: 1rpx solid rgba(238, 221, 200, 0.65);
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
  letter-spacing: 1rpx;
}

.tools-body {
  position: relative;
  z-index: 2;
  padding: 32rpx;
}

.hero-card {
  padding: 26rpx 26rpx;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, rgba(255, 233, 198, 0.92), rgba(255, 246, 230, 0.92));
  border: 2rpx solid rgba(255, 187, 112, 0.35);
  box-shadow: 0 18rpx 40rpx rgba(183, 116, 58, 0.1);
  margin-bottom: 28rpx;
}

.hero-title {
  display: block;
  font-size: 32rpx;
  color: #8a4f1f;
  font-weight: 800;
}

.hero-desc {
  display: block;
  font-size: 24rpx;
  color: #9b6a3d;
  line-height: 1.6;
  margin-top: 8rpx;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24rpx;
}

.tool-card {
  background: linear-gradient(165deg, rgba(255, 255, 255, 0.92), rgba(255, 247, 238, 0.92));
  border-radius: var(--radius-lg);
  padding: 36rpx 28rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  box-shadow: 0 16rpx 32rpx rgba(56, 35, 17, 0.08);
  transition: transform 0.2s ease;
  border: 2rpx solid rgba(255, 255, 255, 0.75);

  &:active {
    transform: scale(0.96);
  }
}

.tool-icon-wrap {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;

  &.dice {
    background: linear-gradient(135deg, #e17055, #fdcb6e);
  }

  &.score {
    background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  }

  &.advanced {
    background: linear-gradient(135deg, #00b894, #55efc4);
  }

  &.timer {
    background: linear-gradient(135deg, #0984e3, #74b9ff);
  }

  &.bottle {
    background: linear-gradient(135deg, #6c5ce7, #e17055);
  }

  &.punish {
    background: linear-gradient(135deg, #e17055, #ff9f43);
  }

  &.ai {
    background: linear-gradient(135deg, #0f9d8a, #6fcf97);
  }
}

.tool-icon {
  font-size: 44rpx;
}

.tool-name {
  font-size: 30rpx;
  font-weight: 700;
  color: var(--color-text-primary);
}

.tool-hint {
  font-size: 24rpx;
  color: #8d7d6c;
  text-align: center;
  line-height: 1.5;
}
</style>
