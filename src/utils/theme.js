/**
 * 主题工具（仅暗色模式）
 */

export function applyTheme() {
    // 设置导航栏颜色（暗色）
    uni.setNavigationBarColor({
        frontColor: '#ffffff',
        backgroundColor: '#0f0f1a',
        animation: { duration: 300, timingFunc: 'easeIn' }
    })

    // 设置 TabBar 样式（暗色）
    uni.setTabBarStyle({
        color: '#6b7280',
        selectedColor: '#a29bfe',
        backgroundColor: '#1a1a2e',
        borderStyle: 'black'
    })
}

// 保留 getTheme 供已有调用兼容，始终返回 dark
export function getTheme() {
    return 'dark'
}
