/**
 * API 请求工具
 * 封装 uni.request，统一处理 baseURL、错误等
 */

// 后端 API 基础地址（开发环境用本地，生产环境改为你的域名）
const BASE_URL = 'http://localhost:8000'

/**
 * 发起 GET 请求
 * @param {string} path - API 路径，例如 '/api/games'
 * @param {object} params - 查询参数，例如 { keyword: '卡坦', page: 1 }
 * @returns {Promise<any>} 响应数据
 */
export function get(path, params = {}) {
    // 过滤掉 null/undefined 的参数
    const query = {}
    for (const [key, value] of Object.entries(params)) {
        if (value !== null && value !== undefined && value !== '') {
            query[key] = value
        }
    }

    return new Promise((resolve, reject) => {
        uni.request({
            url: `${BASE_URL}${path}`,
            method: 'GET',
            data: query,
            success: (res) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(res.data)
                } else {
                    console.warn(`API Error [${res.statusCode}]:`, res.data)
                    reject(new Error(res.data?.detail || `请求失败 (${res.statusCode})`))
                }
            },
            fail: (err) => {
                console.error('Network Error:', err)
                reject(new Error('网络连接失败，请检查网络'))
            }
        })
    })
}

/**
 * 发起 POST 请求
 * @param {string} path - API 路径
 * @param {object} data - 请求体
 * @returns {Promise<any>} 响应数据
 */
export function post(path, data = {}) {
    return new Promise((resolve, reject) => {
        uni.request({
            url: `${BASE_URL}${path}`,
            method: 'POST',
            header: { 'Content-Type': 'application/json' },
            data,
            success: (res) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    resolve(res.data)
                } else {
                    reject(new Error(res.data?.detail || `请求失败 (${res.statusCode})`))
                }
            },
            fail: (err) => {
                reject(new Error('网络连接失败，请检查网络'))
            }
        })
    })
}
