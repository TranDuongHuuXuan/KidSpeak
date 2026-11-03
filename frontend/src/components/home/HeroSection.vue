<script setup>
import { RouterLink } from 'vue-router'
import heroImage from '../../assets/images/home/hero.svg'
</script>

<template>
  <section class="overflow-hidden bg-kids-bg">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-8 px-5 py-14 sm:px-8 sm:py-20 lg:grid-cols-2 lg:gap-12 lg:px-12 lg:py-24">
      <div class="relative z-10">
        <p class="mb-5 inline-flex rounded-full bg-kids-secondary/15 px-4 py-2 text-xs font-bold tracking-[0.12em] text-kids-text sm:text-sm">
          NỀN TẢNG HỖ TRỢ LUYỆN PHÁT ÂM
        </p>
        <h1 class="max-w-2xl text-4xl font-extrabold leading-tight tracking-tight text-kids-text sm:text-5xl lg:text-[3.5rem]">
          Cùng bé phát âm chuẩn – Tự tin giao tiếp mỗi ngày!
        </h1>
        <p class="mt-6 max-w-xl text-base leading-7 text-kids-text/75 sm:text-lg sm:leading-8">
          KidSpeak đồng hành cùng trẻ qua những bài luyện phát âm tương tác và công cụ hỗ trợ phân tích giọng nói, để mỗi buổi luyện tập thêm vui và dễ theo dõi.
        </p>
        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          <RouterLink
            :to="{ name: 'Register' }"
            class="inline-flex min-h-12 items-center justify-center rounded-2xl bg-kids-cta px-6 py-3 font-bold text-kids-text shadow-sm transition hover:-translate-y-0.5 hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/50 active:translate-y-0"
          >
            Bắt đầu trải nghiệm
          </RouterLink>
          <a
            href="#about"
            class="inline-flex min-h-12 items-center justify-center rounded-2xl border border-kids-text/15 bg-kids-surface px-6 py-3 font-semibold text-kids-text transition hover:border-kids-secondary hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
          >
            Khám phá KidSpeak
          </a>
        </div>
        <div class="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3 text-sm text-kids-text/70">
          <span class="inline-flex items-center gap-2">
            <span class="h-2.5 w-2.5 rounded-full bg-feedback-success"></span>
            Luyện tập theo nhịp độ riêng
          </span>
          <span class="inline-flex items-center gap-2">
            <span class="h-2.5 w-2.5 rounded-full bg-kids-primary"></span>
            Đồng hành cùng gia đình
          </span>
        </div>
      </div>

      <div class="relative mx-auto w-full max-w-2xl">
        <div class="absolute inset-8 rounded-[3rem] bg-kids-primary/20 blur-2xl"></div>
        <div class="relative overflow-hidden rounded-[2rem] bg-kids-surface p-3 shadow-xl sm:p-5">
          <img
            :src="heroImage"
            alt="Trẻ tham gia hoạt động học tập và luyện phát âm cùng giáo viên"
            class="h-auto max-h-[34rem] w-full rounded-[1.5rem] object-contain"
            fetchpriority="high"
          />
        </div>
        <div class="absolute -bottom-4 left-2 rounded-2xl border border-kids-text/5 bg-white px-4 py-3 shadow-lg sm:bottom-6 sm:-left-5 sm:px-5">
          <p class="text-xs font-medium text-kids-text/60">Mỗi ngày một chút</p>
          <p class="mt-0.5 text-sm font-bold text-kids-text">Cùng bé tự tin cất lời</p>
        </div>
        <div class="absolute -right-1 top-4 rounded-full bg-kids-primary px-4 py-2 text-xs font-bold text-kids-text shadow-md sm:-right-4 sm:top-10 sm:text-sm">
          Học mà chơi
        </div>
      </div>
    </div>
  </section>
</template>
