<script setup>
defineProps({
  word: { type: Object, required: true },
})
</script>

<template>
  <aside class="rounded-3xl border border-kids-text/10 bg-white p-5 shadow-sm sm:p-6">
    <p class="text-xs font-bold uppercase tracking-[0.12em] text-kids-secondary">Mẹo luyện tập</p>
    <h2 class="mt-2 text-xl font-extrabold text-kids-text">Bé cùng luyện phát âm</h2>

    <div class="mt-5 flex items-center gap-4 rounded-2xl bg-kids-bg p-4">
      <div class="flex h-16 w-16 shrink-0 items-center justify-center rounded-full bg-kids-secondary/20" aria-hidden="true">
        <svg viewBox="0 0 48 48" class="h-10 w-10">
          <circle cx="24" cy="24" r="20" fill="#fff" />
          <circle cx="17" cy="20" r="1.8" fill="#263238" />
          <circle cx="31" cy="20" r="1.8" fill="#263238" />
          <path d="M16 29c2.4 3.2 5 4.8 8 4.8s5.6-1.6 8-4.8" fill="none" stroke="#ff7043" stroke-linecap="round" stroke-width="2.5" />
        </svg>
      </div>
      <div>
        <p class="text-sm font-bold text-kids-text">Hình minh họa khuôn mặt</p>
        <p class="mt-1 text-xs leading-5 text-kids-text/60">Chưa có hình khẩu hình chuyên biệt cho từng âm.</p>
      </div>
    </div>

    <div class="mt-4 space-y-3">
      <div class="rounded-2xl bg-kids-bg/70 p-4">
        <h3 class="text-sm font-bold text-kids-text">Đọc từng tiếng</h3>
        <div class="mt-2 flex flex-wrap gap-2">
          <span v-for="(syllable, index) in word.word.split(/\s+/)" :key="`${syllable}-${index}`" class="rounded-lg bg-white px-3 py-1.5 text-sm font-semibold text-kids-text">
            {{ syllable }}
          </span>
        </div>
        <p class="mt-2 text-xs leading-5 text-kids-text/60">Đây là cách tách tiếng theo khoảng trắng, không phải phiên âm âm vị.</p>
      </div>

      <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
        <div class="rounded-2xl border border-kids-text/10 p-4">
          <h3 class="text-sm font-bold text-kids-text">Môi và lưỡi</h3>
          <p class="mt-1 text-sm leading-6 text-kids-text/70">{{ word.pronunciationGuide }}</p>
        </div>
        <div class="rounded-2xl border border-kids-text/10 p-4">
          <h3 class="text-sm font-bold text-kids-text">Mẹo nhỏ</h3>
          <p class="mt-1 text-sm leading-6 text-kids-text/70">{{ word.tips }}</p>
        </div>
      </div>
    </div>

    <div class="mt-4 rounded-xl bg-kids-secondary/10 px-4 py-3 text-xs leading-5 text-kids-text/70">
      Âm thanh mẫu đang được cập nhật. Minh họa và hướng dẫn hiện tại chỉ hỗ trợ trải nghiệm, không thay thế hướng dẫn chuyên môn.
    </div>
  </aside>
</template>
