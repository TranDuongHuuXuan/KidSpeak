<script setup>
import { ref } from 'vue'
import AdminIcon from '../admin/AdminIcon.vue'

const props = defineProps({
  word: { type: Object, required: true },
  number: { type: Number, required: true },
  completed: { type: Boolean, default: false },
  score: { type: Number, default: null },
})

const emit = defineEmits(['practice'])
const imageIndex = ref(0)
const message = ref('')

function speakWord() {
  message.value = ''
  if (!('speechSynthesis' in window)) {
    message.value = 'Thiết bị chưa hỗ trợ đọc bằng giọng máy.'
    return
  }
  window.speechSynthesis.cancel()
  const utterance = new SpeechSynthesisUtterance(props.word.word)
  utterance.lang = 'vi-VN'
  utterance.onerror = () => { message.value = 'Không thể phát giọng đọc trên thiết bị này.' }
  window.speechSynthesis.speak(utterance)
}
</script>

<template>
  <article class="grid gap-4 rounded-2xl border border-amber-100 bg-white p-4 shadow-sm sm:grid-cols-[180px_minmax(0,1fr)] sm:p-5">
    <div class="relative flex h-40 items-center justify-center overflow-hidden rounded-xl bg-kids-bg sm:h-36">
      <img v-if="word.images.length" :src="word.images[imageIndex]" :alt="`Minh họa từ ${word.word}, ảnh ${imageIndex + 1}`" class="h-full w-full object-contain p-2" />
      <div v-else class="flex flex-col items-center text-slate-400">
        <AdminIcon name="image" :size="28" />
        <span class="mt-2 text-xs">Hình minh họa đang cập nhật</span>
      </div>
      <template v-if="word.images.length > 1">
        <button type="button" class="absolute left-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow" aria-label="Ảnh trước" @click="imageIndex = (imageIndex - 1 + word.images.length) % word.images.length"><AdminIcon name="arrow" :size="15" class="rotate-180" /></button>
        <button type="button" class="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow" aria-label="Ảnh tiếp theo" @click="imageIndex = (imageIndex + 1) % word.images.length"><AdminIcon name="arrow" :size="15" /></button>
        <span class="absolute bottom-2 right-2 rounded-full bg-white/90 px-2 py-1 text-[10px] font-bold text-slate-600">{{ imageIndex + 1 }}/{{ word.images.length }}</span>
      </template>
    </div>

    <div class="flex min-w-0 flex-col justify-center">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Từ {{ String(number).padStart(2, '0') }}</p>
        <span class="rounded-full px-2.5 py-1 text-[10px] font-bold" :class="completed ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-500'">{{ completed ? 'Đã luyện' : 'Chưa luyện' }}</span>
      </div>
      <h3 class="mt-1 text-2xl font-extrabold capitalize text-kids-text">{{ word.word }}</h3>
      <p v-if="word.phonetic" class="mt-1 text-sm text-slate-500">{{ word.phonetic }}</p>
      <p v-else class="mt-1 text-xs text-slate-400">Phiên âm đang được cập nhật</p>
      <p v-if="score !== null" class="mt-1 text-xs font-semibold text-sky-700">Lượt minh họa gần nhất: {{ score }}/100 <span class="font-normal text-slate-400">(không phải điểm AI)</span></p>
      <p v-if="message" class="mt-2 text-xs text-rose-600" role="status">{{ message }}</p>
      <div class="mt-4 flex flex-wrap gap-2">
        <button type="button" class="inline-flex min-h-10 items-center gap-2 rounded-xl border border-sky-200 bg-sky-50 px-3 text-xs font-bold text-sky-800 transition hover:bg-sky-100" @click="speakWord"><AdminIcon name="volume" :size="16" /> Nghe giọng máy</button>
        <button type="button" class="inline-flex min-h-10 items-center gap-2 rounded-xl bg-kids-cta px-3 text-xs font-extrabold text-white transition hover:bg-orange-600" @click="emit('practice', word)"><AdminIcon name="microphone" :size="16" /> Luyện phát âm</button>
      </div>
      <p class="mt-2 text-[10px] text-slate-400">Giọng đọc do thiết bị tạo, có thể khác phát âm mẫu chuẩn.</p>
    </div>
  </article>
</template>
