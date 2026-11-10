<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  result: { type: Object, required: true },
})
</script>

<template>
  <section class="rounded-3xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6" aria-labelledby="pronunciation-feedback-heading">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div><p class="text-xs font-extrabold uppercase tracking-wider text-violet-700">Danh mục 5</p><h2 id="pronunciation-feedback-heading" class="mt-1 text-lg font-extrabold text-kids-text">Nhận xét và sửa lỗi</h2></div>
      <span class="rounded-full bg-amber-50 px-3 py-1 text-[10px] font-extrabold text-amber-900">{{ result.label }}</span>
    </div>
    <div class="mt-4 grid gap-3 md:grid-cols-3">
      <article class="rounded-2xl bg-emerald-50 p-4">
        <h3 class="flex items-center gap-2 text-sm font-extrabold text-emerald-800"><AdminIcon name="circleCheck" :size="17" />Con làm tốt</h3>
        <p class="mt-2 text-xs leading-5 text-emerald-900/80">{{ result.strengths }}</p>
      </article>
      <article class="rounded-2xl bg-amber-50 p-4">
        <h3 class="flex items-center gap-2 text-sm font-extrabold text-amber-900"><AdminIcon name="sparkles" :size="17" />Có thể luyện thêm</h3>
        <p class="mt-2 text-xs leading-5 text-amber-900/80">{{ result.improvement }}</p>
      </article>
      <article class="rounded-2xl bg-sky-50 p-4">
        <h3 class="flex items-center gap-2 text-sm font-extrabold text-sky-900"><AdminIcon name="play" :size="16" />Thử cách này</h3>
        <p class="mt-2 text-xs leading-5 text-sky-900/80">{{ result.retryGuide }} {{ result.suggestion }}</p>
      </article>
    </div>
    <p class="mt-3 text-[10px] text-slate-400">Các nhận xét trên là dữ liệu minh họa, không được suy ra từ âm thanh của con.</p>
  </section>
</template>
