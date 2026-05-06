<template>
  <view class="page-container fp-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">🎯 起始玩家</text>
        <view style="width: 80rpx" />
      </view>
    </view>

    <view class="fp-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <view class="hero-tip">
        <text class="hero-title">让先手更公平</text>
        <text class="hero-desc">输入玩家后一键摇号，再也不为先手烦恼😣。</text>
      </view>

      <!-- 输入区 -->
      <view class="input-section">
        <text class="section-label">添加玩家昵称</text>
        <view class="input-row">
          <input class="name-input" type="text" v-model="newName" placeholder="输入昵称..." @confirm="addPlayer" />
          <view class="add-btn" @tap="addPlayer">
            <text>+</text>
          </view>
        </view>
      </view>

      <!-- 玩家列表 -->
      <view class="players-list">
        <view v-for="(name, idx) in players" :key="idx" class="player-chip">
          <text class="chip-name">{{ name }}</text>
          <view class="chip-remove" @tap="removePlayer(idx)">✕</view>
        </view>
        <view v-if="players.length === 0" class="empty-hint">
          <text>至少添加 2 位玩家</text>
        </view>
      </view>

      <!-- 摇号结果 -->
      <view class="result-area">
        <view class="result-display" :class="{ spinning: isSpinning, revealed: result && !isSpinning }">
          <text class="result-text">{{ displayText }}</text>
        </view>
      </view>

      <!-- 操作按钮 -->
      <view class="action-row">
        <view class="roll-btn" :class="{ disabled: players.length < 2 || isSpinning }" @tap="startRoll">
          <text>{{ isSpinning ? '摇号中...' : '🎲 开始摇号' }}</text>
        </view>
        <view class="reset-btn" @tap="reset">
          <text>重置</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getStatusBarHeight } from '@/utils/system'

const statusBarHeight = ref(44)
const newName = ref('')
const players = ref([])
const result = ref('')
const isSpinning = ref(false)

onMounted(() => {
  statusBarHeight.value = getStatusBarHeight(44)
})

const displayText = computed(() => {
  if (isSpinning.value) return '🎲'
  if (result.value) return result.value
  return '?'
})

function addPlayer() {
  const name = newName.value.trim()
  if (name && !players.value.includes(name)) {
    players.value.push(name)
    newName.value = ''
  }
}

function removePlayer(idx) {
  players.value.splice(idx, 1)
}

function startRoll() {
  if (players.value.length < 2 || isSpinning.value) return

  isSpinning.value = true
  result.value = ''

  // 摇号动画：快速切换名字
  let count = 0
  const maxCount = 20
  const interval = setInterval(() => {
    const randomIdx = Math.floor(Math.random() * players.value.length)
    result.value = players.value[randomIdx]
    count++

    if (count >= maxCount) {
      clearInterval(interval)
      // 最终结果
      const finalIdx = Math.floor(Math.random() * players.value.length)
      result.value = players.value[finalIdx]
      isSpinning.value = false

      // 震动反馈
      uni.vibrateShort({ type: 'heavy' })
    }
  }, 80)
}

