/**
 * 系统信息兼容工具：优先使用新版接口，旧版本再兜底。
 */

export function getWindowInfoSafe() {
    try {
        if (typeof uni.getWindowInfo === 'function') {
            const info = uni.getWindowInfo()
            if (info && typeof info === 'object') {
                return info
            }
        }
    } catch (error) {
        // ignore
    }

    try {
        if (typeof uni.getSystemInfoSync === 'function') {
            return uni.getSystemInfoSync() || {}
        }
    } catch (error) {
        // ignore
    }

    return {}
}

export function getStatusBarHeight(defaultValue = 44) {
    const value = Number(getWindowInfoSafe().statusBarHeight)
    return Number.isFinite(value) && value > 0 ? value : defaultValue
}

export function getWindowWidth(defaultValue = 375) {
    const value = Number(getWindowInfoSafe().windowWidth)
    return Number.isFinite(value) && value > 0 ? value : defaultValue
}

export function getWindowHeight(defaultValue = 667) {
    const value = Number(getWindowInfoSafe().windowHeight)
    return Number.isFinite(value) && value > 0 ? value : defaultValue
}

export function getPixelRatio(defaultValue = 1) {
    const value = Number(getWindowInfoSafe().pixelRatio)
    return Number.isFinite(value) && value > 0 ? value : defaultValue
}
