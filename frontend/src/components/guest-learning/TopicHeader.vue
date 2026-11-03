<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  topic: { type: Object, required: true },
  currentIndex: { type: Number, required: true },
  totalWords: { type: Number, required: true },
  practicedCount: { type: Number, required: true },
})
</script>

<template>
  <div class="border-b border-kids-text/10 bg-white">
    <div class="mx-auto max-w-screen-2xl px-4 py-4 sm:px-8 lg:px-12">
      <RouterLink
        :to="{ name: 'GuestLearning' }"
        class="inline-flex min-h-10 items-center gap-2 rounded-lg px-2 text-sm font-bold text-kids-text/75 transition hover:bg-kids-secondary/10 hover:text-kids-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary"
      >
        <svg viewBox="0 0 20 20" class="h-5 w-5 fill-none stroke-current" stroke-width="1.8" aria-hidden="true">
          <path d="M16 10H4m5 5-5-5 5-5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        Tất cả chủ đề
      </RouterLink>

      <div class="mt-3 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-wide text-kids-text/55">Đang khám phá</p>
          <h1 class="mt-1 text-2xl font-extrabold text-kids-text sm:text-3xl">{{ topic.title }}</h1>
        </div>
        <p class="text-sm font-bold text-kids-text">
          Từ {{ String(currentIndex + 1).padStart(2, '0') }}/{{ totalWords }}
          <span class="ml-2 font-medium text-kids-text/55">· Đã luyện {{ practicedCount }}/{{ totalWords }} từ</span>
        </p>
      </div>

      <div class="mt-3 h-2 overflow-hidden rounded-full bg-kids-text/10" role="progressbar" :aria-valuenow="practicedCount" :aria-valuemin="0" :aria-valuemax="totalWords" :aria-label="`Đã luyện ${practicedCount} trên ${totalWords} từ`">
        <div class="h-full rounded-full bg-kids-secondary transition-[width] duration-300" :style="{ width: `${(practicedCount / totalWords) * 100}%` }"></div>
      </div>
    </div>
  </div>
</template>
