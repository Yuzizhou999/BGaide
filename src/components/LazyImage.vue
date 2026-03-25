<template>
  <image
    :id="observerId"
    :src="displaySrc"
    :mode="mode"
    :lazy-load="false"
    @error="handleError"
  />
</template>

<script setup>
import { computed, getCurrentInstance, onMounted, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  placeholder: { type: String, default: '/static/icons/placeholder.svg' },
  mode: { type: String, default: 'aspectFill' },
  preload: { type: Number, default: 300 }
})

const instance = getCurrentInstance()
const observerId = `lazy-image-${Math.random().toString(36).slice(2, 10)}`
const loaded = ref(false)
const broken = ref(false)
let observer = null

const displaySrc = computed(() => {
  if (broken.value) return props.placeholder
  if (!loaded.value) return props.placeholder
  return props.src || props.placeholder
})

function markLoaded() {
  loaded.value = true
  if (observer) {
    observer.disconnect()
    observer = null
  }
}

function initObserver() {
  if (loaded.value || !instance) return
  if (!uni.createIntersectionObserver) {
    loaded.value = true
    return
  }

  observer = uni.createIntersectionObserver(instance)
  observer
    .relativeToViewport({ bottom: props.preload, top: props.preload })
    .observe(`#${observerId}`, (res) => {
      if (res && res.intersectionRatio > 0) {
        markLoaded()
      }
    })
}

function handleError() {
  broken.value = true
}

watch(
  () => props.src,
  (next, prev) => {
    broken.value = false
    if (!next) {
      loaded.value = false
      return
    }

    if (loaded.value && prev && next !== prev) {
      // 已经进入可视区后，切换图片时直接显示新图
      loaded.value = true
    }
  }
)

onMounted(() => {
  initObserver()
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
})
</script>
