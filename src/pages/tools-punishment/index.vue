<template>
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
        <text class="hero-icon">👿</text>
        <view class="hero-text">
          <text class="hero-title">为气氛加点料</text>
          <text class="hero-desc">输掉本局游戏的玩家需要抽取下方趣味挑战，而获胜者则可以直接跳过下次挑战！破冰局默认可拒绝可替代，熟人局我说你是不是玩不起~</text>
        </view>
      </view>

      <!-- 选项过滤区 -->
      <view class="filter-card">
        <view class="filter-header">
          <text class="filter-title">参数配置</text>
          <view class="social-switch" @tap="enableSocialMode">
            <text class="switch-label">社恐友好</text>
            <text class="switch-state" :class="{ on: socialFriendlyOnly }">{{ socialFriendlyOnly ? '开' : '关' }}</text>
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
          <text v-if="!currentPunishment">还没有抽中台词，点击下方按钮让气氛升温</text>
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
          <text class="btn-main-txt">{{ currentPunishment ? '🎲 换一个' : '🎲 立刻抽取' }}</text>
        </view>

        <view class="btn-sub-row">
          <view class="btn-sub secondary" :class="{ disabled: !currentPunishment }" @tap="playRedrawFx">太社死，重抽</view>
          <view class="btn-sub primary" :class="{ disabled: !currentPunishment }" @tap="playDoneFx">我做完了</view>
        </view>
      </view>

      <view v-if="effectVisible" class="fx-screen" :class="effectType" @tap="finishFxNow">
        <view class="fx-flash" :class="effectType"></view>

        <view v-if="effectType === 'redraw'" class="fx-poo-stage" aria-hidden="true">
          <view class="fx-splat s1"></view>
          <view class="fx-splat s2"></view>
          <view class="fx-splat s3"></view>
          <view class="fx-splat s4"></view>
          <text class="fx-poo p1">💩</text>
          <text class="fx-poo p2">💩</text>
          <text class="fx-poo p3">💩</text>
          <text class="fx-poo p4">💩</text>
          <text class="fx-poo p5">💩</text>
          <text class="fx-poo p6">💩</text>
          <text class="fx-poo p7">💩</text>
          <text class="fx-poo p8">💩</text>
          <text class="fx-poo p9">💩</text>
          <text class="fx-poo p10">💩</text>
          <text class="fx-poo p11">💩</text>
          <text class="fx-poo p12">💩</text>
        </view>

        <view v-if="effectType === 'done'" class="fx-fire-stage" aria-hidden="true">
          <view class="fx-spark s1"></view>
          <view class="fx-spark s2"></view>
          <view class="fx-spark s3"></view>
          <view class="fx-spark s4"></view>
          <view class="fx-spark s5"></view>
          <view class="fx-spark s6"></view>
          <view class="fx-spark s7"></view>
          <view class="fx-spark s8"></view>
          <view class="fx-spark s9"></view>
          <view class="fx-spark s10"></view>
          <view class="fx-spark s11"></view>
          <view class="fx-spark s12"></view>
          <view class="fx-spark s13"></view>
          <view class="fx-spark s14"></view>
          <view class="fx-spark s15"></view>
          <view class="fx-spark s16"></view>
          <view class="fx-spark s17"></view>
          <view class="fx-spark s18"></view>
          <view class="fx-confetti c1"></view>
          <view class="fx-confetti c2"></view>
          <view class="fx-confetti c3"></view>
          <view class="fx-confetti c4"></view>
          <view class="fx-confetti c5"></view>
          <view class="fx-confetti c6"></view>
          <view class="fx-confetti c7"></view>
          <view class="fx-confetti c8"></view>
          <view class="fx-confetti c9"></view>
          <view class="fx-confetti c10"></view>
          <view class="fx-confetti c11"></view>
          <view class="fx-confetti c12"></view>
        </view>

        <view class="fx-copy" :class="effectType">
          <text class="fx-title">{{ effectType === 'redraw' ? '社死回避中...' : '挑战完成！' }}</text>
          <text class="fx-desc">{{ effectType === 'redraw' ? '便便已投掷，正在重新抽取更友好的挑战' : rewardText }}</text>
          <text class="fx-tip">点击任意区域可跳过动画</text>
        </view>
      </view>

    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToolsStore } from '@/stores/tools'
