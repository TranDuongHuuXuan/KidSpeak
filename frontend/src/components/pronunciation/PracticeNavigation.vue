<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  topicSlug: { type: String, required: true },
  previousWord: { type: Object, default: null },
  nextWord: { type: Object, default: null },
  confirmed: { type: Boolean, default: false },
})

const emit = defineEmits(['previous', 'next', 'retry'])
</script>

<template>
  <nav class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-5" aria-label="Điều hướng bài học">
    <p class="text-xs font-extrabold uppercase tracking-wider text-slate-500">Danh mục 7 · Điều hướng bài học</p>
    <div class="mt-3 grid gap-2 sm:grid-cols-3">
      <RouterLink :to="{ name: 'StudentTopicDetail', params: { topicSlug } }" class="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl border border-slate-200 px-3 text-xs font-bold text-slate-700 transition hover:bg-slate-50"><AdminIcon name="arrow" :size="16" class="rotate-180" />Quay lại danh sách từ</RouterLink>
      <button type="button" class="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-kids-cta px-3 text-xs font-extrabold text-white transition hover:bg-orange-600 disabled:opacity-45" :disabled="!confirmed" @click="emit('retry')"><AdminIcon name="microphone" :size="16" />Luyện tập lại</button>
      <button type="button" class="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-kids-primary px-3 text-xs font-extrabold text-kids-text transition hover:bg-amber-400 disabled:cursor-not-allowed disabled:opacity-45" :disabled="!nextWord || !confirmed" @click="emit('next')">{{ nextWord ? 'Từ tiếp theo' : 'Đã đến từ cuối' }}<AdminIcon v-if="nextWord" name="arrow" :size="16" /></button>
    </div>
    <div v-if="previousWord" class="mt-3 text-center"><button type="button" class="text-xs font-bold text-sky-700 hover:text-sky-900" @click="emit('previous')">← Từ trước: {{ previousWord.word }}</button></div>
    <p v-if="!nextWord" class="mt-3 text-center text-[11px] leading-5 text-slate-500">Con đã đến từ cuối cùng trong chủ đề. Có thể quay lại danh sách từ để chọn một từ khác.</p>
  </nav>
</template>
