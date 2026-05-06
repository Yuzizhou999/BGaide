<template>
  <view class="page-container timer-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">⏱️ 计时器</text>
        <view style="width: 60rpx" />
      </view>
    </view>

    <view class="timer-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <view class="hero-tip">
        <text class="hero-title">专注回合节奏</text>
        <text class="hero-desc">倒计时适合限时决策，正计时适合记录整局时长。</text>
      </view>

      <!-- 模式切换 -->
      <view class="mode-tabs">
        <view
          class="mode-tab"
          :class="{ active: toolsStore.timer.mode === 'countdown' }"
          @tap="switchMode('countdown')"
        >
          <text>⏳ 倒计时</text>
        </view>
        <view
          class="mode-tab"
          :class="{ active: toolsStore.timer.mode === 'stopwatch' }"
          @tap="switchMode('stopwatch')"
        >
          <text>⏱️ 正计时</text>
        </view>
      </view>

      <!-- 倒计时预设 -->
      <view v-if="toolsStore.timer.mode === 'countdown' && !toolsStore.timer.isRunning && toolsStore.timer.elapsedSeconds === 0" class="presets">
        <text class="preset-label">预设时间</text>
        <view class="preset-grid">
          <view
            v-for="p in presets"
            :key="p.seconds"
            class="preset-chip"
            :class="{ active: toolsStore.timer.targetSeconds === p.seconds }"
            @tap="setTarget(p.seconds)"
          >
            <text>{{ p.label }}</text>
          </view>
        </view>
      </view>

      <!-- 时钟显示 -->
      <view class="clock-area">
        <view class="clock-ring" :class="{ running: toolsStore.timer.isRunning, danger: isTimeUp }">
          <view class="clock-inner">
            <text class="clock-time">{{ displayTime }}</text>
            <text class="clock-label">
              {{ toolsStore.timer.mode === 'countdown' ? '剩余时间' : '已用时间' }}
            </text>
          </view>
        </view>
      </view>

      <!-- 控制按钮 -->
      <view class="control-row">
        <view class="ctrl-btn secondary" @tap="resetTimer">
          <text>重置</text>
        </view>
        <view
          class="ctrl-btn primary"
          :class="{ pause: toolsStore.timer.isRunning }"
          @tap="toggleTimer"
        >
          <text>{{ toolsStore.timer.isRunning ? '⏸ 暂停' : '▶ 开始' }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useToolsStore } from '@/stores/tools'
import { getStatusBarHeight } from '@/utils/system'

const toolsStore = useToolsStore()
const statusBarHeight = ref(44)
let timerInterval = null

const presets = [
  { label: '30秒', seconds: 30 },
  { label: '1分钟', seconds: 60 },
  { label: '2分钟', seconds: 120 },
  { label: '3分钟', seconds: 180 },
  { label: '5分钟', seconds: 300 },
  { label: '10分钟', seconds: 600 },
  { label: '15分钟', seconds: 900 },
  { label: '30分钟', seconds: 1800 }
]

onMounted(() => {
  statusBarHeight.value = getStatusBarHeight(44)
  toolsStore.init()
  // 如果切回时在运行状态，恢复计时
  if (toolsStore.timer.isRunning) {
    startInterval()
  }
})

onUnmounted(() => {
  clearInterval(timerInterval)
})

const displayTime = computed(() => {
  let seconds
  if (toolsStore.timer.mode === 'countdown') {
    seconds = Math.max(0, toolsStore.timer.targetSeconds - toolsStore.timer.elapsedSeconds)
  } else {
    seconds = toolsStore.timer.elapsedSeconds
  }
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

const isTimeUp = computed(() => {
  if (toolsStore.timer.mode !== 'countdown') return false
  return toolsStore.timer.elapsedSeconds >= toolsStore.timer.targetSeconds
})

// 监听时间终了
watch(isTimeUp, (val) => {
  if (val) {
    toolsStore.pauseTimer()
    clearInterval(timerInterval)
    // 长震动提醒
    uni.vibrateLong()
    uni.showToast({ title: '⏰ 时间到！', icon: 'none', duration: 2000 })
  }
})

function switchMode(mode) {
  clearInterval(timerInterval)
  toolsStore.setTimerMode(mode)
}

function setTarget(seconds) {
  toolsStore.setTargetSeconds(seconds)
}

function toggleTimer() {
  if (toolsStore.timer.isRunning) {
    toolsStore.pauseTimer()
    clearInterval(timerInterval)
  } else {
    toolsStore.startTimer()
    startInterval()
  }
}

function startInterval() {
  clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    // 倒计时模式检查是否到时
    if (toolsStore.timer.mode === 'countdown' &&
        toolsStore.timer.elapsedSeconds >= toolsStore.timer.targetSeconds) {
      return
    }
    toolsStore.tickTimer()
  }, 1000)
}

function resetTimer() {
  clearInterval(timerInterval)
  toolsStore.resetTimer()
}

function goBack() { uni.navigateBack() }
</script>

