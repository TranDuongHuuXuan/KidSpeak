<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  stats: { type: Object, required: true },
})
</script>

<template>
  <section class="rounded-3xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6" aria-labelledby="practice-statistics-heading">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div><p class="text-xs font-extrabold uppercase tracking-wider text-amber-700">Danh mục 6</p><h2 id="practice-statistics-heading" class="mt-1 text-lg font-extrabold text-kids-text">Thành tích luyện tập</h2></div>
      <span class="rounded-full bg-slate-100 px-3 py-1 text-[10px] font-bold text-slate-600">Lưu trên trình duyệt này</span>
    </div>

    <div class="mt-4 grid grid-cols-2 gap-3 lg:grid-cols-4">
      <article class="rounded-2xl bg-kids-bg p-4"><p class="text-[11px] font-semibold text-slate-500">Số lượt đã xác nhận</p><p class="mt-2 text-2xl font-extrabold text-kids-text">{{ stats.attempts }}</p></article>
      <article class="rounded-2xl bg-amber-50 p-4"><p class="text-[11px] font-semibold text-slate-500">Điểm cao nhất</p><p class="mt-2 text-2xl font-extrabold text-amber-800">{{ stats.bestScore ?? '—' }}<span v-if="stats.bestScore !== null" class="ml-1 text-xs">/100</span></p></article>
      <article class="rounded-2xl bg-sky-50 p-4"><p class="text-[11px] font-semibold text-slate-500">Điểm gần nhất</p><p class="mt-2 text-2xl font-extrabold text-sky-800">{{ stats.latestScore ?? '—' }}<span v-if="stats.latestScore !== null" class="ml-1 text-xs">/100</span></p></article>
      <article class="rounded-2xl bg-emerald-50 p-4"><p class="text-[11px] font-semibold text-slate-500">Trạng thái</p><p class="mt-2 flex items-center gap-1.5 text-sm font-extrabold text-emerald-800"><AdminIcon :name="stats.completed ? 'circleCheck' : 'clock'" :size="17" />{{ stats.completed ? 'Đã luyện' : 'Đang chờ luyện' }}</p></article>
    </div>

    <div class="mt-4">
      <h3 class="text-xs font-extrabold text-slate-600">Lịch sử các lượt luyện</h3>
      <div v-if="stats.history.length" class="mt-2 space-y-2">
        <div v-for="(attempt, index) in stats.history" :key="`${attempt.practicedAt}-${index}`" class="flex items-center justify-between gap-3 rounded-xl border border-slate-100 px-3 py-2.5">
          <div class="flex min-w-0 items-center gap-2"><AdminIcon name="clock" :size="15" class="shrink-0 text-slate-400" /><span class="truncate text-xs text-slate-500">{{ new Date(attempt.practicedAt).toLocaleString('vi-VN') }}</span></div>
          <span class="shrink-0 text-xs font-extrabold text-slate-700">{{ attempt.score }}/100 · {{ attempt.label }}</span>
        </div>
      </div>
      <p v-else class="mt-2 rounded-xl border border-dashed border-slate-200 px-4 py-3 text-xs text-slate-500">Sau khi con xác nhận một lượt luyện, lịch sử mô phỏng sẽ xuất hiện ở đây.</p>
    </div>
  </section>
</template>