import { applyTheme, getTheme } from '@/utils/theme'
import { getStatusBarHeight } from '@/utils/system'

const toolsStore = useToolsStore()
const statusBarHeight = ref(44)
const selectedLevel = ref('all')
const selectedScene = ref('all')
const currentPunishment = ref('')
const currentMeta = ref(null)
const socialFriendlyOnly = ref(false)
const effectVisible = ref(false)
const effectType = ref('')
const rewardText = ref('')
let effectTimer = null

const levels = [
  { label: '全部', value: 'all' },
  { label: '轻度', value: 'light' },
  { label: '中度', value: 'medium' },
  { label: '桌游专属', value: 'tabletop' }
]

const scenes = ['all', '破冰', '熟人局', '欢乐局', '推理局']
const doneRewards = [
  '成就解锁：气氛发动机 +1，今天你就是局内MVP。',
  '奖励到账：社交勇气值暴涨，下一轮你先手。',
  '恭喜通关：本回合掌声与笑点都归你。',
  '隐藏称号获得：聚会节奏大师，继续保持。'
]

onMounted(() => {
  statusBarHeight.value = getStatusBarHeight(44)
  applyTheme(getTheme())
  toolsStore.init()
  selectedLevel.value = toolsStore.punishment.level || 'all'
  selectedScene.value = toolsStore.punishment.scene || 'all'
  socialFriendlyOnly.value = !!toolsStore.punishment.socialFriendlyOnly
})

function levelText(level) {
  const map = {
    light: '轻度',
    medium: '中度',
    tabletop: '桌游专属'
  }
  return map[level] || '全部'
}

function selectLevel(level) {
  selectedLevel.value = level
  toolsStore.setPunishmentLevel(level)
}

function selectScene(scene) {
  selectedScene.value = scene
  toolsStore.setPunishmentScene(scene)
}

function enableSocialMode() {
  socialFriendlyOnly.value = !socialFriendlyOnly.value
  toolsStore.setPunishmentSocialFriendlyOnly(socialFriendlyOnly.value)
}

function draw(options = {}) {
  const picked = toolsStore.drawPunishment({
    level: selectedLevel.value,
    scene: selectedScene.value,
    socialFriendlyOnly: socialFriendlyOnly.value,
    ...options
  })
  if (!picked) {
    uni.showToast({ title: '当前条件下暂无可用惩罚', icon: 'none' })
    return null
  }
  currentPunishment.value = picked.text
  currentMeta.value = picked
  return picked
}

function drawOne() {
  draw()
}

function redrawOne() {
  if (!currentMeta.value) {
    draw()
    return
  }
  if (currentMeta.value.canSkip === false) {
    uni.showToast({ title: '本条不允许重抽', icon: 'none' })
    return
  }
  draw()
}

function markDone() {
  if (!currentMeta.value) {
    uni.showToast({ title: '先抽一条挑战', icon: 'none' })
    return
  }
}

function playRedrawFx() {
  if (!currentMeta.value) {
    uni.showToast({ title: '先抽一条挑战', icon: 'none' })
    return
  }
  if (currentMeta.value.canSkip === false) {
    uni.showToast({ title: '本条不允许重抽', icon: 'none' })
    return
  }
  startFx('redraw')
}

function playDoneFx() {
  if (!currentMeta.value) {
    uni.showToast({ title: '先抽一条挑战', icon: 'none' })
    return
  }
  rewardText.value = doneRewards[Math.floor(Math.random() * doneRewards.length)]
  startFx('done')
}

