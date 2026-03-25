import sys

with open(r'e:\project\BGaide\src\pages\tools-punishment\index.vue', 'r', encoding='utf-8') as f:
    code = f.read()

template_start = code.find('<template>')
template_end = code.find('</template>') + len('</template>')

new_template = """<template>
  <view class="page-container punish-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>
    <view class="bg-orb orb-c"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack">
          <text class="back-icon"> 返回</text>
        </view>
        <text class="nav-title">趣味挑战</text>
        <view class="nav-placeholder"></view>
      </view>
    </view>

    <view class="punish-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      
      <!-- 顶部趣味提示 -->
      <view class="hero-card">
        <text class="hero-icon"></text>
        <view class="hero-text">
          <text class="hero-title">为气氛加点料</text>
          <text class="hero-desc">破冰局可拒绝可替代，熟人局别说玩不起~</text>
        </view>
      </view>

      <!-- 选项过滤区 -->
      <view class="filter-card">
        <view class="filter-header">
          <text class="filter-title">参数配置</text>
          <view class="social-switch" @tap="enableSocialMode">
            <text class="switch-label">社恐友好</text>
            <view class="switch-ui" :class="{ 'is-on': socialFriendlyOnly }">
              <view class="switch-knob"></view>
            </view>
          </view>
        </view>

        <view class="filter-group">
          <text class="group-label">挑战强度</text>
          <view class="chip-row">
            <view
              v-for="lv in levels"
              :key="lv.value"
              class="chip-item"
              :class="{ active: selectedLevel === lv.value }"
              @tap="selectLevel(lv.value)"
            >
              {{ lv.label }}
            </view>
          </view>
        </view>

        <view class="filter-group" style="margin-top: 28rpx;">
          <text class="group-label">聚会场景</text>
          <view class="chip-row">
            <view
              v-for="sc in scenes"
              :key="sc"
              class="chip-item scene"
              :class="{ active: selectedScene === sc }"
              @tap="selectScene(sc)"
            >
              {{ sc }}
            </view>
          </view>
        </view>
      </view>

      <!-- 结果展示区 -->
      <view class="result-area">
        <text class="quote-mark left"></text>
        <text class="quote-mark right"></text>
        <view class="result-content" :class="{ empty: !currentPunishment }">
          <text v-if="!currentPunishment">还没准备好？点击下方抽取</text>
          <text v-else class="result-text">{{ currentPunishment }}</text>
        </view>
        <view class="result-tags" v-if="currentMeta">
          <text class="res-tag">{{ levelText(currentMeta.level) }}</text>
          <text class="res-tag">{{ currentMeta.scene }}</text>
          <text class="res-tag">{{ currentMeta.source === 'custom' ? '自定义' : '预置' }}</text>
        </view>
      </view>

      <!-- 底部动作区 -->
      <view class="action-dock">
        <view class="btn-main" @tap="drawOne">
          <text class="btn-main-txt">{{ currentPunishment ? '换一个' : '立刻抽取挑战' }}</text>
        </view>
        
        <view class="btn-sub-row" v-if="currentPunishment">
          <view class="btn-sub secondary" @tap="redrawOne">太社死，重抽</view>
          <view class="btn-sub primary" @tap="markDone">我做完了</view>
        </view>
      </view>

    </view>
  </view>
</template>"""

code = code[:template_start] + new_template + code[template_end:]

script_str_to_remove = """function enableTabletopMode() {
  selectedLevel.value = 'tabletop'
  toolsStore.setPunishmentLevel('tabletop')
}

"""
code = code.replace(script_str_to_remove, "")

style_start = code.find('<style')
style_end = code.find('</style>') + len('</style>')

