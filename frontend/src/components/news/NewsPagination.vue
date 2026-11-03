<script setup>
import { ChevronLeft, ChevronRight } from '@lucide/vue'

defineProps({
  currentPage: { type: Number, required: true },
  pageCount: { type: Number, required: true },
})

const emit = defineEmits(['update:currentPage'])
</script>

<template>
  <nav v-if="pageCount > 1" class="mt-9 flex items-center justify-center gap-2" aria-label="Phân trang bài viết">
    <button type="button" :disabled="currentPage === 1" class="inline-flex h-10 items-center gap-1 rounded-xl border border-kids-text/10 bg-white px-3 text-sm font-semibold text-kids-text transition hover:bg-kids-bg disabled:cursor-not-allowed disabled:opacity-40" @click="emit('update:currentPage', currentPage - 1)"><ChevronLeft :size="17" />Trước</button>
    <button v-for="page in pageCount" :key="page" type="button" :aria-current="page === currentPage ? 'page' : undefined" class="h-10 min-w-10 rounded-xl border px-3 text-sm font-bold transition" :class="page === currentPage ? 'border-kids-text bg-kids-text text-white' : 'border-kids-text/10 bg-white text-kids-text hover:bg-kids-bg'" @click="emit('update:currentPage', page)">{{ page }}</button>
    <button type="button" :disabled="currentPage === pageCount" class="inline-flex h-10 items-center gap-1 rounded-xl border border-kids-text/10 bg-white px-3 text-sm font-semibold text-kids-text transition hover:bg-kids-bg disabled:cursor-not-allowed disabled:opacity-40" @click="emit('update:currentPage', currentPage + 1)">Tiếp<ChevronRight :size="17" /></button>
  </nav>
</template>
