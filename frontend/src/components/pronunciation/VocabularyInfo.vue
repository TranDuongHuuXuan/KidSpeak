<script setup>
import { ref, watch } from 'vue'
import AdminIcon from '../admin/AdminIcon.vue'

const props = defineProps({
  word: { type: Object, required: true },
  topicTitle: { type: String, required: true },
})

const speaking = ref(false)
const message = ref('')
let speechRequest = null

function speakWord() {
  message.value = ''
  if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') {
    message.value = 'Thiết bị chưa hỗ trợ giọng đọc.'
    return
  }
  window.speechSynthesis.cancel()
  speechRequest = new SpeechSynthesisUtterance(props.word.word)
  speechRequest.lang = 'vi-VN'
  speechRequest.onstart = () => { speaking.value = true }
  speechRequest.onend = () => { speaking.value = false }
  speechRequest.onerror = () => {
    speaking.value = false
    message.value = 'Không thể phát giọng đọc trên thiết bị này.'
  }
  window.speechSynthesis.speak(speechRequest)
}

function stopSpeech() {
  if (!speaking.value) return
  window.speechSynthesis.cancel()
  speaking.value = false
}

watch(() => props.word.id, () => {
  window.speechSynthesis?.cancel()
  speaking.value = false
  message.value = ''
})
</script>

<template>
  <section class="rounded-3xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6" aria-labelledby="vocabulary-info-heading">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Danh mục 1</p>
        <h2 id="vocabulary-info-heading" class="mt-1 text-lg font-extrabold text-kids-text">Thông tin từ vựng</h2>
      </div>
      <span class="rounded-full bg-amber-50 px-3 py-1 text-[11px] font-bold text-amber-800">{{ topicTitle }}</span>
    </div>

    <div class="mt-5 grid items-center gap-5 md:grid-cols-[minmax(190px,0.8fr)_minmax(0,1.2fr)]">
      <div class="flex h-48 items-center justify-center overflow-hidden rounded-2xl bg-kids-bg sm:h-56">
        <img v-if="word.images?.length" :src="word.images[0]" :alt="`Minh họa từ ${word.word}`" class="h-full w-full object-contain p-3" />
        <div v-else class="flex flex-col items-center text-slate-400"><AdminIcon name="image" :size="30" /><span class="mt-2 text-xs">Hình minh họa đang cập nhật</span></div>
      </div>

      <div class="text-center md:text-left">
        <p class="text-xs font-semibold text-slate-400">Từ chuẩn cần luyện</p>
        <h3 class="mt-1 text-4xl font-extrabold capitalize text-kids-text sm:text-5xl">{{ word.word }}</h3>
        <p class="mt-2 text-sm text-slate-500">{{ word.phonetic || 'Phiên âm đang được cập nhật' }}</p>
        <p class="mt-2 text-xs text-slate-400">Hình minh họa thuộc chủ đề {{ topicTitle }}; không phải ảnh cụ thể của từ nếu chưa có ảnh riêng.</p>
        <div class="mt-4 flex flex-wrap justify-center gap-2 md:justify-start">
          <button type="button" class="inline-flex min-h-11 items-center gap-2 rounded-xl bg-sky-100 px-4 text-sm font-bold text-sky-900 transition hover:bg-sky-200" :aria-pressed="speaking" @click="speaking ? stopSpeech() : speakWord()">
            <AdminIcon :name="speaking ? 'close' : 'volume'" :size="18" />{{ speaking ? 'Đang phát · Dừng' : 'Nghe giọng đọc' }}
          </button>
          <button type="button" class="inline-flex min-h-11 items-center gap-2 rounded-xl border border-sky-200 px-4 text-sm font-bold text-sky-800 transition hover:bg-sky-50" @click="speakWord">
            <AdminIcon name="play" :size="16" />Nghe lại
          </button>
        </div>
        <p class="mt-2 text-[10px] text-slate-400">Giọng tổng hợp tiếng Việt của thiết bị, không phải âm thanh mẫu chuyên môn.</p>
        <p v-if="message" class="mt-2 text-xs text-rose-600" role="status">{{ message }}</p>
      </div>
    </div>
  </section>
</template>
