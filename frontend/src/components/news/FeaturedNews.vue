<script setup>
import { ArrowRight, Clock3, Sparkles } from '@lucide/vue'
import { RouterLink } from 'vue-router'
import { formatNewsDate } from './newsFormat.js'

defineProps({ article: { type: Object, required: true } })
</script>

<template>
  <section class="mx-auto max-w-screen-xl px-5 pt-10 sm:px-8 sm:pt-14">
    <div class="mb-5 flex items-center justify-between gap-3">
      <div><p class="text-xs font-bold uppercase tracking-[0.16em] text-kids-cta">Đáng chú ý</p><h2 class="mt-1 text-2xl font-extrabold text-kids-text">Bài viết nổi bật</h2></div>
      <span class="hidden items-center gap-1.5 rounded-full bg-kids-primary/20 px-3 py-1.5 text-xs font-bold text-kids-text sm:inline-flex"><Sparkles :size="15" />Được chọn cho ba mẹ</span>
    </div>
    <RouterLink :to="{ name: 'NewsDetail', params: { slug: article.slug } }" class="group grid overflow-hidden rounded-3xl border border-kids-text/10 bg-white shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-lg lg:grid-cols-[1.05fr_0.95fr]">
      <div class="relative flex aspect-[16/10] items-center justify-center overflow-hidden bg-kids-secondary/10 p-8 sm:aspect-[16/9] lg:aspect-auto lg:min-h-[350px]">
        <img :src="article.thumbnail" :alt="article.title" class="h-full max-h-80 w-full object-contain transition-transform duration-500 group-hover:scale-105" />
        <span class="absolute left-5 top-5 rounded-full bg-white/95 px-3 py-1.5 text-xs font-bold text-kids-text shadow-sm">{{ article.category }}</span>
      </div>
      <div class="flex flex-col justify-center p-6 sm:p-9 lg:p-10">
        <span class="text-sm font-bold text-kids-cta">Bài viết mới nhất</span>
        <h3 class="mt-3 text-2xl font-extrabold leading-tight text-kids-text transition-colors group-hover:text-kids-cta sm:text-3xl">{{ article.title }}</h3>
        <p class="mt-4 line-clamp-3 text-sm leading-7 text-kids-text/70 sm:text-base">{{ article.excerpt }}</p>
        <div class="mt-6 flex flex-wrap items-center gap-x-5 gap-y-2 text-xs font-medium text-kids-text/55"><span>{{ formatNewsDate(article.publishedAt) }}</span><span class="inline-flex items-center gap-1.5"><Clock3 :size="15" />{{ article.readTime }} phút đọc</span></div>
        <span class="mt-7 inline-flex items-center gap-2 text-sm font-extrabold text-kids-text transition-colors group-hover:text-kids-cta">Đọc bài viết <ArrowRight :size="18" class="transition-transform group-hover:translate-x-1" /></span>
      </div>
    </RouterLink>
  </section>
</template>
