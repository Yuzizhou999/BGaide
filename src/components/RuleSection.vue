<template>
  <view class="rule-section" :class="{ expanded }">
    <view class="section-header" @tap="expanded = !expanded">
      <view class="section-step">
        <text class="step-number">{{ stepNumber }}</text>
      </view>
      <view class="section-info">
        <text class="section-title">{{ title }}</text>
        <text class="section-hint">{{ hint }}</text>
      </view>
      <view class="section-arrow" :class="{ rotated: expanded }">
        <text>▼</text>
      </view>
    </view>
    <view class="section-content" v-if="expanded">
      <!-- 列表项模式 -->
      <view v-if="items && items.length" class="content-list">
        <view v-for="(item, idx) in items" :key="idx" class="content-item">
          <text class="item-bullet">{{ listStyle === 'number' ? (idx + 1) + '.' : '•' }}</text>
          <text class="item-text">{{ item }}</text>
        </view>
      </view>
      <!-- 纯文本模式 -->
      <view v-else-if="text" class="content-text">
        <text>{{ text }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  stepNumber: { type: [String, Number], default: '1' },
  title: { type: String, required: true },
  hint: { type: String, default: '' },
  items: { type: Array, default: () => [] },
  text: { type: String, default: '' },
  listStyle: { type: String, default: 'bullet' },
  defaultExpanded: { type: Boolean, default: false }
})

const expanded = ref(false)
</script>

<style lang="scss" scoped>
.rule-section {
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  margin-bottom: 16rpx;
  overflow: hidden;
  border: 2rpx solid var(--color-border);
  transition: border-color 0.3s ease;

  &.expanded {
    border-color: var(--color-accent);
  }
}

.section-header {
  display: flex;
  align-items: center;
  padding: 24rpx;
  gap: 20rpx;
}

.section-step {
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-accent), var(--color-accent-light));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-number {
  color: #fff;
  font-size: 28rpx;
  font-weight: 700;
}

.section-info {
  flex: 1;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: var(--color-text-primary);
  display: block;
}

.section-hint {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  margin-top: 4rpx;
  display: block;
}

.section-arrow {
  font-size: 20rpx;
  color: var(--color-text-tertiary);
  transition: transform 0.3s ease;
  flex-shrink: 0;

  &.rotated {
    transform: rotate(180deg);
  }
}

.section-content {
  padding: 0 24rpx 24rpx;
  animation: slideDown 0.3s ease;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10rpx);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-list {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
}

.content-item {
  display: flex;
  gap: 12rpx;
  align-items: flex-start;
}

.item-bullet {
  color: var(--color-accent);
  font-weight: 600;
  flex-shrink: 0;
  min-width: 36rpx;
}

.item-text {
  font-size: 28rpx;
  color: var(--color-text-secondary);
  line-height: 1.7;
}

.content-text {
  font-size: 28rpx;
  color: var(--color-text-secondary);
  line-height: 1.8;
}
</style>
