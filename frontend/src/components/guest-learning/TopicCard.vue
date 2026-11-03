<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  topic: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <RouterLink
    :to="{ name: 'GuestLearningTopic', params: { topicSlug: topic.slug } }"
    class="group flex h-full flex-col overflow-hidden rounded-3xl border border-kids-text/10 bg-white p-3 shadow-sm transition duration-200 hover:-translate-y-1 hover:border-kids-secondary/60 hover:shadow-lg focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
  >
    <div class="relative flex h-44 items-center justify-center overflow-hidden rounded-2xl p-4" :class="topic.colorClass">
      <img :src="topic.image" :alt="topic.imageAlt" class="h-full w-full object-contain transition-transform duration-300 group-hover:scale-105" loading="lazy" />
      <span class="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs font-extrabold text-kids-text">
        {{ String(topic.id).padStart(2, '0') }}
      </span>
      <span class="absolute bottom-3 right-3 flex h-11 w-11 items-center justify-center rounded-full bg-white text-2xl shadow-sm" aria-hidden="true">
        {{ topic.icon }}
      </span>
    </div>

    <div class="flex flex-1 flex-col p-3 sm:p-4">
      <h2 class="text-lg font-extrabold text-kids-text">{{ topic.title }}</h2>
      <p class="mt-2 flex-1 text-sm leading-6 text-kids-text/70">{{ topic.description }}</p>
      <div class="mt-5 flex items-center justify-between gap-3">
        <span class="text-xs font-semibold text-kids-text/60">{{ topic.words.length }} từ vựng</span>
        <span class="inline-flex items-center gap-1 text-sm font-bold text-kids-text transition-colors group-hover:text-kids-secondary">
          Khám phá ngay
          <svg viewBox="0 0 20 20" class="h-4 w-4 fill-none stroke-current" stroke-width="1.8" aria-hidden="true">
            <path d="M4 10h12m-5-5 5 5-5 5" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </span>
      </div>
    </div>
  </RouterLink>
</template>
