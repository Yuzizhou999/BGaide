/**
 * 主题工具（仅暗色模式）
 */

const TAB_BAR_PAGES = new Set([
    'pages/recommend/index',
    'pages/home/index',
    'pages/tools/index',
    'pages/profile/index'
])

function isTabBarPage() {
    try {
        const pages = getCurrentPages()
        const current = pages[pages.length - 1]
        const route = current?.route || ''
        return TAB_BAR_PAGES.has(route)
    } catch {
        return false
    }
}

export function applyTheme() {
    // 设置导航栏颜色（暗色）
    uni.setNavigationBarColor({
        frontColor: '#ffffff',
        backgroundColor: '#0f0f1a',
        animation: { duration: 300, timingFunc: 'easeIn' }
    })

    // 仅 TabBar 页面设置样式，避免在非 TabBar 页面报错
    if (isTabBarPage()) {
        uni.setTabBarStyle({
            color: '#6b7280',
            selectedColor: '#a29bfe',
            backgroundColor: '#1a1a2e',
            borderStyle: 'black',
            fail: () => {}
        })
    }
}

// 保留 getTheme 供已有调用兼容，始终返回 dark
export function getTheme() {
    return 'dark'
}
