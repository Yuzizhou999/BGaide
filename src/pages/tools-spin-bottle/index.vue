<template>
    <view class="page-container spin-page">
        <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
            <view class="nav-content">
                <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
                <text class="nav-title">🍾 转瓶子</text>
                <view style="width: 80rpx" />
            </view>
        </view>

        <view class="spin-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px', minHeight: bodyMinHeight + 'px' }">
            <!-- 提示文字 -->
            <text class="spin-hint">将手机平放在桌子中央</text>

            <!-- 转盘区域 -->
            <view class="spin-area" @tap="startSpin">
                <!-- 外圈装饰 -->
                <view class="outer-ring">
                    <view class="outer-ring ring-mid"></view>
                    <view class="outer-ring ring-inner"></view>
                    <view class="tick-marks">
                        <view v-for="i in 12" :key="i" class="tick" :style="{ transform: `rotate(${i * 30}deg)` }" />
                    </view>
                </view>

                <!-- Canvas 瓶子 -->
                <view class="canvas-wrap">
                    <canvas type="2d" id="spinCanvas" class="spin-canvas"
                        :style="{ width: canvasSize + 'px', height: canvasSize + 'px' }" />
                </view>

                <!-- 中心发光点 -->
                <view class="center-dot" />
            </view>

            <!-- 状态提示 -->
            <view class="status-area">
                <text class="status-text">
                    {{ statusText }}
                </text>
            </view>

            <!-- 操作按钮 -->
            <view class="action-row">
                <view class="spin-btn" :class="{ disabled: isSpinning }" @tap="startSpin">
                    <text>{{ isSpinning ? '旋转中...' : '🍾 点击旋转' }}</text>
                </view>
            </view>
        </view>
    </view>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const statusBarHeight = ref(44)
const canvasSize = ref(280)
const bodyMinHeight = ref(640)

const isSpinning = ref(false)
const isFinished = ref(false)

// 旋转参数
let angle = 0
const SPIN_DURATION = 2000
let spinStartAngle = 0
let spinTargetAngle = 0
let spinStartTime = 0
let animFrameId = null
let canvasCtx = null
let canvasNode = null

const statusText = ref('点击屏幕开始旋转')

onMounted(() => {
    const sysInfo = uni.getSystemInfoSync()
    statusBarHeight.value = sysInfo.statusBarHeight || 44
    bodyMinHeight.value = Math.max(560, (sysInfo.windowHeight || 720) - (statusBarHeight.value + 44))

    // 根据屏幕宽度调整 canvas 大小
    const screenWidth = sysInfo.windowWidth
    canvasSize.value = Math.min(screenWidth * 0.65, 300)

    // 初始化 Canvas
    setTimeout(() => {
        initCanvas()
    }, 300)
})

onUnmounted(() => {
    if (animFrameId) {
        cancelFrame(animFrameId)
    }
})

function requestFrame(callback) {
    if (canvasNode && typeof canvasNode.requestAnimationFrame === 'function') {
        return canvasNode.requestAnimationFrame(callback)
    }
    return requestAnimationFrame(callback)
}

function cancelFrame(id) {
    if (canvasNode && typeof canvasNode.cancelAnimationFrame === 'function') {
        canvasNode.cancelAnimationFrame(id)
        return
    }
    cancelAnimationFrame(id)
}

function initCanvas() {
    const query = uni.createSelectorQuery()
    query.select('#spinCanvas')
        .fields({ node: true, size: true })
        .exec((res) => {
            if (!res[0]) return

            canvasNode = res[0].node
            canvasCtx = canvasNode.getContext('2d')

            // 设置 canvas 实际像素大小（高清）
            const dpr = uni.getSystemInfoSync().pixelRatio
            canvasNode.width = canvasSize.value * dpr
            canvasNode.height = canvasSize.value * dpr
            canvasCtx.scale(dpr, dpr)

            drawBottle(0)
        })
}

