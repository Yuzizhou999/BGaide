<template>
  <view class="faq-item" :class="{ expanded }" @tap="expanded = !expanded">
    <view class="faq-header">
      <view class="faq-badge">Q</view>
      <text class="faq-question">{{ item.q }}</text>
      <view class="faq-arrow" :class="{ rotated: expanded }">
        <text>▼</text>
      </view>
    </view>
    <view v-if="expanded" class="faq-answer">
      <view class="faq-answer-badge">A</view>
      <text class="faq-answer-text">{{ item.a }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  item: { type: Object, required: true }
})

const expanded = ref(false)
</script>

<style lang="scss" scoped>
.faq-item {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  margin-bottom: 12rpx;
  overflow: hidden;
  border: 2rpx solid var(--color-border);
  transition: all 0.2s ease;

  &.expanded {
    border-color: var(--color-accent);
  }
}

.faq-header {
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  gap: 16rpx;
}

.faq-badge {
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 700;
  flex-shrink: 0;
  background: var(--color-accent-bg);
  color: var(--color-accent);
}

.faq-question {
  flex: 1;
  font-size: 28rpx;
  font-weight: 500;
  color: var(--color-text-primary);
  line-height: 1.5;
}

.faq-arrow {
  font-size: 18rpx;
  color: var(--color-text-tertiary);
  transition: transform 0.3s ease;
  flex-shrink: 0;

  &.rotated {
    transform: rotate(180deg);
  }
}

.faq-answer {
  display: flex;
  gap: 16rpx;
  padding: 0 24rpx 20rpx;
  animation: slideDown 0.3s ease;
}

.faq-answer-badge {
  width: 44rpx;
  height: 44rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  font-weight: 700;
  flex-shrink: 0;
  background: rgba(0, 184, 148, 0.1);
  color: var(--color-success);
}

.faq-answer-text {
  flex: 1;
  font-size: 28rpx;
  color: var(--color-text-secondary);
  line-height: 1.8;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