function reset() {
  players.value = []
  result.value = ''
  isSpinning.value = false
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.fp-page {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding-bottom: 60rpx;
  background: linear-gradient(180deg, #fffdf9 0%, #fff8f0 66%, #fff5ea 100%);
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
  top: 180rpx;
  right: -100rpx;
  background: radial-gradient(circle, rgba(116, 185, 255, 0.18), rgba(116, 185, 255, 0));
}

.orb-b {
  width: 340rpx;
  height: 340rpx;
  bottom: 130rpx;
  left: -90rpx;
  background: radial-gradient(circle, rgba(255, 159, 67, 0.18), rgba(255, 159, 67, 0));
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
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

.nav-back {
  font-size: 28rpx;
  color: var(--color-accent);
  width: 80rpx;
  white-space: nowrap;
}

.nav-title {
  font-size: 32rpx;
  font-weight: 700;
  color: var(--color-text-primary);
}

.fp-body {
  position: relative;
  z-index: 2;
  padding: 32rpx;
}

.hero-tip {
  padding: 22rpx 24rpx;
  border-radius: var(--radius-lg);
  background: linear-gradient(140deg, rgba(230, 241, 255, 0.9), rgba(243, 250, 255, 0.92));
  border: 2rpx solid rgba(116, 185, 255, 0.28);
  box-shadow: 0 14rpx 34rpx rgba(60, 95, 140, 0.1);
  margin-bottom: 22rpx;
}

.hero-title {
  display: block;
  font-size: 30rpx;
  font-weight: 800;
  color: #2b6ea3;
}

.hero-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.55;
  color: #507ea3;
}

.section-label {
  font-size: 28rpx;
  color: var(--color-text-secondary);
  margin-bottom: 16rpx;
  display: block;
}

.input-row {
  display: flex;
  gap: 16rpx;
  padding: 18rpx;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.62);
  border: 2rpx solid rgba(255, 255, 255, 0.82);
}

.name-input {
  flex: 1;
  height: 80rpx;
  padding: 0 24rpx;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(247, 243, 236, 0.95));
  border-radius: var(--radius-md);
  border: 2rpx solid var(--color-border);
  font-size: 28rpx;
  color: var(--color-text-primary);
}

.add-btn {
  width: 80rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  border-radius: var(--radius-md);
  color: #fff;
  font-size: 40rpx;
  font-weight: 700;
  box-shadow: 0 12rpx 24rpx rgba(225, 112, 85, 0.2);
}

.players-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-top: 24rpx;
  min-height: 80rpx;
}

.player-chip {
  display: flex;
  align-items: center;
  gap: 8rpx;
  padding: 10rpx 20rpx;
  background: linear-gradient(145deg, rgba(225, 112, 85, 0.14), rgba(253, 203, 110, 0.14));
  border-radius: var(--radius-full);
  border: 2rpx solid rgba(225, 112, 85, 0.42);
}

.chip-name {
  font-size: 28rpx;
  color: var(--color-accent);
  font-weight: 500;
}

.chip-remove {
  font-size: 22rpx;
  color: var(--color-accent);
  opacity: 0.6;
}

.empty-hint {
  width: 100%;
  text-align: center;
  padding: 40rpx;
  color: var(--color-text-tertiary);
  font-size: 26rpx;
}

.result-area {
  display: flex;
  justify-content: center;
  margin: 60rpx 0;
}

.result-display {
  width: 320rpx;
  height: 320rpx;
  border-radius: 50%;
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.95), rgba(255, 244, 230, 0.95));
  border: 6rpx solid rgba(255, 209, 155, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 22rpx 48rpx rgba(73, 51, 27, 0.12);
  transition: all 0.3s ease;

  &.spinning {
    animation: pulse 0.3s ease-in-out infinite;
    border-color: var(--color-accent);
    box-shadow: 0 0 40rpx var(--color-accent-bg);
  }

  &.revealed {
    border-color: var(--color-success);
    box-shadow: 0 0 40rpx rgba(0, 184, 148, 0.2);
  }
}

.result-text {
  font-size: 56rpx;
  font-weight: 800;
  color: var(--color-text-primary);
}

@keyframes pulse {

  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }
}

.action-row {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.roll-btn {
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  border-radius: var(--radius-lg);
  color: #fff;
  font-size: 34rpx;
  font-weight: 700;

  &.disabled {
    opacity: 0.5;
  }

  &:active:not(.disabled) {
    transform: scale(0.98);
  }
}

.reset-btn {
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(247, 243, 236, 0.95));
  border-radius: var(--radius-lg);
  border: 2rpx solid rgba(211, 197, 179, 0.84);
  color: var(--color-text-secondary);
  font-size: 28rpx;
}
</style>
