<template>
  <view class="page-container adv-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">🏛️ 高级计分器</text>
        <view class="nav-action" @tap="resetAll"><text>重置</text></view>
      </view>
    </view>

    <view class="adv-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <view class="hero-board">
        <text class="hero-title">七大奇迹专用计分台</text>
        <text class="hero-desc">横向录入各分项，系统实时求和并显示总分。</text>
      </view>

      <text class="mode-label">七大奇迹 积分模板</text>

      <!-- 添加玩家 -->
      <view class="input-row">
        <input class="name-input" v-model="newName" placeholder="玩家昵称" @confirm="addPlayer" />
        <view class="add-btn" @tap="addPlayer"><text>+</text></view>
      </view>

      <!-- 横向滚动计分表 -->
      <scroll-view class="score-table-scroll" scroll-x v-if="toolsStore.advancedScorer.players.length > 0">
        <view class="score-table">
          <!-- 表头 -->
          <view class="table-header">
            <view class="th-cell th-name">玩家</view>
            <view v-for="cat in categories" :key="cat.key" class="th-cell" :style="{ background: cat.color + '15' }">
              <text class="th-icon">{{ cat.icon }}</text>
              <text class="th-label">{{ cat.label }}</text>
            </view>
            <view class="th-cell th-total">总分</view>
          </view>

          <!-- 玩家行 -->
          <view
            v-for="(player, pIdx) in toolsStore.advancedScorer.players"
            :key="pIdx"
            class="table-row"
          >
            <view class="td-cell td-name">
              <text>{{ player.name }}</text>
              <view class="remove-mini" @tap="removePlayer(pIdx)">✕</view>
            </view>
            <view v-for="cat in categories" :key="cat.key" class="td-cell">
              <input
                class="score-input"
                type="number"
                :value="player[cat.key]"
                @blur="updateField(pIdx, cat.key, $event)"
              />
            </view>
            <view class="td-cell td-total">
              <text class="total-value">{{ player.total }}</text>
            </view>
          </view>
        </view>
      </scroll-view>

      <view v-else class="empty-state">
        <text class="empty-icon">🏛️</text>
        <text class="empty-text">添加玩家，输入各类得分</text>
        <text class="empty-hint">系统自动汇总求和</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToolsStore } from '@/stores/tools'

const toolsStore = useToolsStore()
const statusBarHeight = ref(44)
const newName = ref('')

const categories = [
  { key: 'military', label: '军事', icon: '⚔️', color: '#e17055' },
  { key: 'coin', label: '金币', icon: '🪙', color: '#fdcb6e' },
  { key: 'wonder', label: '奇迹', icon: '🏛️', color: '#6c5ce7' },
  { key: 'civic', label: '市政', icon: '🏢', color: '#0984e3' },
  { key: 'commercial', label: '商业', icon: '🛒', color: '#00b894' },
  { key: 'science', label: '科学', icon: '🔬', color: '#00cec9' },
  { key: 'guild', label: '行会', icon: '🤝', color: '#636e72' }
]

onMounted(() => {
  const sysInfo = uni.getSystemInfoSync()
  statusBarHeight.value = sysInfo.statusBarHeight || 44
  toolsStore.init()
})

function addPlayer() {
  const name = newName.value.trim()
  if (name) {
    toolsStore.addAdvPlayer(name)
    newName.value = ''
  }
}

function removePlayer(idx) {
  toolsStore.removeAdvPlayer(idx)
}

function updateField(pIdx, field, e) {
  const val = e.detail.value
  toolsStore.updateAdvScore(pIdx, field, val)
}

function resetAll() {
  uni.showModal({
    title: '重置确认',
    content: '确定要清空所有高级计分数据吗？',
    success: (res) => {
      if (res.confirm) toolsStore.resetAdvScorer()
    }
  })
}

function goBack() { uni.navigateBack() }
</script>

