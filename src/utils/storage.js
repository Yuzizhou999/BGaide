/**
 * 本地缓存封装
 */
export function getStorage(key, defaultValue = null) {
    try {
        const val = uni.getStorageSync(key)
        return val ? JSON.parse(val) : defaultValue
    } catch (e) {
        return defaultValue
    }
}

export function setStorage(key, value) {
    try {
        uni.setStorageSync(key, JSON.stringify(value))
    } catch (e) {
        console.warn('setStorage error:', key, e)
    }
}

export function removeStorage(key) {
    try {
        uni.removeStorageSync(key)
    } catch (e) {
        console.warn('removeStorage error:', key, e)
    }
}
