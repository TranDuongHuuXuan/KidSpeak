<script setup>
defineProps({
  score: { type: Number, required: true },
  word: { type: String, required: true },
})

defineEmits(['retry', 'next'])
</script>

<template>
  <section class="rounded-3xl border border-kids-secondary/30 bg-kids-secondary/10 p-5 sm:p-7" aria-live="polite">
    <div class="flex flex-col gap-5 sm:flex-row sm:items-center">
      <div class="flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-full border-4 border-white bg-kids-primary/50 text-kids-text shadow-sm">
        <span class="text-3xl font-extrabold">{{ score }}</span>
        <span class="text-[10px] font-bold uppercase">Mô phỏng</span>
      </div>
      <div class="flex-1">
        <p class="text-xs font-extrabold uppercase tracking-[0.12em] text-kids-text/60">Lượt luyện: {{ word }}</p>
        <h2 class="mt-1 text-2xl font-extrabold text-kids-text">Rất tốt! Bé đã hoàn thành lượt luyện tập.</h2>
        <p class="mt-2 text-sm leading-6 text-kids-text/70">
          Đừng lo nếu chưa phát âm hoàn toàn chính xác. Bé có thể luyện thêm một lần nữa nhé!
        </p>
      </div>
    </div>

    <div class="mt-5 rounded-2xl border border-kids-text/10 bg-white p-4">
      <div class="flex items-center justify-between gap-3 text-sm">
        <span class="font-semibold text-kids-text">Mức hoàn thành lượt luyện (mô phỏng)</span>
        <span class="font-extrabold text-kids-text">{{ score }}%</span>
      </div>
      <div class="mt-2 h-3 overflow-hidden rounded-full bg-kids-text/10" role="progressbar" :aria-valuenow="score" aria-valuemin="0" aria-valuemax="100" aria-label="Điểm mô phỏng">
        <div class="h-full rounded-full bg-feedback-success transition-[width] duration-500" :style="{ width: `${score}%` }"></div>
      </div>
      <p class="mt-3 text-xs leading-5 text-kids-text/60">
        Kết quả chỉ mang tính minh họa trong phiên bản trải nghiệm. Chưa phải kết quả phân tích từ mô hình AI.
      </p>
    </div>

    <div class="mt-5 flex flex-col gap-3 sm:flex-row">
      <button type="button" class="min-h-12 rounded-xl border border-kids-text/15 bg-white px-5 text-sm font-bold text-kids-text transition hover:bg-kids-bg" @click="$emit('retry')">
        Luyện lại từ này
      </button>
      <button type="button" class="min-h-12 rounded-xl bg-kids-cta px-5 text-sm font-bold text-white transition hover:brightness-95" @click="$emit('next')">
        Chuyển sang từ tiếp theo
      </button>
    </div>
  </section>
</template>