function drawBottle(rotation) {
    if (!canvasCtx) return

    const ctx = canvasCtx
    const size = canvasSize.value
    const cx = size / 2
    const cy = size / 2

    // 清空画布
    ctx.clearRect(0, 0, size, size)

    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rotation)

    // ====== 绘制匕首 ======
    const scale = size / 280

    // 刀刃（渐变银色）
    const bladeGrad = ctx.createLinearGradient(0, -95 * scale, 0, 20 * scale)
    bladeGrad.addColorStop(0, '#e8eaed')
    bladeGrad.addColorStop(0.3, '#c0c8d4')
    bladeGrad.addColorStop(0.5, '#f0f2f5')
    bladeGrad.addColorStop(0.7, '#c0c8d4')
    bladeGrad.addColorStop(1, '#a0a8b4')

    ctx.beginPath()
    ctx.moveTo(0, -95 * scale)            // 刀尖
    ctx.lineTo(14 * scale, -30 * scale)   // 右刃
    ctx.quadraticCurveTo(16 * scale, -10 * scale, 14 * scale, 10 * scale)
    ctx.lineTo(10 * scale, 20 * scale)    // 右侧收
    ctx.lineTo(-10 * scale, 20 * scale)   // 左侧收
    ctx.lineTo(-14 * scale, 10 * scale)
    ctx.quadraticCurveTo(-16 * scale, -10 * scale, -14 * scale, -30 * scale)
    ctx.closePath()
    ctx.fillStyle = bladeGrad
    ctx.fill()

    // 刀刃中脊线
    ctx.beginPath()
    ctx.moveTo(0, -90 * scale)
    ctx.lineTo(0, 18 * scale)
    ctx.strokeStyle = 'rgba(255,255,255,0.5)'
    ctx.lineWidth = 1.5 * scale
    ctx.stroke()

    // 护手（金色横条）
    const guardGrad = ctx.createLinearGradient(-22 * scale, 0, 22 * scale, 0)
    guardGrad.addColorStop(0, '#b8860b')
    guardGrad.addColorStop(0.3, '#ffd700')
    guardGrad.addColorStop(0.5, '#fff8dc')
    guardGrad.addColorStop(0.7, '#ffd700')
    guardGrad.addColorStop(1, '#b8860b')

    ctx.beginPath()
    ctx.ellipse(0, 22 * scale, 22 * scale, 7 * scale, 0, 0, Math.PI * 2)
    ctx.fillStyle = guardGrad
    ctx.fill()
    ctx.strokeStyle = '#8B6914'
    ctx.lineWidth = 1 * scale
    ctx.stroke()

    // 手柄（深红木纹）
    const handleGrad = ctx.createLinearGradient(-8 * scale, 0, 8 * scale, 0)
    handleGrad.addColorStop(0, '#5c1a0a')
    handleGrad.addColorStop(0.3, '#8b3a1a')
    handleGrad.addColorStop(0.5, '#a0442a')
    handleGrad.addColorStop(0.7, '#8b3a1a')
    handleGrad.addColorStop(1, '#5c1a0a')

    ctx.beginPath()
    const hx = -8 * scale, hy = 30 * scale, hw = 16 * scale, hh = 50 * scale, hr = 3 * scale
    ctx.moveTo(hx + hr, hy)
    ctx.lineTo(hx + hw - hr, hy)
    ctx.arcTo(hx + hw, hy, hx + hw, hy + hr, hr)
    ctx.lineTo(hx + hw, hy + hh - hr)
    ctx.arcTo(hx + hw, hy + hh, hx + hw - hr, hy + hh, hr)
    ctx.lineTo(hx + hr, hy + hh)
    ctx.arcTo(hx, hy + hh, hx, hy + hh - hr, hr)
    ctx.lineTo(hx, hy + hr)
    ctx.arcTo(hx, hy, hx + hr, hy, hr)
    ctx.closePath()
    ctx.fillStyle = handleGrad
    ctx.fill()

    // 手柄金属环
    for (let i = 0; i < 3; i++) {
        const y = (35 + i * 18) * scale
        ctx.beginPath()
        ctx.rect(-9 * scale, y, 18 * scale, 3 * scale)
        ctx.fillStyle = i === 1 ? '#ffd700' : '#cd9b1d'
        ctx.fill()
    }

    // 柄底宝石
    ctx.beginPath()
    ctx.arc(0, 86 * scale, 6 * scale, 0, Math.PI * 2)
    const gemGrad = ctx.createRadialGradient(
        -2 * scale, 83 * scale, 1 * scale,
        0, 86 * scale, 6 * scale
    )
    gemGrad.addColorStop(0, '#ff6b6b')
    gemGrad.addColorStop(0.5, '#ee2c2c')
    gemGrad.addColorStop(1, '#8b0000')
    ctx.fillStyle = gemGrad
    ctx.fill()
    ctx.strokeStyle = '#ffd700'
    ctx.lineWidth = 1.5 * scale
    ctx.stroke()

    ctx.restore()
}

