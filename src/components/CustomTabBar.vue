<template>
    <view class="custom-tabbar" :style="{ background: bgColor }">
        <view v-for="(item, index) in tabs" :key="item.path" class="tab-item" :class="{ active: current === index }"
            @click="switchTab(index)">
            <view class="tab-icon-wrap" :class="{ active: current === index }">
                <text class="tab-icon">{{ current === index ? item.activeIcon : item.icon }}</text>
            </view>
            <text class="tab-label" :class="{ active: current === index }">{{ item.text }}</text>
            <view v-if="current === index" class="tab-indicator" />
        </view>
    </view>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    current: { type: Number, default: 0 }
})

const tabs = [
    { path: '/pages/recommend/index', text: '推荐', icon: '🌟', activeIcon: '✨' },
    { path: '/pages/home/index', text: '探索', icon: '🔍', activeIcon: '🔎' },
    { path: '/pages/tools/index', text: '工具', icon: '🧰', activeIcon: '🛠️' },
    { path: '/pages/profile/index', text: '我的', icon: '👤', activeIcon: '😊' }
]

const bgColor = computed(() => {
    return 'var(--color-bg-secondary)'
})

function switchTab(index) {
    if (props.current === index) return
    uni.switchTab({
        url: tabs[index].path,
        fail: (err) => {
            console.error('switchTab fail:', err)
            uni.reLaunch({ url: tabs[index].path })
        }
    })
}
</script>

<style lang="scss" scoped>
.custom-tabbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-around;
    height: calc(110rpx + env(safe-area-inset-bottom));
    padding-bottom: env(safe-area-inset-bottom);
    border-top: 1rpx solid var(--color-divider);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
}

.tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rpx;
    position: relative;
    padding: 8rpx 0;
    transition: all 0.25s ease;

    &:active {
        transform: scale(0.92);
    }
}

.tab-icon-wrap {
    width: 64rpx;
    height: 64rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

    &.active {
        background: var(--color-accent-bg);
        transform: scale(1.15);
    }
}

.tab-icon {
    font-size: 40rpx;
    transition: all 0.25s ease;
}

.tab-label {
    font-size: 24rpx;
    color: var(--color-text-tertiary);
    font-weight: 400;
    transition: all 0.25s ease;
    margin-top: 2rpx;

    &.active {
        color: var(--color-accent);
        font-weight: 600;
        font-size: 24rpx;
    }
}

.tab-indicator {
    position: absolute;
    bottom: 4rpx;
    width: 36rpx;
    height: 6rpx;
    border-radius: 6rpx;
    background: var(--color-accent);
    animation: indicatorIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes indicatorIn {
    0% {
        width: 0;
        opacity: 0;
    }

    100% {
        width: 36rpx;
        opacity: 1;
    }
}
</style>
