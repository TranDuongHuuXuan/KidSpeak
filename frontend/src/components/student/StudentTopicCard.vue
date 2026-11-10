<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  topic: { type: Object, required: true },
  showRecommended: { type: Boolean, default: true },
  actionLabel: { type: String, default: '' },
})

const emit = defineEmits(['open', 'favorite', 'star'])
</script>

<template>
  <article class="group flex h-full flex-col overflow-hidden rounded-2xl border border-amber-100 bg-white shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">
    <div class="relative h-44 overflow-hidden bg-kids-bg">
      <img :src="topic.image" :alt="topic.imageAlt" class="h-full w-full object-cover transition duration-300 group-hover:scale-105" loading="lazy" />
      <span class="absolute left-3 top-3 rounded-full bg-white/95 px-3 py-1 text-[11px] font-bold text-slate-600 shadow-sm">{{ topic.level }}</span>
      <div class="absolute right-3 top-3 flex gap-2">
        <button
          type="button"
          class="flex h-9 w-9 items-center justify-center rounded-full bg-white/95 shadow-sm transition hover:scale-105"
          :class="topic.isFavorite ? 'text-rose-500' : 'text-slate-500 hover:text-rose-500'"
          :aria-label="topic.isFavorite ? `Bỏ yêu thích ${topic.title}` : `Yêu thích ${topic.title}`"
          :aria-pressed="topic.isFavorite"
          @click="emit('favorite', topic.slug)"
        ><AdminIcon name="heart" :size="18" /></button>
        <button
          type="button"
          class="flex h-9 w-9 items-center justify-center rounded-full bg-white/95 shadow-sm transition hover:scale-105"
          :class="topic.isStarred ? 'text-amber-500' : 'text-slate-500 hover:text-amber-500'"
          :aria-label="topic.isStarred ? `Bỏ đánh dấu sao ${topic.title}` : `Đánh dấu sao ${topic.title}`"
          :aria-pressed="topic.isStarred"
          @click="emit('star', topic.slug)"
        ><AdminIcon name="star" :size="18" /></button>
      </div>
      <span v-if="showRecommended && topic.isRecommended" class="absolute bottom-3 left-3 inline-flex items-center gap-1 rounded-full bg-amber-100 px-2.5 py-1 text-[10px] font-extrabold text-amber-900">
        <AdminIcon name="sparkles" :size="13" /> Gợi ý cho con
      </span>
    </div>

    <div class="flex flex-1 flex-col p-4">
      <div class="flex items-start justify-between gap-2">
        <h3 class="font-extrabold leading-6 text-kids-text">{{ topic.title }}</h3>
        <span class="shrink-0 rounded-full px-2.5 py-1 text-[10px] font-bold" :class="topic.progress.status === 'completed' ? 'bg-emerald-50 text-emerald-700' : topic.progress.status === 'in-progress' ? 'bg-sky-50 text-sky-700' : 'bg-slate-100 text-slate-500'">
          {{ topic.progress.status === 'completed' ? 'Hoàn thành' : topic.progress.status === 'in-progress' ? 'Đang học' : 'Chưa học' }}
        </span>
      </div>
      <p class="mt-2 line-clamp-2 min-h-10 text-xs leading-5 text-slate-500">{{ topic.description }}</p>
      <div class="mt-4 flex items-center justify-between text-xs text-slate-500">
        <span>{{ topic.wordCount }} từ vựng</span>
        <span>{{ topic.progress.completed }}/{{ topic.wordCount }} từ đã học</span>
      </div>
      <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="topic.progress.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${topic.title}`">
        <div class="h-full rounded-full bg-gradient-to-r from-kids-secondary to-sky-500 transition-all" :style="{ width: `${topic.progress.progress}%` }"></div>
      </div>
      <button type="button" class="mt-4 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-kids-primary px-4 text-sm font-extrabold text-kids-text transition hover:bg-amber-400" @click="emit('open', topic)">
        {{ actionLabel || (topic.progress.started ? 'Tiếp tục học' : 'Bắt đầu học') }} <AdminIcon name="arrow" :size="16" />
      </button>
    </div>
  </article>
</template>
