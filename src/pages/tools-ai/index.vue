<template>
  <view class="page-container ai-page">
    <view class="bg-orb orb-a"></view>
    <view class="bg-orb orb-b"></view>

    <view class="nav-bar" :style="{ paddingTop: statusBarHeight + 'px' }">
      <view class="nav-content">
        <view class="nav-back" @tap="goBack"><text>← 返回</text></view>
        <text class="nav-title">🤖 AI 助手</text>
        <view class="nav-action" @tap="resetChat"><text>清空</text></view>
      </view>
    </view>

    <view class="ai-body" :style="{ paddingTop: (statusBarHeight + 44) + 'px' }">
      <view class="hero-card">
        <text class="hero-title">问我任何桌游问题</text>
        <text class="hero-desc">例如：4 人 60 分钟轻策略推荐？阿瓦隆 6 人怎么开局更稳？</text>
      </view>

      <scroll-view
        class="chat-list"
        scroll-y
        :scroll-with-animation="true"
        :scroll-into-view="scrollTarget"
      >
        <view
          v-for="(msg, index) in chatMessages"
          :key="`${msg.role}-${index}`"
          class="chat-item"
          :class="msg.role"
        >
          <view class="bubble">
            <text class="bubble-text">{{ msg.content }}</text>
            <view v-if="msg.reasoning && showReasoning" class="reasoning-box">
              <text class="reasoning-label">模型思考片段</text>
              <text class="reasoning-text">{{ msg.reasoning }}</text>
            </view>
          </view>
        </view>
        <view id="chat-bottom"></view>
      </scroll-view>

      <view class="quick-prompts">
        <view class="prompt-chip" @tap="applyPrompt('适合 5 人、45 分钟、新手友好的桌游推荐 3 款')">
          <text>新手推荐</text>
        </view>
        <view class="prompt-chip" @tap="applyPrompt('请解释一下一般隐藏身份桌游的主持流程')">
          <text>流程讲解</text>
        </view>
        <view class="prompt-chip" @tap="applyPrompt('起始玩家可以怎么公平决定？给我 5 个方法')">
          <text>开局先手</text>
        </view>
      </view>
    </view>

    <view class="composer">
      <view class="input-wrap">
        <textarea
          v-model="inputText"
          class="input"
          placeholder="输入桌游问题..."
          maxlength="500"
          :disabled="isStreaming"
          auto-height
        />
      </view>
      <view class="send-btn" :class="{ disabled: isSendDisabled }" @tap="sendQuestion">
        <text>{{ isStreaming ? '回答中...' : '发送' }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, nextTick, ref } from 'vue'
import { buildBoardgameMessages, streamBoardgameAnswer } from '@/utils/aiAssistant'

const statusBarHeight = ref(44)
const inputText = ref('')
const isStreaming = ref(false)
const scrollTarget = ref('')
const showReasoning = ref(false)

const chatMessages = ref([
  {
    role: 'assistant',
    content: '你好，我是桌游 AI 助手。你可以问我规则、人数匹配、开局建议、时长规划。',
    reasoning: ''
  }
])

const isSendDisabled = computed(() => {
  return isStreaming.value || !inputText.value.trim()
})

function goBack() {
  uni.navigateBack()
}

function resetChat() {
  chatMessages.value = [
    {
      role: 'assistant',
      content: '会话已清空。继续问我桌游问题吧。',
      reasoning: ''
    }
  ]
  inputText.value = ''
  scrollToBottom()
}

function applyPrompt(text) {
  inputText.value = text
}

function toModelMessages() {
  const history = chatMessages.value
    .filter((item) => item.role === 'user' || item.role === 'assistant')
    .slice(-12)
    .map((item) => ({
      role: item.role,
      content: item.content
    }))

  return buildBoardgameMessages(history)
}

async function sendQuestion() {
  const question = inputText.value.trim()
  if (!question || isStreaming.value) {
    return
  }

  isStreaming.value = true
  inputText.value = ''

  chatMessages.value.push({
    role: 'user',
    content: question,
    reasoning: ''
  })

  const assistantMsg = {
    role: 'assistant',
    content: '',
    reasoning: '',
    rawContent: ''
  }
  chatMessages.value.push(assistantMsg)
  scrollToBottom()

  try {
    await streamBoardgameAnswer({
      messages: toModelMessages(),
      onReasoning: (chunk) => {
        assistantMsg.reasoning += chunk
      },
      onText: (chunk) => {
        assistantMsg.rawContent += chunk
        assistantMsg.content = normalizeAssistantText(assistantMsg.rawContent)
        scrollToBottom()
      },
      onDone: () => {
        assistantMsg.content = normalizeAssistantText(assistantMsg.rawContent)
        if (!assistantMsg.content.trim()) {
          assistantMsg.content = '我暂时没有成功生成回答，请重试一次。'
        }
      }
    })
  } catch (error) {
    assistantMsg.content = error?.message || '调用失败，请确认云开发大模型已开通且在微信小程序环境中运行'
  } finally {
    isStreaming.value = false
    scrollToBottom()
  }
}

function scrollToBottom() {
  nextTick(() => {
    scrollTarget.value = ''
    setTimeout(() => {
      scrollTarget.value = 'chat-bottom'
    }, 0)
  })
}