function startSpin() {
    if (isSpinning.value) return

    isSpinning.value = true
    isFinished.value = false
    statusText.value = '旋转中...'

    // 8~16 圈 + 随机角度，保证足够随机。
    const randomTurns = 8 + Math.floor(Math.random() * 9)
    const entropy = ((Date.now() % 997) / 997 + Math.random()) % 1
    const randomOffset = entropy * Math.PI * 2

    spinStartAngle = angle
    spinTargetAngle = spinStartAngle + randomTurns * Math.PI * 2 + randomOffset
    spinStartTime = 0

    if (animFrameId) {
        cancelFrame(animFrameId)
        animFrameId = null
    }

    // 震动提示开始
    uni.vibrateShort({ type: 'medium' })

    animFrameId = requestFrame(animate)
}

function animate(ts) {
    if (!isSpinning.value) return

    if (!spinStartTime) {
        spinStartTime = ts
    }

    const elapsed = ts - spinStartTime
    const progress = Math.min(1, elapsed / SPIN_DURATION)
    const eased = 1 - Math.pow(1 - progress, 3)
    angle = spinStartAngle + (spinTargetAngle - spinStartAngle) * eased

    drawBottle(angle)

    if (progress >= 1) {
        // 停止旋转
        isSpinning.value = false
        isFinished.value = true
        statusText.value = '🎯 结果已定！再次点击重新旋转'

        // 停止时强震动反馈
        uni.vibrateLong()
        return
    }

    animFrameId = requestFrame(animate)
}

function goBack() {
    uni.navigateBack()
}
</script>

<style lang="scss" scoped>
.spin-page {
    min-height: 100vh;
    background: #0f1326;
    overflow: hidden;
}

.nav-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 50;
    background: rgba(10, 10, 26, 0.9);
    backdrop-filter: blur(20px);
    border-bottom: 1rpx solid rgba(255, 255, 255, 0.08);
}

.nav-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 88rpx;
    padding: 0 32rpx;
}

.nav-back {
    font-size: 28rpx;
    color: #a78bfa;
    width: 80rpx;
    white-space: nowrap;
}

.nav-title {
    font-size: 32rpx;
    font-weight: 700;
    color: #e8e8f0;
}

.spin-body {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 32rpx 28rpx;
    position: relative;
    z-index: 2;
}

.spin-hint {
    color: rgba(255, 255, 255, 0.4);
    font-size: 26rpx;
    margin-bottom: 12rpx;
    letter-spacing: 4rpx;
}

/* 转盘区域 */
.spin-area {
    position: relative;
    width: 100%;
    flex: 1;
    min-height: 620rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
}

/* 外圈装饰环 */
.outer-ring {
    position: absolute;
    width: 620rpx;
    height: 620rpx;
    border-radius: 50%;
    border: 3rpx solid rgba(167, 139, 250, 0.28);
}

.ring-mid {
    width: 500rpx;
    height: 500rpx;
    border-color: rgba(96, 165, 250, 0.24);
}

.ring-inner {
    width: 380rpx;
    height: 380rpx;
    border-color: rgba(250, 204, 21, 0.2);
}

.tick-marks {
    position: relative;
    width: 100%;
    height: 100%;
}

.tick {
    position: absolute;
    top: 0;
    left: 50%;
    width: 4rpx;
    height: 20rpx;
    background: rgba(167, 139, 250, 0.4);
    transform-origin: 50% 310rpx;
    border-radius: 2rpx;
}

/* Canvas */
.canvas-wrap {
    position: relative;
    z-index: 2;
}

.spin-canvas {
    display: block;
}

/* 中心发光点 */
.center-dot {
    position: absolute;
    width: 24rpx;
    height: 24rpx;
    border-radius: 50%;
    background: radial-gradient(circle, #ffd700, #b8860b);
    z-index: 3;
}

/* 状态区 */
.status-area {
    margin: 8rpx 0 18rpx;
    min-height: 60rpx;
    display: flex;
    align-items: center;
}

.status-text {
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.65);
    letter-spacing: 2rpx;
    transition: all 0.5s ease;
}

/* 操作按钮 */
.action-row {
    width: 100%;
    padding: 0 40rpx;
}

.spin-btn {
    height: 96rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #7c3aed, #a78bfa);
    border-radius: 48rpx;
    color: #fff;
    font-size: 34rpx;
    font-weight: 700;
    box-shadow: 0 14rpx 34rpx rgba(124, 58, 237, 0.42);
    letter-spacing: 4rpx;

    &.disabled {
        opacity: 0.5;
    }

    &:active:not(.disabled) {
        transform: scale(0.97);
    }
}
</style>
