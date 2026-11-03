<script setup>
import { ArrowRight, Clock3 } from '@lucide/vue'
import { RouterLink } from 'vue-router'
import { formatNewsDate } from './newsFormat.js'

defineProps({ article: { type: Object, required: true } })
</script>

<template>
  <RouterLink :to="{ name: 'NewsDetail', params: { slug: article.slug } }" class="group flex h-full flex-col overflow-hidden rounded-2xl border border-kids-text/10 bg-white shadow-sm transition duration-300 hover:-translate-y-1 hover:border-kids-secondary/50 hover:shadow-lg focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/30">
    <div class="relative aspect-[16/10] overflow-hidden bg-kids-bg p-5">
      <img :src="article.thumbnail" :alt="article.title" loading="lazy" class="h-full w-full object-contain transition-transform duration-500 group-hover:scale-105" />
      <span class="absolute left-4 top-4 rounded-full bg-white/95 px-3 py-1.5 text-[11px] font-bold text-kids-text shadow-sm">{{ article.category }}</span>
    </div>
    <div class="flex flex-1 flex-col p-5">
      <div class="flex items-center gap-2 text-xs font-medium text-kids-text/50"><span>{{ formatNewsDate(article.publishedAt) }}</span><span aria-hidden="true">·</span><span class="inline-flex items-center gap-1"><Clock3 :size="13" />{{ article.readTime }} phút đọc</span></div>
      <h3 class="mt-3 line-clamp-2 min-h-[3.5rem] text-lg font-extrabold leading-7 text-kids-text transition-colors group-hover:text-kids-cta">{{ article.title }}</h3>
      <p class="mt-2 line-clamp-3 flex-1 text-sm leading-6 text-kids-text/65">{{ article.excerpt }}</p>
      <span class="mt-5 inline-flex items-center gap-2 text-sm font-bold text-kids-text transition-colors group-hover:text-kids-cta">Đọc thêm <ArrowRight :size="16" class="transition-transform group-hover:translate-x-1" /></span>
    </div>
  </RouterLink>
</template>
