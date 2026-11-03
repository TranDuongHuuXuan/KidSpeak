<script setup>
import { RouterLink } from 'vue-router'
import heroImage from '../../assets/images/introduce/about-hero.png'
</script>

<template>
  <section id="about" class="scroll-mt-24 overflow-hidden bg-kids-bg">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 py-14 sm:px-8 sm:py-20 lg:grid-cols-[1.05fr_0.95fr] lg:gap-16 lg:px-12 lg:py-24">
      <div>
        <p class="inline-flex items-center gap-2 rounded-full bg-kids-secondary/15 px-4 py-2 text-xs font-bold tracking-[0.12em] text-kids-text sm:text-sm">
          GIỚI THIỆU VỀ KIDSPEAK
        </p>
        <h1 class="mt-5 max-w-2xl text-4xl font-extrabold leading-tight text-kids-text sm:text-5xl lg:text-[3.4rem]">
          Đồng hành cùng bé trên hành trình phát âm rõ ràng và tự tin hơn.
        </h1>
        <p class="mt-6 max-w-2xl text-base leading-7 text-kids-text/75 sm:text-lg sm:leading-8">
          KidSpeak là dự án nền tảng hỗ trợ trẻ luyện phát âm thông qua các hoạt động học tập tương tác,
          với định hướng ứng dụng công nghệ hỗ trợ phân tích giọng nói.
        </p>
        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          <a
            href="#ai-technology"
            class="inline-flex min-h-12 items-center justify-center rounded-xl bg-kids-secondary px-6 text-sm font-bold text-kids-text transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
          >
            Khám phá cách hoạt động
          </a>
          <RouterLink
            :to="{ name: 'Register' }"
            class="inline-flex min-h-12 items-center justify-center rounded-xl border border-kids-text/15 bg-white px-6 text-sm font-bold text-kids-text transition hover:border-kids-secondary hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
          >
            Bắt đầu học
          </RouterLink>
        </div>
        <p class="mt-4 text-xs leading-5 text-kids-text/60">
          Trang đăng ký hiện có; các hoạt động luyện tập và phân tích giọng nói chưa được tích hợp vào giao diện hiện tại.
        </p>
      </div>

      <div class="relative mx-auto w-full max-w-xl">
        <div class="absolute -inset-4 rounded-[2.5rem] bg-kids-primary/20 blur-2xl" aria-hidden="true"></div>
        <div class="relative rounded-[2rem] border border-kids-text/5 bg-white p-4 shadow-sm sm:p-7">
          <img
            :src="heroImage"
            alt="Minh họa phụ huynh cùng trẻ học tập bên máy tính"
            class="h-auto max-h-[34rem] w-full object-contain"
            fetchpriority="high"
          />
          <p class="mt-2 text-center text-xs text-kids-text/55">Hình minh họa, không phải ảnh chụp giao diện KidSpeak.</p>
        </div>
      </div>
    </div>
  </section>
</template>
