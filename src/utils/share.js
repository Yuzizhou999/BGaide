/**
 * 微信官方分享辅助工具
 */

export function enableWeChatOfficialShare() {
    try {
        uni.showShareMenu({
            withShareTicket: true,
            menus: ['shareAppMessage', 'shareTimeline']
        })
    } catch (error) {
        console.warn('showShareMenu failed:', error)
    }
}

export function buildPageSharePayload({ title = '', path = '', imageUrl = '', query }) {
    const sharePath = query ? `${path}?${query}` : path

    return {
        title,
        path: sharePath,
        imageUrl
    }
}

export function buildTimelineSharePayload({ title = '', query = '', imageUrl = '' }) {
    return {
        title,
        query,
        imageUrl
    }
}

export function buildShareImages(primaryImage, fallbackImage = '') {
    return primaryImage || fallbackImage || '/static/icons/placeholder.svg'
}