function normalizeAssistantText(raw) {
  if (!raw) return ''

  let text = String(raw)
    .replace(/\r\n/g, '\n')
    .replace(/<think>[\s\S]*?<\/think>/g, '')
    .replace(/<\/?think>/g, '')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/^#{1,6}\s*/gm, '')
    .replace(/^>\s?/gm, '')
    .replace(/^\s*[-*]\s+/gm, '• ')
    .replace(/\n{3,}/g, '\n\n')
    .trim()

  // 防止纯分片阶段出现结尾半句标点堆积，做轻量整理
  text = text.replace(/[ \t]{2,}/g, ' ')

  return text
}

const sysInfo = uni.getSystemInfoSync()
statusBarHeight.value = sysInfo.statusBarHeight || 44
</script>

<style lang="scss" scoped>
.ai-page {
  position: relative;
  overflow: hidden;
  min-height: 100vh;
  padding-bottom: 220rpx;
  background: linear-gradient(180deg, #f8fffb 0%, #f4fff8 60%, #eefef6 100%);
}

.bg-orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(58rpx);
  pointer-events: none;
}

.orb-a {
  width: 420rpx;
  height: 420rpx;
  top: -120rpx;
  right: -120rpx;
  background: radial-gradient(circle, rgba(18, 185, 154, 0.2), rgba(18, 185, 154, 0));
}

.orb-b {
  width: 380rpx;
  height: 380rpx;
  bottom: 120rpx;
  left: -120rpx;
  background: radial-gradient(circle, rgba(112, 213, 173, 0.24), rgba(112, 213, 173, 0));
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 30;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(22px);
  border-bottom: 1rpx solid rgba(196, 236, 218, 0.7);
}

.nav-content {
  height: 88rpx;
  padding: 0 28rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-back,
.nav-action {
  font-size: 26rpx;
  color: #109a80;
  width: 90rpx;
}

.nav-action {
  text-align: right;
}

.nav-title {
  font-size: 30rpx;
  font-weight: 700;
  color: #0d5749;
}

.ai-body {
  position: relative;
  z-index: 2;
  padding: 24rpx;
}

.hero-card {
  background: linear-gradient(130deg, rgba(213, 255, 235, 0.9), rgba(236, 255, 246, 0.92));
  border-radius: 24rpx;
  padding: 24rpx;
  border: 2rpx solid rgba(88, 201, 161, 0.4);
  box-shadow: 0 16rpx 32rpx rgba(20, 102, 78, 0.08);
}

.hero-title {
  display: block;
  font-size: 30rpx;
  color: #0c5d4d;
  font-weight: 800;
}

.hero-desc {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #327565;
  line-height: 1.5;
}

.chat-list {
  margin-top: 20rpx;
  max-height: calc(100vh - 520rpx);
  padding-bottom: 12rpx;
}

.chat-item {
  display: flex;
  margin-bottom: 18rpx;
}

.chat-item.user {
  justify-content: flex-end;
}

.chat-item.assistant {
  justify-content: flex-start;
}

.bubble {
  max-width: 84%;
  border-radius: 22rpx;
  padding: 18rpx 20rpx;
}

.chat-item.user .bubble {
  background: linear-gradient(135deg, #10a688, #6fd59f);
  color: #ffffff;
  border-bottom-right-radius: 8rpx;
}

.chat-item.assistant .bubble {
  background: rgba(255, 255, 255, 0.92);
  border: 1rpx solid rgba(188, 233, 212, 0.8);
  border-bottom-left-radius: 8rpx;
}

.bubble-text {
  font-size: 28rpx;
  line-height: 1.6;
  white-space: pre-wrap;
}

.reasoning-box {
  margin-top: 14rpx;
  padding-top: 12rpx;
  border-top: 1rpx dashed rgba(72, 163, 132, 0.4);
}

.reasoning-label {
  display: block;
  font-size: 22rpx;
  color: #4a907f;
  margin-bottom: 4rpx;
}

.reasoning-text {
  font-size: 22rpx;
  color: #5c7f75;
  line-height: 1.5;
  white-space: pre-wrap;
}

.quick-prompts {
  margin-top: 8rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.prompt-chip {
  background: rgba(255, 255, 255, 0.78);
  border: 1rpx solid rgba(157, 222, 196, 0.8);
  border-radius: 999rpx;
  padding: 10rpx 20rpx;
}

.prompt-chip text {
  font-size: 23rpx;
  color: #0f7660;
}

.composer {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 40;
  background: rgba(252, 255, 253, 0.95);
  border-top: 1rpx solid rgba(184, 228, 208, 0.8);
  backdrop-filter: blur(20px);
  padding: 16rpx 20rpx calc(16rpx + env(safe-area-inset-bottom));
  display: flex;
  gap: 14rpx;
  align-items: flex-end;
}

.input-wrap {
  flex: 1;
  background: #ffffff;
  border: 2rpx solid rgba(164, 223, 198, 0.7);
  border-radius: 18rpx;
  padding: 10rpx 14rpx;
}

.input {
  width: 100%;
  min-height: 42rpx;
  max-height: 150rpx;
  font-size: 28rpx;
  line-height: 1.5;
}

.send-btn {
  min-width: 142rpx;
  height: 78rpx;
  border-radius: 18rpx;
  background: linear-gradient(135deg, #0fa486, #57c997);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-size: 28rpx;
  font-weight: 700;
}

.send-btn.disabled {
  opacity: 0.5;
}
</style>
