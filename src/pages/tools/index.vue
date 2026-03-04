<template>
  <view class="page-container tools-page">
    <!-- 自定义导航栏 -->
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <text class="nav-title">🛠️ 工具箱</text>
      </view>
    </view>

    <view class="tools-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <text class="tools-desc">游玩辅助工具，让桌游体验更丝滑</text>

      <view class="tools-grid">
        <view class="tool-card" @tap="goTo('tools-first-player')">
          <view class="tool-icon-wrap dice">
            <text class="tool-icon">🎯</text>
          </view>
          <text class="tool-name">起始玩家</text>
          <text class="tool-hint">摇号决定谁先开始</text>
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
      </view>
    </view>

    <!-- 自定义 TabBar -->
    <CustomTabBar :current="1" />
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

.tools-body {
  padding: 32rpx;
}

.tools-desc {
  font-size: 28rpx;
  color: var(--color-text-tertiary);
  margin-bottom: 32rpx;
  display: block;
}

.tools-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24rpx;
}

.tool-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: 36rpx 28rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12rpx;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease;
  border: 2rpx solid var(--color-border);

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
  color: var(--color-text-tertiary);
  text-align: center;
}
</style>
