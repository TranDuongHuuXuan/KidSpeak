<script setup>
defineProps({
  words: { type: Array, required: true },
  currentIndex: { type: Number, required: true },
  practicedIds: { type: Array, required: true },
})

const emit = defineEmits(['select', 'previous', 'next'])
</script>

<template>
  <section class="rounded-3xl border border-kids-text/10 bg-white p-5 shadow-sm sm:p-6" aria-label="Danh sách từ vựng">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h2 class="text-lg font-extrabold text-kids-text">Chọn từ muốn luyện</h2>
        <p class="mt-1 text-xs text-kids-text/60">Bé có thể chọn bất kỳ từ nào, không cần theo thứ tự.</p>
      </div>
      <div class="flex gap-2">
        <button
          type="button"
          class="min-h-11 rounded-xl border border-kids-text/10 px-4 text-sm font-bold text-kids-text transition hover:bg-kids-bg disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="currentIndex === 0"
          @click="emit('previous')"
        >
          Từ trước
        </button>
        <button
          type="button"
          class="min-h-11 rounded-xl bg-kids-secondary/25 px-4 text-sm font-bold text-kids-text transition hover:bg-kids-secondary/40 disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="currentIndex === words.length - 1"
          @click="emit('next')"
        >
          Từ tiếp theo
        </button>
      </div>
    </div>

    <div class="mt-5 grid grid-cols-5 gap-2 sm:grid-cols-10">
      <button
        v-for="(word, index) in words"
        :key="word.id"
        type="button"
        class="relative flex min-h-16 cursor-pointer items-center justify-center rounded-xl border px-1 transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary sm:min-h-24"
        :class="[
          currentIndex === index
            ? 'border-kids-secondary bg-kids-secondary/20 text-kids-text'
            : 'border-kids-text/10 bg-white text-kids-text/75 hover:bg-kids-bg',
        ]"
        :aria-current="currentIndex === index ? 'step' : undefined"
        :aria-label="`${word.word}${practicedIds.includes(word.id) ? ', đã luyện' : ', chưa luyện'}`"
        @click="emit('select', index)"
      >
        <img v-if="word.hasSpecificImage" :src="word.image" alt="" class="h-14 w-full object-contain sm:h-20" loading="lazy" />
        <span v-else class="px-1 text-center text-xs font-bold sm:text-sm">{{ word.word }}</span>
        <span v-if="practicedIds.includes(word.id)" class="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-feedback-success text-[10px] text-white" aria-label="Đã luyện">
          ✓
        </span>
      </button>
    </div>
  </section>
</template>