<style lang="scss" scoped>
.timer-page {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding-bottom: 60rpx;
  background: linear-gradient(180deg, #fffdf8 0%, #fff7ee 68%, #fff5e9 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(52rpx);
  pointer-events: none;
}

.orb-a {
  width: 360rpx;
  height: 360rpx;
  top: 160rpx;
  right: -100rpx;
  background: radial-gradient(circle, rgba(9, 132, 227, 0.16), rgba(9, 132, 227, 0));
}

.orb-b {
  width: 340rpx;
  height: 340rpx;
  bottom: 120rpx;
  left: -80rpx;
  background: radial-gradient(circle, rgba(225, 112, 85, 0.16), rgba(225, 112, 85, 0));
}

.nav-bar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.74);
  backdrop-filter: blur(22px);
  border-bottom: 1rpx solid rgba(238, 221, 200, 0.65);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 88rpx;
  padding: 0 32rpx;
}

.nav-back { font-size: 28rpx; color: var(--color-accent); }
.nav-title { font-size: 32rpx; font-weight: 700; color: var(--color-text-primary); }

.timer-body {
  position: relative;
  z-index: 2;
  padding: 32rpx;
}

.hero-tip {
  padding: 22rpx 24rpx;
  border-radius: var(--radius-lg);
  background: linear-gradient(145deg, rgba(255, 237, 210, 0.9), rgba(255, 248, 238, 0.92));
  border: 2rpx solid rgba(255, 187, 112, 0.32);
  box-shadow: 0 14rpx 34rpx rgba(180, 111, 55, 0.1);
  margin-bottom: 22rpx;
}

.hero-title {
  display: block;
  font-size: 30rpx;
  font-weight: 800;
  color: #8a4f1f;
}

.hero-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.6;
  color: #9a6d43;
}

/* 模式切换 */
.mode-tabs {
  display: flex;
  background: rgba(255, 255, 255, 0.62);
  backdrop-filter: blur(16px);
  border-radius: var(--radius-lg);
  padding: 6rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.82);
  box-shadow: 0 12rpx 24rpx rgba(68, 48, 28, 0.08);
}

.mode-tab {
  flex: 1;
  height: 76rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  font-size: 28rpx;
  color: var(--color-text-secondary);
  transition: all 0.3s ease;

  &.active {
    background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
    color: #fff;
    font-weight: 600;
  }
}

/* 预设 */
.presets {
  margin-top: 32rpx;
  padding: 20rpx;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.6);
  border: 2rpx solid rgba(255, 255, 255, 0.8);
}

.preset-label {
  font-size: 26rpx;
  color: var(--color-text-tertiary);
  display: block;
  margin-bottom: 16rpx;
}

.preset-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.preset-chip {
  padding: 14rpx 28rpx;
  border-radius: var(--radius-full);
  font-size: 26rpx;
  color: var(--color-text-secondary);
  background: linear-gradient(155deg, rgba(255, 255, 255, 0.9), rgba(248, 244, 238, 0.9));
  border: 2rpx solid rgba(255, 255, 255, 0.85);
  box-shadow: 0 8rpx 16rpx rgba(56, 35, 17, 0.06);
  transition: all 0.2s ease;

  &.active {
    background: var(--color-accent-bg);
    color: var(--color-accent);
    border-color: var(--color-accent);
    font-weight: 600;
  }
}

/* 时钟 */
.clock-area {
  display: flex;
  justify-content: center;
  margin: 60rpx 0;
}

.clock-ring {
  width: 400rpx;
  height: 400rpx;
  border-radius: 50%;
  background: linear-gradient(165deg, rgba(255, 255, 255, 0.95), rgba(255, 244, 230, 0.95));
  border: 8rpx solid rgba(255, 209, 155, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 22rpx 48rpx rgba(73, 51, 27, 0.12);
  transition: all 0.3s ease;

  &.running {
    border-color: var(--color-accent);
    box-shadow: 0 0 60rpx var(--color-accent-bg);
    animation: breathe 2s ease-in-out infinite;
  }

  &.danger {
    border-color: var(--color-danger);
    box-shadow: 0 0 60rpx rgba(225, 112, 85, 0.3);
    animation: shake 0.5s ease;
  }
}

@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-8rpx); }
  75% { transform: translateX(8rpx); }
}

.clock-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.clock-time {
  font-size: 80rpx;
  font-weight: 800;
  color: var(--color-text-primary);
  letter-spacing: 4rpx;
  font-variant-numeric: tabular-nums;
}

.clock-label {
  font-size: 24rpx;
  color: #91785f;
  margin-top: 4rpx;
}

/* 控制按钮 */
.control-row {
  display: flex;
  gap: 24rpx;
}

.ctrl-btn {
  flex: 1;
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  font-size: 30rpx;
  font-weight: 600;

  &.secondary {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(247, 243, 236, 0.95));
    border: 2rpx solid rgba(211, 197, 179, 0.84);
    color: var(--color-text-secondary);
    box-shadow: 0 12rpx 24rpx rgba(56, 35, 17, 0.08);
  }

  &.primary {
    background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
    color: #fff;
    box-shadow: 0 14rpx 28rpx rgba(225, 112, 85, 0.24);

    &.pause {
      background: linear-gradient(135deg, var(--color-danger), #ff7675);
    }
  }

  &:active {
    transform: scale(0.97);
  }
}
</style>
