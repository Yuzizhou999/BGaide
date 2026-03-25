<template>
  <view class="game-card" @tap="goDetail">
    <view class="card-cover">
      <LazyImage
        class="cover-img"
        :src="game.thumb || '/static/icons/placeholder.svg'"
        mode="aspectFill"
        :preload="480"
      />
      <view v-if="game.hot" class="hot-badge">🔥 热门</view>
    </view>
    <view class="card-body">
      <text class="card-title">{{ game.name }}</text>
      <text class="card-subtitle">{{ game.nameEn }}</text>
      <view class="card-meta">
        <view class="meta-item">
          <text class="meta-icon">👥</text>
          <text class="meta-text">{{ game.players[0] }}-{{ game.players[1] }}人</text>
        </view>
        <view class="meta-item">
          <text class="meta-icon">⏱️</text>
          <text class="meta-text">{{ game.duration[0] }}-{{ game.duration[1] }}分钟</text>
        </view>
        <view class="meta-item bgg-score">
          <text class="meta-icon">⭐</text>
          <text class="meta-text">{{ game.bggScore }}</text>
        </view>
      </view>
      <view class="card-tags">
        <text class="difficulty-badge" :class="difficultyClass">{{ game.difficulty }}</text>
        <text v-for="tag in game.tags.slice(0, 3)" :key="tag" class="tag-item">{{ tag }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import LazyImage from '@/components/LazyImage.vue'

const props = defineProps({
  game: { type: Object, required: true }
})

const difficultyClass = computed(() => {
  const map = { '简单': 'badge-success', '中等': 'badge-accent', '困难': 'badge-warning' }
  return map[props.game.difficulty] || ''
})

function goDetail() {
  uni.navigateTo({
    url: `/pages/game-detail/index?id=${props.game.id}`
  })
}
</script>

<style lang="scss" scoped>
.game-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:active {
    transform: scale(0.98);
    box-shadow: var(--shadow-md);
  }
}

.card-cover {
  position: relative;
  width: 100%;
  height: 280rpx;
  overflow: hidden;
}

.cover-img {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.hot-badge {
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  padding: 6rpx 18rpx;
  border-radius: var(--radius-full);
  background: rgba(225, 112, 85, 0.9);
  color: #fff;
  font-size: 22rpx;
  font-weight: 600;
  backdrop-filter: blur(8px);
}

.card-body {
  padding: 20rpx 24rpx 24rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: var(--color-text-primary);
  display: block;
  line-height: 1.3;
}

.card-subtitle {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  margin-top: 4rpx;
  display: block;
}

.card-meta {
  display: flex;
  align-items: center;
  margin-top: 16rpx;
  gap: 20rpx;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4rpx;
}

.meta-icon {
  font-size: 24rpx;
}

.meta-text {
  font-size: 24rpx;
  color: var(--color-text-secondary);
}

.bgg-score .meta-text {
  font-weight: 700;
  color: var(--color-accent);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 14rpx;
}

.difficulty-badge {
  display: inline-block;
  padding: 4rpx 16rpx;
  border-radius: var(--radius-full);
  font-size: 22rpx;
  font-weight: 600;
}

.badge-success {
  background: rgba(0, 184, 148, 0.1);
  color: #00b894;
}

.badge-accent {
  background: var(--color-accent-bg);
  color: var(--color-accent);
}

.badge-warning {
  background: rgba(253, 203, 110, 0.15);
  color: #e17055;
}

.tag-item {
  display: inline-block;
  padding: 4rpx 14rpx;
  border-radius: var(--radius-full);
  font-size: 22rpx;
  color: var(--color-text-tertiary);
  background: var(--color-bg-primary);
}
</style>
