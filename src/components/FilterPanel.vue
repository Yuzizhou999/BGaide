<template>
  <view class="filter-mask" v-if="visible" @tap="$emit('close')" />
  <view class="filter-panel" :class="{ show: visible }">
    <view class="filter-header">
      <text class="filter-title">筛选条件</text>
      <text class="filter-reset" @tap="onReset">重置</text>
    </view>

    <!-- 游玩人数 -->
    <view class="filter-section">
      <text class="filter-label">游玩人数</text>
      <view class="filter-tags">
        <view v-for="n in playerOptions" :key="n" class="filter-tag" :class="{ active: selectedPlayers === n }"
          @tap="selectPlayers(n)">
          {{ n }}人
        </view>
      </view>
    </view>

    <!-- 游戏时长 -->
    <view class="filter-section">
      <text class="filter-label">游戏时长</text>
      <view class="filter-tags">
        <view v-for="d in durationOptions" :key="d.label" class="filter-tag" :class="{ active: isDurationActive(d) }"
          @tap="selectDuration(d)">
          {{ d.label }}
        </view>
      </view>
    </view>

    <!-- 难度 -->
    <view class="filter-section">
      <text class="filter-label">难度</text>
      <view class="filter-tags">
        <view v-for="lv in difficultyOptions" :key="lv" class="filter-tag"
          :class="{ active: selectedDifficulty === lv }" @tap="selectDifficulty(lv)">
          {{ lv }}
        </view>
      </view>
    </view>

    <!-- 确认 -->
    <view class="filter-confirm" @tap="onConfirm">
      <text>确认筛选</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  visible: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'filter'])

const playerOptions = [1, 2, 3, 4, 5, 6, 7]
const durationOptions = [
  { label: '30分钟内', range: [0, 30] },
  { label: '30-60分钟', range: [30, 60] },
  { label: '1-2小时', range: [60, 120] },
  { label: '2小时以上', range: [120, 999] }
]
const difficultyOptions = ['简单', '中等', '困难']

const selectedPlayers = ref(null)
const selectedDurationLabel = ref(null)
const selectedDifficulty = ref(null)

function selectPlayers(n) {
  selectedPlayers.value = selectedPlayers.value === n ? null : n
}

function selectDuration(d) {
  selectedDurationLabel.value = selectedDurationLabel.value === d.label ? null : d.label
}

function isDurationActive(d) {
  return selectedDurationLabel.value === d.label
}

function selectDifficulty(lv) {
  selectedDifficulty.value = selectedDifficulty.value === lv ? null : lv
}

function onReset() {
  selectedPlayers.value = null
  selectedDurationLabel.value = null
  selectedDifficulty.value = null
  emit('filter', { playerCount: null, duration: null, difficulty: null })
}

function onConfirm() {
  const selectedDuration = durationOptions.find(d => d.label === selectedDurationLabel.value)
  emit('filter', {
    playerCount: selectedPlayers.value,
    duration: selectedDuration ? selectedDuration.range : null,
    difficulty: selectedDifficulty.value
  })
  emit('close')
}
</script>

<style lang="scss" scoped>
.filter-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--color-bg-overlay);
  z-index: 1000;
}

.filter-panel {
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

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;
}

.filter-title {
  font-size: 34rpx;
  font-weight: 700;
  color: var(--color-text-primary);
}

.filter-reset {
  font-size: 26rpx;
  color: var(--color-accent);
}

.filter-section {
  margin-bottom: 32rpx;
}

.filter-label {
  font-size: 26rpx;
  color: var(--color-text-secondary);
  margin-bottom: 16rpx;
  display: block;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.filter-tag {
  padding: 12rpx 28rpx;
  border-radius: var(--radius-full);
  font-size: 26rpx;
  color: var(--color-text-secondary);
  background: var(--color-bg-primary);
  border: 2rpx solid var(--color-border);
  transition: all 0.2s ease;

  &.active {
    background: var(--color-accent-bg);
    color: var(--color-accent);
    border-color: var(--color-accent);
    font-weight: 600;
  }
}

.filter-confirm {
  margin-top: 16rpx;
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