<style lang="scss" scoped>
.adv-page {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding-bottom: 60rpx;
  background: linear-gradient(180deg, #fffdf8 0%, #fff8ef 68%, #fff5ea 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(54rpx);
  pointer-events: none;
}

.orb-a {
  width: 380rpx;
  height: 380rpx;
  top: 220rpx;
  right: -130rpx;
  background: radial-gradient(circle, rgba(108, 92, 231, 0.16), rgba(108, 92, 231, 0));
}

.orb-b {
  width: 360rpx;
  height: 360rpx;
  bottom: 120rpx;
  left: -90rpx;
  background: radial-gradient(circle, rgba(0, 184, 148, 0.16), rgba(0, 184, 148, 0));
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
.nav-action { font-size: 26rpx; color: var(--color-danger); }

.adv-body {
  position: relative;
  z-index: 2;
  padding: 24rpx 32rpx;
}

.hero-board {
  padding: 22rpx 24rpx;
  border-radius: var(--radius-lg);
  background: linear-gradient(145deg, rgba(240, 236, 255, 0.9), rgba(247, 245, 255, 0.92));
  border: 2rpx solid rgba(108, 92, 231, 0.24);
  box-shadow: 0 14rpx 34rpx rgba(73, 62, 136, 0.1);
  margin-bottom: 16rpx;
}

.hero-title {
  display: block;
  font-size: 30rpx;
  font-weight: 800;
  color: #5d4cb6;
}

.hero-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  line-height: 1.55;
  color: #6f63a3;
}

.mode-label {
  font-size: 26rpx;
  color: var(--color-text-tertiary);
  display: block;
  margin-bottom: 16rpx;
}

.input-row {
  display: flex;
  gap: 16rpx;
  margin-bottom: 24rpx;
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
  font-size: 36rpx;
  font-weight: 700;
  box-shadow: 0 12rpx 24rpx rgba(225, 112, 85, 0.2);
}

/* 计分表 */
.score-table-scroll {
  white-space: nowrap;
  margin-top: 16rpx;
  padding: 16rpx;
  border-radius: var(--radius-lg);
  background: rgba(255, 255, 255, 0.64);
  border: 2rpx solid rgba(255, 255, 255, 0.82);
}

.score-table {
  display: inline-flex;
  flex-direction: column;
  min-width: 100%;
}

.table-header, .table-row {
  display: inline-flex;
  align-items: stretch;
}

.th-cell, .td-cell {
  min-width: 120rpx;
  padding: 16rpx 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: 2rpx solid var(--color-divider);
  flex-shrink: 0;
}

.th-name, .td-name {
  min-width: 140rpx;
  position: sticky;
  left: 0;
  z-index: 2;
  background: rgba(255, 255, 255, 0.95);
}

.th-cell {
  border-radius: var(--radius-sm);
  margin: 4rpx;
  border: 1rpx solid rgba(255, 255, 255, 0.7);
}

.th-icon { font-size: 28rpx; }
.th-label { font-size: 20rpx; color: var(--color-text-secondary); margin-top: 4rpx; }

.th-total {
  background: var(--color-accent-bg) !important;
  font-weight: 700;
  color: var(--color-accent);
}

.td-name {
  flex-direction: row;
  gap: 8rpx;
  font-size: 26rpx;
  font-weight: 600;
  color: var(--color-text-primary);
}

.remove-mini {
  font-size: 20rpx;
  color: var(--color-text-tertiary);
}

.score-input {
  width: 100rpx;
  height: 60rpx;
  text-align: center;
  font-size: 28rpx;
  font-weight: 600;
  color: var(--color-text-primary);
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 243, 236, 0.96));
  border: 2rpx solid rgba(211, 197, 179, 0.84);
  border-radius: var(--radius-sm);
}

.td-total {
  background: var(--color-accent-bg);
}

.total-value {
  font-size: 34rpx;
  font-weight: 800;
  color: var(--color-accent);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
  background: rgba(255, 255, 255, 0.58);
  border-radius: var(--radius-lg);
  border: 2rpx dashed rgba(228, 210, 188, 0.8);
}
.empty-icon { font-size: 80rpx; margin-bottom: 16rpx; }
.empty-text { font-size: 28rpx; color: var(--color-text-secondary); font-weight: 600; }
.empty-hint { font-size: 24rpx; color: var(--color-text-tertiary); margin-top: 8rpx; }
</style>
