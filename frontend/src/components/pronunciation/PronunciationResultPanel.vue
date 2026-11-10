<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  result: { type: Object, required: true },
})
</script>

<template>
  <section class="rounded-3xl border border-sky-200 bg-sky-50/80 p-5 shadow-sm sm:p-6" aria-labelledby="pronunciation-result-heading" aria-live="polite">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-center">
      <div class="flex h-28 w-28 shrink-0 flex-col items-center justify-center rounded-full border-4 border-white bg-kids-primary/50 text-kids-text shadow-sm">
        <span class="text-4xl font-extrabold">{{ result.overall }}</span><span class="text-[9px] font-bold uppercase">/ 100</span>
      </div>
      <div class="flex-1">
        <span class="inline-flex items-center gap-1.5 rounded-full bg-amber-100 px-3 py-1 text-[11px] font-extrabold text-amber-900"><AdminIcon name="sparkles" :size="14" />{{ result.label }}</span>
        <h2 id="pronunciation-result-heading" class="mt-3 text-xl font-extrabold text-kids-text">{{ result.classification }}</h2>
        <p class="mt-1 text-xs leading-5 text-slate-600">Điểm minh họa giao diện, không phải kết quả phân tích giọng nói hay AI.</p>
      </div>
    </div>

    <div class="mt-5 grid gap-3 sm:grid-cols-3">
      <article v-for="part in result.components" :key="part.key" class="rounded-2xl bg-white p-4">
        <div class="flex items-center justify-between gap-2 text-xs"><h3 class="font-bold text-slate-600">{{ part.label }}</h3><span class="font-extrabold text-kids-text">{{ part.score }}/100</span></div>
        <div class="mt-3 h-3 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="part.score" aria-valuemin="0" aria-valuemax="100" :aria-label="`Điểm minh họa ${part.label}`"><div class="h-full rounded-full transition-all" :class="part.score >= 80 ? 'bg-emerald-400' : 'bg-amber-400'" :style="{ width: `${part.score}%` }"></div></div>
        <p class="mt-2 text-[10px] text-slate-400">Tỷ trọng minh họa {{ part.weight }}%</p>
      </article>
    </div>
  </section>
</template>