new_style = """<style lang="scss" scoped>
.punish-page {
  position: relative;
  overflow: hidden;
  padding-bottom: 60rpx;
  min-height: 100vh;
  background-color: var(--color-bg-primary);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(40rpx);
  pointer-events: none;
  z-index: 0;
}

.orb-a {
  width: 450rpx;
  height: 450rpx;
  top: -100rpx;
  left: -150rpx;
  background: radial-gradient(circle, rgba(255, 159, 67, 0.15), rgba(255, 159, 67, 0));
}

.orb-b {
  width: 350rpx;
  height: 350rpx;
  top: 300rpx;
  right: -100rpx;
  background: radial-gradient(circle, rgba(238, 82, 83, 0.12), rgba(238, 82, 83, 0));
}

.orb-c {
  width: 400rpx;
  height: 400rpx;
  bottom: 0;
  left: 0;
  background: radial-gradient(circle, rgba(254, 202, 87, 0.12), rgba(254, 202, 87, 0));
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(28px);
}

.nav-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 88rpx;
  padding: 0 32rpx;
}

.nav-back, .nav-placeholder {
  width: 140rpx;
}

.back-icon {
  font-size: 26rpx;
  color: var(--color-text-secondary);
  font-weight: 600;
  padding: 10rpx 24rpx;
  background: rgba(0, 0, 0, 0.05);
  border-radius: var(--radius-full);
}

.nav-title {
  flex: 1;
  text-align: center;
  font-size: 32rpx;
  font-weight: 800;
  color: var(--color-text-primary);
  letter-spacing: 2rpx;
}

.punish-body {
  position: relative;
  z-index: 2;
  padding: 30rpx 32rpx;
  display: flex;
  flex-direction: column;
  gap: 30rpx;
}

/* 顶部卡片 */
.hero-card {
  display: flex;
  align-items: center;
  gap: 20rpx;
  padding: 24rpx 28rpx;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, rgba(255, 159, 67, 0.12), rgba(238, 82, 83, 0.06));
  border: 4rpx solid rgba(255, 159, 67, 0.15);
}

.hero-icon {
  font-size: 64rpx;
  line-height: 1;
}

.hero-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.hero-title {
  font-size: 30rpx;
  font-weight: 800;
  color: #c0392b;
}

.hero-desc {
  font-size: 24rpx;
  color: #d35400;
  line-height: 1.4;
}

/* 过滤区域 */
.filter-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  border-radius: var(--radius-lg);
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.04);
  border: 1rpx solid rgba(255, 255, 255, 0.6);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
  padding-bottom: 20rpx;
  border-bottom: 2rpx dashed var(--color-divider);
}

.filter-title {
  font-size: 28rpx;
  font-weight: 800;
  color: var(--color-text-primary);
}

.social-switch {
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.switch-label {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  font-weight: 600;
}

.switch-ui {
  width: 76rpx;
  height: 44rpx;
  border-radius: 44rpx;
  background: var(--color-border);
  position: relative;
  transition: all 0.3s ease;

  &.is-on {
    background: #00b894;
    .switch-knob {
      transform: translateX(32rpx);
    }
  }
}

.switch-knob {
  width: 36rpx;
  height: 36rpx;
  background: #fff;
  border-radius: 50%;
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4rpx 8rpx rgba(0,0,0,0.1);
}

.group-label {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  margin-bottom: 16rpx;
  display: block;
  font-weight: 600;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.chip-item {
  padding: 12rpx 28rpx;
  border-radius: 14rpx;
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  font-size: 24rpx;
  border: 2rpx solid transparent;
  transition: all 0.2s ease;

  &.active {
    background: rgba(225, 112, 85, 0.08);
    color: #e17055;
    border-color: rgba(225, 112, 85, 0.4);
    font-weight: 700;
  }
  
  &.scene {
    border-radius: var(--radius-full);
    padding: 10rpx 24rpx;
    font-size: 24rpx;
    &.active {
       background: rgba(9, 132, 227, 0.08);
       color: #0984e3;
       border-color: rgba(9, 132, 227, 0.3);
    }
  }
}

/* 结果展示卡片 */
.result-area {
  position: relative;
  background: linear-gradient(160deg, #ffffff, #fffdf8);
  border-radius: var(--radius-lg);
  padding: 70rpx 40rpx;
  min-height: 280rpx;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 20rpx 40rpx rgba(225, 112, 85, 0.06);
  border: 4rpx solid #ffeaa7;
}

.quote-mark {
  position: absolute;
  font-size: 140rpx;
  color: rgba(253, 203, 110, 0.15);
  font-family: serif;
  font-weight: 900;
  line-height: 1;

  &.left {
    top: 10rpx;
    left: 20rpx;
  }

  &.right {
    bottom: -50rpx;
    right: 20rpx;
  }
}

.result-content {
  text-align: center;
  z-index: 1;
  width: 100%;

  &.empty {
    color: var(--color-text-tertiary);
    font-size: 28rpx;
    font-weight: 600;
  }
}

.result-text {
  font-size: 40rpx;
  color: #2d3436;
  font-weight: 900;
  line-height: 1.5;
  letter-spacing: 2rpx;
}

.result-tags {
  margin-top: 36rpx;
  display: flex;
  gap: 16rpx;
  justify-content: center;
  z-index: 1;
}

.res-tag {
  padding: 8rpx 20rpx;
  background: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  font-size: 22rpx;
  border-radius: var(--radius-sm);
  font-weight: 700;
}

/* 底部动作 */
.action-dock {
  margin-top: 10rpx;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.btn-main {
  width: 100%;
  height: 100rpx;
  border-radius: 50rpx;
  background: linear-gradient(135deg, #ff7675, #fab1a0);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 16rpx 32rpx rgba(255, 118, 117, 0.35);
  transition: transform 0.1s;
  
  &:active {
    transform: scale(0.98);
  }
}

.btn-main-txt {
  color: #fff;
  font-size: 34rpx;
  font-weight: 800;
  letter-spacing: 4rpx;
}

.btn-sub-row {
  display: flex;
  gap: 24rpx;
}

.btn-sub {
  flex: 1;
  height: 88rpx;
  border-radius: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28rpx;
  font-weight: 800;
  transition: transform 0.1s;
  
  &:active {
    transform: scale(0.98);
  }

  &.secondary {
    background: var(--color-bg-card);
    color: var(--color-text-secondary);
    border: 3rpx solid var(--color-border);
    box-shadow: 0 8rpx 16rpx rgba(0,0,0,0.03);
  }

  &.primary {
    background: #00cec9;
    color: #fff;
    box-shadow: 0 12rpx 24rpx rgba(0, 206, 201, 0.25);
  }
}
</style>"""

code = code[:style_start] + new_style

with open(r'e:\project\BGaide\src\pages\tools-punishment\index.vue', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patch applied successfully.")
