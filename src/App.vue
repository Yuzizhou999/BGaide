<script>
export default {
  onLaunch() {
    // 恢复主题设置
    const theme = uni.getStorageSync('bgaide_theme') || 'light'
    this.globalData.theme = theme

    // #ifdef MP-WEIXIN
    this.initWeChatCloud()
    // #endif
  },
  methods: {
    // 微信云开发初始化（AI 扩展能力依赖此初始化）
    initWeChatCloud() {
      if (typeof wx === 'undefined' || !wx.cloud) {
        console.warn('wx.cloud 不可用，请确认在微信小程序环境运行')
        return
      }
      try {
        wx.cloud.init({
          traceUser: true
        })
      } catch (error) {
        console.error('wx.cloud.init 失败:', error)
      }
    }
  },
  globalData: {
    theme: 'light'
  }
}
</script>

<style lang="scss">
/* ===== 全局 CSS 变量 (深浅色主题) ===== */
page {
  --color-bg-primary: #f5f5f7;
  --color-bg-secondary: #ffffff;
  --color-bg-card: #ffffff;
  --color-bg-overlay: rgba(0, 0, 0, 0.5);
  --color-text-primary: #1a1a2e;
  --color-text-secondary: #6b7280;
  --color-text-tertiary: #9ca3af;
  --color-accent: #6c5ce7;
  --color-accent-light: #a29bfe;
  --color-accent-bg: rgba(108, 92, 231, 0.08);
  --color-success: #00b894;
  --color-warning: #fdcb6e;
  --color-danger: #e17055;
  --color-border: #e5e7eb;
  --color-divider: #f0f0f3;
  --shadow-sm: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4rpx 16rpx rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8rpx 32rpx rgba(0, 0, 0, 0.12);
  --radius-sm: 12rpx;
  --radius-md: 20rpx;
  --radius-lg: 28rpx;
  --radius-full: 999rpx;
  font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-size: 28rpx;
  color: var(--color-text-primary);
  background-color: var(--color-bg-primary);
  line-height: 1.6;
}

/* 暗色主题 */
page[data-theme="dark"] {
  --color-bg-primary: #0f0f1a;
  --color-bg-secondary: #1a1a2e;
  --color-bg-card: #222240;
  --color-bg-overlay: rgba(0, 0, 0, 0.7);
  --color-text-primary: #eaeaef;
  --color-text-secondary: #9ca3af;
  --color-text-tertiary: #6b7280;
  --color-accent: #a29bfe;
  --color-accent-light: #6c5ce7;
  --color-accent-bg: rgba(162, 155, 254, 0.12);
  --color-border: #2d2d4a;
  --color-divider: #252545;
  --shadow-sm: 0 2rpx 8rpx rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4rpx 16rpx rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 8rpx 32rpx rgba(0, 0, 0, 0.4);
}

/* ===== 全局基础样式 ===== */
view,
text {
  box-sizing: border-box;
}

.page-container {
  min-height: 100vh;
  padding-bottom: env(safe-area-inset-bottom);
  background-color: var(--color-bg-primary);
}

.section-title {
  font-size: 36rpx;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 24rpx;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 4rpx 16rpx;
  border-radius: var(--radius-full);
  font-size: 22rpx;
  font-weight: 500;
}

.badge-accent {
  background-color: var(--color-accent-bg);
  color: var(--color-accent);
}

.badge-success {
  background-color: rgba(0, 184, 148, 0.1);
  color: var(--color-success);
}

.badge-warning {
  background-color: rgba(253, 203, 110, 0.15);
  color: #e17055;
}
</style>