function startFx(type) {
  if (effectTimer) {
    clearTimeout(effectTimer)
    effectTimer = null
  }
  effectType.value = type
  effectVisible.value = true
  try {
    if (type === 'redraw') {
      uni.vibrateShort({ type: 'heavy' })
    } else {
      uni.vibrateShort({ type: 'light' })
    }
  } catch (e) {
    // ignore vibration errors on unsupported platforms
  }
  effectTimer = setTimeout(() => {
    finishFxAction()
  }, 2500)
}

function finishFxNow() {
  if (!effectVisible.value) {
    return
  }
  if (effectTimer) {
    clearTimeout(effectTimer)
    effectTimer = null
  }
  finishFxAction()
}

function finishFxAction() {
  if (effectType.value === 'redraw') {
    redrawOne()
  }
  if (effectType.value === 'done') {
    markDone()
  }
  effectVisible.value = false
  effectType.value = ''
}

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.punish-page {
  position: relative;
  overflow: hidden;
  padding-bottom: 60rpx;
  min-height: 100vh;
  background: linear-gradient(180deg, #fffdf9 0%, #fff8ef 58%, #fff6eb 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(56rpx);
  pointer-events: none;
  z-index: 0;
}

.orb-a {
  width: 450rpx;
  height: 450rpx;
  top: -100rpx;
  left: -150rpx;
  background: radial-gradient(circle, rgba(255, 159, 67, 0.2), rgba(255, 159, 67, 0));
}

.orb-b {
  width: 350rpx;
  height: 350rpx;
  top: 300rpx;
  right: -100rpx;
  background: radial-gradient(circle, rgba(238, 82, 83, 0.16), rgba(238, 82, 83, 0));
}

.orb-c {
  width: 400rpx;
  height: 400rpx;
  bottom: 0;
  left: 0;
  background: radial-gradient(circle, rgba(254, 202, 87, 0.18), rgba(254, 202, 87, 0));
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.72);
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
  background: linear-gradient(135deg, rgba(255, 159, 67, 0.14), rgba(238, 82, 83, 0.08));
  border: 2rpx solid rgba(255, 159, 67, 0.22);
  box-shadow: 0 18rpx 42rpx rgba(225, 112, 85, 0.12);
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
  background: rgba(255, 255, 255, 0.54);
  backdrop-filter: blur(26px);
  border-radius: var(--radius-lg);
  padding: 32rpx;
  box-shadow: 0 24rpx 50rpx rgba(56, 35, 17, 0.08);
  border: 1rpx solid rgba(255, 255, 255, 0.9);
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
  gap: 10rpx;
}

.switch-label {
  font-size: 24rpx;
  color: var(--color-text-tertiary);
  font-weight: 600;
}

.switch-state {
  min-width: 34rpx;
  text-align: center;
  font-size: 22rpx;
  color: #8c7a68;
  font-weight: 700;

  &.on {
    color: #00a884;
  }
}

