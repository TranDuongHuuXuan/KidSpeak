<script setup>
import { RouterLink } from 'vue-router'
import { learningTopics } from '../../data/learningTopics'
import TopicCard from './TopicCard.vue'
</script>

<template>
  <section class="bg-kids-bg px-5 py-12 sm:px-8 sm:py-16 lg:py-20">
    <div class="mx-auto max-w-screen-2xl">
      <div class="mx-auto max-w-3xl text-center">
        <p class="inline-flex rounded-full bg-kids-secondary/15 px-4 py-2 text-xs font-extrabold tracking-[0.12em] text-kids-text sm:text-sm">
          GÓC HỌC TẬP KIDSPEAK
        </p>
        <h1 class="mt-5 text-4xl font-extrabold leading-tight text-kids-text sm:text-5xl">
          Cùng bé khám phá thế giới phát âm!
        </h1>
        <p class="mt-5 text-base leading-7 text-kids-text/70 sm:text-lg">
          Chọn một chủ đề yêu thích và bắt đầu hành trình luyện phát âm qua những hình ảnh
          và hoạt động học tập thú vị.
        </p>
        <p class="mt-5 inline-flex items-center gap-2 rounded-full border border-feedback-success/20 bg-feedback-success/10 px-4 py-2 text-sm font-semibold text-kids-text">
          <svg viewBox="0 0 20 20" class="h-5 w-5 fill-none stroke-feedback-success" stroke-width="1.8" aria-hidden="true">
            <path d="m5 10 3.2 3.2L15.5 6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          Bạn có thể trải nghiệm các bài học miễn phí mà không cần đăng nhập.
        </p>
      </div>

      <div v-if="learningTopics.length" class="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
        <TopicCard v-for="topic in learningTopics" :key="topic.id" :topic="topic" />
      </div>
      <div v-else class="mt-10 rounded-3xl border border-kids-text/10 bg-white p-10 text-center">
        <p class="font-semibold text-kids-text">Chủ đề đang được chuẩn bị. Bạn hãy quay lại sau nhé.</p>
      </div>

      <div class="mt-10 text-center">
        <RouterLink to="/" class="text-sm font-semibold text-kids-text/70 underline decoration-kids-secondary underline-offset-4 hover:text-kids-text">
          Quay về trang chủ
        </RouterLink>
      </div>
    </div>
  </section>
</template>
