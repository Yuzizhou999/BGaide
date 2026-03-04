<template>
  <view class="page-container timer-page">
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">⏱️ 计时器</text>
        <view style="width: 60rpx" />
      </view>
    </view>

    <view class="timer-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
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
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44
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
  padding-bottom: 60rpx;
}

.nav-bar {
  position: fixed;
  top: 0; left: 0; right: 0;
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

.nav-back { font-size: 28rpx; color: var(--color-accent); }
.nav-title { font-size: 32rpx; font-weight: 700; color: var(--color-text-primary); }

.timer-body {
  padding: 32rpx;
}

/* 模式切换 */
.mode-tabs {
  display: flex;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: 6rpx;
  border: 2rpx solid var(--color-border);
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
  background: var(--color-bg-card);
  border: 2rpx solid var(--color-border);
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
  background: var(--color-bg-card);
  border: 8rpx solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
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
  color: var(--color-text-tertiary);
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
    background: var(--color-bg-card);
    border: 2rpx solid var(--color-border);
    color: var(--color-text-secondary);
  }

  &.primary {
    background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
    color: #fff;

    &.pause {
      background: linear-gradient(135deg, var(--color-danger), #ff7675);
    }
  }

  &:active {
    transform: scale(0.97);
  }
}
</style>
