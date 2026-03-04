<template>
  <view class="page-container scorer-page">
    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">📊 万能计分板</text>
        <view class="nav-action" @tap="resetAll"><text>重置</text></view>
      </view>
    </view>

    <view class="scorer-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <!-- 添加玩家 -->
      <view class="add-section">
        <view class="input-row">
          <input
            class="name-input"
            v-model="newName"
            placeholder="玩家昵称"
            @confirm="addPlayer"
          />
          <view class="add-btn" @tap="addPlayer"><text>+ 添加</text></view>
        </view>
      </view>

      <!-- 玩家列表 -->
      <view class="player-list">
        <view
          v-for="(player, idx) in toolsStore.scorer.players"
          :key="idx"
          class="player-row"
          :class="{ 'is-leading': isLeading(idx) }"
        >
          <view class="player-rank">
            <text class="rank-num">{{ getRank(idx) }}</text>
          </view>
          <view class="player-info">
            <text class="player-name">{{ player.name }}</text>
          </view>
          <view class="player-score-area">
            <view class="score-btn minus" @tap="changeScore(idx, -1)">
              <text>−</text>
            </view>
            <text class="score-value">{{ player.score }}</text>
            <view class="score-btn plus" @tap="changeScore(idx, 1)">
              <text>+</text>
            </view>
          </view>
          <view class="player-remove" @tap="removePlayer(idx)">
            <text>✕</text>
          </view>
        </view>

        <view v-if="toolsStore.scorer.players.length === 0" class="empty-state">
          <text class="empty-icon">📊</text>
          <text class="empty-text">添加玩家开始计分</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToolsStore } from '@/stores/tools'

const toolsStore = useToolsStore()
const statusBarHeight = ref(44)
const newName = ref('')

onMounted(() => {
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44
  toolsStore.init()
})

function addPlayer() {
  const name = newName.value.trim()
  if (name) {
    toolsStore.addPlayer(name)
    newName.value = ''
  }
}

function changeScore(idx, delta) {
  toolsStore.updateScore(idx, delta)
  // 微震动反馈
  uni.vibrateShort({ type: 'light' })
}

function removePlayer(idx) {
  toolsStore.removePlayer(idx)
}

function resetAll() {
  uni.showModal({
    title: '重置确认',
    content: '确定要清空所有计分数据吗？',
    success: (res) => {
      if (res.confirm) toolsStore.resetScorer()
    }
  })
}

// 计算排名
const sortedScores = computed(() => {
  return [...toolsStore.scorer.players]
    .map((p, i) => ({ ...p, originalIdx: i }))
    .sort((a, b) => b.score - a.score)
})

function getRank(idx) {
  const player = toolsStore.scorer.players[idx]
  const rank = sortedScores.value.findIndex(p => p.originalIdx === idx) + 1
  return rank
}

function isLeading(idx) {
  if (toolsStore.scorer.players.length < 2) return false
  return getRank(idx) === 1
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.scorer-page {
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
.nav-action { font-size: 26rpx; color: var(--color-danger); }

.scorer-body {
  padding: 24rpx 32rpx;
}

.input-row {
  display: flex;
  gap: 16rpx;
}

.name-input {
  flex: 1;
  height: 80rpx;
  padding: 0 24rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  border: 2rpx solid var(--color-border);
  font-size: 28rpx;
  color: var(--color-text-primary);
}

.add-btn {
  padding: 0 28rpx;
  height: 80rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  border-radius: var(--radius-md);
  color: #fff;
  font-size: 28rpx;
  font-weight: 600;
}

.player-list {
  margin-top: 32rpx;
}

.player-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
  padding: 20rpx 24rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  margin-bottom: 12rpx;
  border: 2rpx solid var(--color-border);
  transition: all 0.3s ease;

  &.is-leading {
    border-color: var(--color-accent);
    background: var(--color-accent-bg);
  }
}

.player-rank {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: var(--color-bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rank-num {
  font-size: 24rpx;
  font-weight: 700;
  color: var(--color-text-secondary);
}

.is-leading .rank-num {
  color: var(--color-accent);
}

.player-info {
  flex: 1;
}

.player-name {
  font-size: 30rpx;
  font-weight: 600;
  color: var(--color-text-primary);
}

.player-score-area {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.score-btn {
  width: 64rpx;
  height: 64rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  font-weight: 700;

  &.minus {
    background: rgba(225, 112, 85, 0.1);
    color: var(--color-danger);
  }
  &.plus {
    background: rgba(0, 184, 148, 0.1);
    color: var(--color-success);
  }

  &:active {
    transform: scale(0.9);
  }
}

.score-value {
  font-size: 40rpx;
  font-weight: 800;
  color: var(--color-text-primary);
  min-width: 80rpx;
  text-align: center;
}

.player-remove {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  padding: 8rpx;
  flex-shrink: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
}

.empty-icon { font-size: 80rpx; margin-bottom: 16rpx; }
.empty-text { font-size: 28rpx; color: var(--color-text-tertiary); }
</style>
