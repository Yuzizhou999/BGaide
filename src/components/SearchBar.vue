<template>
  <view class="search-bar" :class="{ focused: isFocused }">
    <view class="search-icon">🔍</view>
    <input
      class="search-input"
      type="text"
      :value="modelValue"
      :placeholder="placeholder"
      placeholder-class="search-placeholder"
      confirm-type="search"
      @input="onInput"
      @focus="isFocused = true"
      @blur="isFocused = false"
      @confirm="$emit('search', modelValue)"
    />
    <view v-if="modelValue" class="search-clear" @tap="onClear">✕</view>
  </view>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '搜索桌游名称、英文名、别名...' }
})

const emit = defineEmits(['update:modelValue', 'search'])
const isFocused = ref(false)

let timer = null
function onInput(e) {
  const val = e.detail.value
  emit('update:modelValue', val)
  // 防抖 300ms
  clearTimeout(timer)
  timer = setTimeout(() => {
    emit('search', val)
  }, 300)
}

function onClear() {
  emit('update:modelValue', '')
  emit('search', '')
}
</script>

<style lang="scss" scoped>
.search-bar {
  display: flex;
  align-items: center;
  padding: 0 24rpx;
  height: 80rpx;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 2rpx solid var(--color-border);
  transition: all 0.3s ease;

  &.focused {
    border-color: var(--color-accent);
    box-shadow: 0 0 0 4rpx var(--color-accent-bg);
  }
}

.search-icon {
  font-size: 32rpx;
  margin-right: 16rpx;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  font-size: 28rpx;
  color: var(--color-text-primary);
  background: transparent;
}

.search-placeholder {
  color: var(--color-text-tertiary);
}

.search-clear {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  padding: 8rpx 12rpx;
  margin-left: 8rpx;
  flex-shrink: 0;
}
</style>