.switch-ui {
  width: 76rpx;
  height: 44rpx;
  border-radius: 44rpx;
  background: linear-gradient(180deg, #ece8e1, #d7d0c6);
  position: relative;
  transition: all 0.3s ease;
  box-shadow:
    inset 0 4rpx 8rpx rgba(100, 77, 51, 0.12),
    0 8rpx 16rpx rgba(100, 77, 51, 0.08);

  &.is-on {
    background: linear-gradient(180deg, #2fd7b1, #00b894);
    .switch-knob {
      transform: translateX(32rpx);
    }
  }
}

.switch-knob {
  width: 36rpx;
  height: 36rpx;
  background: linear-gradient(180deg, #ffffff, #f7f3ed);
  border-radius: 50%;
  position: absolute;
  top: 4rpx;
  left: 4rpx;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow:
    0 4rpx 8rpx rgba(0,0,0,0.08),
    inset 0 -2rpx 4rpx rgba(0,0,0,0.06);
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
  background: linear-gradient(160deg, rgba(255, 255, 255, 0.86), rgba(248, 244, 236, 0.86));
  color: var(--color-text-secondary);
  font-size: 24rpx;
  border: 2rpx solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 8rpx 20rpx rgba(86, 66, 43, 0.08),
    inset 0 1rpx 0 rgba(255, 255, 255, 0.9);
  transition: all 0.2s ease;

  &.active {
    background: linear-gradient(160deg, rgba(225, 112, 85, 0.16), rgba(255, 180, 140, 0.16));
    color: #e17055;
    border-color: rgba(225, 112, 85, 0.58);
    font-weight: 700;
    box-shadow:
      0 10rpx 24rpx rgba(225, 112, 85, 0.16),
      inset 0 1rpx 0 rgba(255, 255, 255, 0.9);
  }
  
  &.scene {
    border-radius: var(--radius-full);
    padding: 10rpx 24rpx;
    font-size: 24rpx;
    &.active {
       background: linear-gradient(160deg, rgba(9, 132, 227, 0.14), rgba(116, 185, 255, 0.14));
       color: #0984e3;
       border-color: rgba(9, 132, 227, 0.5);
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
  box-shadow: 0 26rpx 58rpx rgba(225, 112, 85, 0.1);
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
    color: #9e8f80;
    font-size: 28rpx;
    font-weight: 500;
    line-height: 1.6;
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
  background: linear-gradient(180deg, #fff4dd, #ffeecb);
  color: var(--color-text-secondary);
  font-size: 22rpx;
  border-radius: var(--radius-full);
  font-weight: 700;
  border: 1rpx solid rgba(255, 190, 118, 0.45);
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
  box-shadow: 0 22rpx 44rpx rgba(255, 118, 117, 0.28);
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
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 243, 236, 0.96));
    color: var(--color-text-secondary);
    border: 2rpx solid rgba(206, 193, 176, 0.8);
    box-shadow: 0 14rpx 30rpx rgba(0,0,0,0.06);
  }

  &.primary {
    background: linear-gradient(135deg, #00cec9, #00b894);
    color: #fff;
    box-shadow: 0 14rpx 30rpx rgba(0, 206, 201, 0.22);
  }

  &.disabled {
    opacity: 0.45;
  }
}

.fx-screen {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 130;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32rpx;
  animation: fxFade 180ms ease;

  &.redraw {
    background: radial-gradient(circle at 30% 20%, rgba(255, 183, 94, 0.5), rgba(66, 43, 22, 0.9));
    animation: fxFade 180ms ease, shakeLoop 520ms linear infinite;
  }

  &.done {
    background: radial-gradient(circle at 50% 25%, rgba(89, 255, 230, 0.38), rgba(13, 43, 56, 0.92));
    animation: fxFade 180ms ease;
  }
}

.fx-flash {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  opacity: 0;

  &.redraw {
    background: radial-gradient(circle at 50% 50%, rgba(255, 218, 184, 0.3), rgba(255, 218, 184, 0));
    animation: flashPulse 620ms ease-in-out infinite;
  }

  &.done {
    background: radial-gradient(circle at 50% 40%, rgba(255, 255, 255, 0.36), rgba(255, 255, 255, 0));
    animation: flashPulseDone 740ms ease-in-out infinite;
  }
}

.fx-poo-stage,
.fx-fire-stage {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.fx-splat {
  position: absolute;
  width: 220rpx;
  height: 220rpx;
  border-radius: 50%;
  background:
    radial-gradient(circle at 35% 40%, rgba(129, 92, 58, 0.85), rgba(82, 53, 30, 0.72) 58%, rgba(82, 53, 30, 0));
  filter: blur(1rpx);
  opacity: 0;

  &.s1 {
    left: -60rpx;
    top: -40rpx;
    animation: splatShow 2500ms ease-out;
  }

  &.s2 {
    right: -80rpx;
    top: 16%;
    animation: splatShow 2500ms ease-out 120ms;
  }

  &.s3 {
    left: 8%;
    bottom: -100rpx;
    animation: splatShow 2500ms ease-out 210ms;
  }

  &.s4 {
    right: 12%;
    bottom: -90rpx;
    animation: splatShow 2500ms ease-out 300ms;
  }
}

.fx-poo {
  position: absolute;
  top: 40%;
  font-size: 82rpx;
  opacity: 0;
  filter: drop-shadow(0 14rpx 16rpx rgba(0, 0, 0, 0.34));

  &.p1 {
    left: -60rpx;
    top: 24%;
    animation: pooArc1 1900ms ease-in-out infinite;
  }

  &.p2 {
    left: -20rpx;
    top: 40%;
    animation: pooArc2 2000ms ease-in-out 120ms infinite;
  }

  &.p3 {
    left: 20%;
    top: 64%;
    animation: pooArc3 2100ms ease-in-out 180ms infinite;
  }

  &.p4 {
    right: 18%;
    top: 22%;
    animation: pooArc4 1900ms ease-in-out 80ms infinite;
  }

  &.p5 {
    right: 0;
    top: 46%;
    animation: pooArc5 2050ms ease-in-out 140ms infinite;
  }

  &.p6 {
    right: -70rpx;
    top: 70%;
    animation: pooArc6 1980ms ease-in-out 220ms infinite;
  }

  &.p7 {
    left: -80rpx;
    top: 74%;
    animation: pooArc1 1960ms ease-in-out 260ms infinite;
  }

  &.p8 {
    left: 10%;
    top: 14%;
    animation: pooArc2 1880ms ease-in-out 300ms infinite;
  }

  &.p9 {
    left: 44%;
    top: 18%;
    animation: pooArc3 2020ms ease-in-out 360ms infinite;
  }

  &.p10 {
    right: 34%;
    top: 58%;
    animation: pooArc4 1960ms ease-in-out 420ms infinite;
  }

  &.p11 {
    right: 8%;
    top: 10%;
    animation: pooArc5 2100ms ease-in-out 480ms infinite;
  }

  &.p12 {
    right: -86rpx;
    top: 32%;
    animation: pooArc6 1940ms ease-in-out 520ms infinite;
  }
}

.fx-spark {
  position: absolute;
  left: var(--x, 50%);
  top: var(--y, 58%);
  width: 14rpx;
  height: 126rpx;
  border-radius: 999rpx;
  transform-origin: center bottom;
  transform: translateX(-50%) rotate(var(--rot));
  opacity: 0;
  box-shadow: 0 0 30rpx currentColor;

  &.s1 { color: #00cec9; --rot: 0deg; --x: 18%; --y: 66%; animation: sparkBurst 1850ms ease-out infinite; }
  &.s2 { color: #fdcb6e; --rot: 35deg; --x: 18%; --y: 66%; animation: sparkBurst 1900ms ease-out 90ms infinite; }
  &.s3 { color: #ff7675; --rot: 70deg; --x: 18%; --y: 66%; animation: sparkBurst 1880ms ease-out 180ms infinite; }
  &.s4 { color: #74b9ff; --rot: 105deg; --x: 48%; --y: 48%; animation: sparkBurst 1920ms ease-out 260ms infinite; }
  &.s5 { color: #55efc4; --rot: 140deg; --x: 48%; --y: 48%; animation: sparkBurst 1830ms ease-out 350ms infinite; }
  &.s6 { color: #a29bfe; --rot: 200deg; --x: 48%; --y: 48%; animation: sparkBurst 1940ms ease-out 430ms infinite; }
  &.s7 { color: #ffeaa7; --rot: 235deg; --x: 78%; --y: 64%; animation: sparkBurst 1900ms ease-out 520ms infinite; }
  &.s8 { color: #e17055; --rot: 270deg; --x: 78%; --y: 64%; animation: sparkBurst 1880ms ease-out 600ms infinite; }
  &.s9 { color: #ff9ff3; --rot: 305deg; --x: 78%; --y: 64%; animation: sparkBurst 1950ms ease-out 680ms infinite; }
  &.s10 { color: #81ecec; --rot: 340deg; --x: 32%; --y: 26%; animation: sparkBurst 1860ms ease-out 760ms infinite; }
  &.s11 { color: #00d2d3; --rot: 20deg; --x: 32%; --y: 26%; animation: sparkBurst 1980ms ease-out 840ms infinite; }
  &.s12 { color: #feca57; --rot: 315deg; --x: 32%; --y: 26%; animation: sparkBurst 1900ms ease-out 920ms infinite; }
  &.s13 { color: #48dbfb; --rot: 45deg; --x: 64%; --y: 24%; animation: sparkBurst 1960ms ease-out 1000ms infinite; }
  &.s14 { color: #ff6b6b; --rot: 90deg; --x: 64%; --y: 24%; animation: sparkBurst 1920ms ease-out 1080ms infinite; }
  &.s15 { color: #1dd1a1; --rot: 135deg; --x: 64%; --y: 24%; animation: sparkBurst 1880ms ease-out 1160ms infinite; }
  &.s16 { color: #f368e0; --rot: 220deg; --x: 52%; --y: 76%; animation: sparkBurst 1940ms ease-out 1240ms infinite; }
  &.s17 { color: #ff9f43; --rot: 260deg; --x: 52%; --y: 76%; animation: sparkBurst 1860ms ease-out 1320ms infinite; }
  &.s18 { color: #54a0ff; --rot: 300deg; --x: 52%; --y: 76%; animation: sparkBurst 1980ms ease-out 1400ms infinite; }
}

.fx-confetti {
  position: absolute;
  top: -60rpx;
  width: 16rpx;
  height: 34rpx;
  border-radius: 6rpx;
  opacity: 0;
  box-shadow: 0 4rpx 14rpx rgba(255, 255, 255, 0.22);
  animation: confettiFall 2300ms linear infinite;

  &.c1 { left: 8%; background: #ff7675; animation-delay: 0ms; }
  &.c2 { left: 14%; background: #74b9ff; animation-delay: 140ms; }
  &.c3 { left: 22%; background: #feca57; animation-delay: 260ms; }
  &.c4 { left: 30%; background: #55efc4; animation-delay: 380ms; }
  &.c5 { left: 38%; background: #a29bfe; animation-delay: 520ms; }
  &.c6 { left: 46%; background: #ff9ff3; animation-delay: 650ms; }
  &.c7 { left: 54%; background: #00d2d3; animation-delay: 780ms; }
  &.c8 { left: 62%; background: #ff6b6b; animation-delay: 920ms; }
  &.c9 { left: 70%; background: #48dbfb; animation-delay: 1080ms; }
  &.c10 { left: 78%; background: #1dd1a1; animation-delay: 1220ms; }
  &.c11 { left: 86%; background: #f368e0; animation-delay: 1360ms; }
  &.c12 { left: 92%; background: #ff9f43; animation-delay: 1520ms; }
}

.fx-copy {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 640rpx;
  padding: 32rpx 30rpx;
  border-radius: 30rpx;
  backdrop-filter: blur(10px);
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
  animation: cardLift 600ms cubic-bezier(0.2, 0.86, 0.24, 1);

  &.redraw {
    background: linear-gradient(165deg, rgba(64, 39, 18, 0.55), rgba(102, 69, 36, 0.46));
  }

  &.done {
    background: linear-gradient(165deg, rgba(8, 54, 64, 0.5), rgba(13, 74, 86, 0.4));
  }
}

.fx-title {
  font-size: 38rpx;
  font-weight: 800;
  color: #fff;
  line-height: 1.4;
  letter-spacing: 1rpx;
}

.fx-desc {
  font-size: 27rpx;
  color: rgba(255, 255, 255, 0.92);
  line-height: 1.6;
}

.fx-tip {
  font-size: 22rpx;
  color: rgba(255, 255, 255, 0.72);
}

@keyframes fxFade {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes shakeLoop {
  0% { transform: translate(0, 0); }
  20% { transform: translate(-4rpx, 2rpx); }
  40% { transform: translate(4rpx, -2rpx); }
  60% { transform: translate(-3rpx, 2rpx); }
  80% { transform: translate(3rpx, -1rpx); }
  100% { transform: translate(0, 0); }
}

@keyframes flashPulse {
  0% { opacity: 0; }
  40% { opacity: 0.7; }
  100% { opacity: 0; }
}

@keyframes flashPulseDone {
  0% { opacity: 0; }
  25% { opacity: 0.85; }
  100% { opacity: 0; }
}

@keyframes splatShow {
  0% {
    opacity: 0;
    transform: scale(0.2) rotate(0deg);
  }
  18% {
    opacity: 0.8;
    transform: scale(1.08) rotate(24deg);
  }
  100% {
    opacity: 0.36;
    transform: scale(1) rotate(20deg);
  }
}

@keyframes confettiFall {
  0% {
    opacity: 0;
    transform: translateY(-80rpx) rotate(0deg);
  }
  10% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateY(120vh) rotate(540deg);
  }
}

@keyframes cardLift {
  0% {
    opacity: 0;
    transform: translateY(20rpx) scale(0.96);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes pooArc1 {
  0% { transform: translate(-40rpx, 120rpx) rotate(0deg) scale(0.72); opacity: 0; }
  15% { opacity: 1; }
  55% { transform: translate(340rpx, -220rpx) rotate(160deg) scale(1); }
  100% { transform: translate(760rpx, 80rpx) rotate(300deg) scale(0.86); opacity: 0; }
}

@keyframes pooArc2 {
  0% { transform: translate(-120rpx, 110rpx) rotate(-20deg) scale(0.7); opacity: 0; }
  20% { opacity: 1; }
  55% { transform: translate(260rpx, -260rpx) rotate(100deg) scale(1.02); }
  100% { transform: translate(650rpx, 70rpx) rotate(240deg) scale(0.84); opacity: 0; }
}

@keyframes pooArc3 {
  0% { transform: translate(20rpx, 120rpx) rotate(0deg) scale(0.74); opacity: 0; }
  18% { opacity: 1; }
  55% { transform: translate(220rpx, -230rpx) rotate(130deg) scale(0.98); }
  100% { transform: translate(620rpx, 90rpx) rotate(280deg) scale(0.86); opacity: 0; }
}

@keyframes pooArc4 {
  0% { transform: translate(20rpx, 120rpx) rotate(0deg) scale(0.68); opacity: 0; }
  22% { opacity: 1; }
  55% { transform: translate(-300rpx, -240rpx) rotate(-100deg) scale(0.98); }
  100% { transform: translate(-700rpx, 70rpx) rotate(-240deg) scale(0.82); opacity: 0; }
}

@keyframes pooArc5 {
  0% { transform: translate(-20rpx, 120rpx) rotate(0deg) scale(0.74); opacity: 0; }
  20% { opacity: 1; }
  55% { transform: translate(-340rpx, -270rpx) rotate(-130deg) scale(1); }
  100% { transform: translate(-760rpx, 80rpx) rotate(-280deg) scale(0.86); opacity: 0; }
}

@keyframes pooArc6 {
  0% { transform: translate(20rpx, 118rpx) rotate(0deg) scale(0.72); opacity: 0; }
  20% { opacity: 1; }
  56% { transform: translate(-320rpx, -250rpx) rotate(-140deg) scale(1.02); }
  100% { transform: translate(-740rpx, 60rpx) rotate(-300deg) scale(0.84); opacity: 0; }
}

@keyframes sparkBurst {
  0% {
    opacity: 0;
    transform: translateX(-50%) rotate(var(--rot, 0deg)) scaleY(0.25);
  }
  18% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(-260rpx) rotate(var(--rot, 0deg)) scaleY(1.3);
  }
}
</style>