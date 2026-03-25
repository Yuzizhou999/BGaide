/**
 * 微信云开发 AI 助手封装（桌游问答）
 */

const MODEL_SERVICE_ID = 'hunyuan-exp'
const MODEL_NAME = 'hunyuan-2.0-thinking-20251109'

const SYSTEM_PROMPT = [
    '你是一个桌游助手，熟悉各种桌游规则，擅长给出清晰、可执行的桌游建议。',
].join('')

export function buildBoardgameMessages(history = []) {
    return [
        { role: 'system', content: SYSTEM_PROMPT },
        ...history
    ]
}

export async function streamBoardgameAnswer({
    messages,
    onReasoning,
    onText,
    onDone
}) {
    if (typeof wx === 'undefined' || !wx.cloud?.extend?.AI?.createModel) {
        throw new Error('当前环境不支持微信云开发大模型，请在微信小程序中使用')
    }

    const res = await wx.cloud.extend.AI.createModel(MODEL_SERVICE_ID).streamText({
        data: {
            model: MODEL_NAME,
            messages
        }
    })

    for await (const event of res.eventStream) {
        if (event?.data === '[DONE]') {
            break
        }

        let parsed
        try {
            parsed = JSON.parse(event?.data || '{}')
        } catch (error) {
            continue
        }

        const reasoning = parsed?.choices?.[0]?.delta?.reasoning_content
        if (reasoning && typeof onReasoning === 'function') {
            onReasoning(reasoning)
        }

        const content = parsed?.choices?.[0]?.delta?.content
        if (content && typeof onText === 'function') {
            onText(content)
        }
    }

    if (typeof onDone === 'function') {
        onDone()
    }
}
