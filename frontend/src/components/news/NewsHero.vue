<script setup>
import heroImage from '../../assets/images/home/child.svg'
</script>

<template>
  <section class="relative overflow-hidden border-b border-kids-text/5 bg-gradient-to-br from-kids-primary/15 via-kids-bg to-kids-secondary/15">
    <div class="mx-auto grid max-w-screen-xl items-center gap-6 px-5 py-10 sm:px-8 sm:py-14 lg:grid-cols-[1.1fr_0.9fr] lg:gap-10 lg:py-16">
      <div class="relative z-10">
        <span class="inline-flex items-center gap-2 rounded-full border border-kids-secondary/25 bg-white/80 px-3 py-1.5 text-xs font-bold uppercase tracking-wider text-kids-text/65">
          <span class="h-2 w-2 rounded-full bg-kids-secondary"></span>Góc chia sẻ KidSpeak
        </span>
        <h1 class="mt-4 max-w-2xl text-4xl font-extrabold leading-tight tracking-tight text-kids-text sm:text-5xl lg:text-[3.4rem]">Tin tức <span class="text-kids-cta">&amp; Cập nhật</span></h1>
        <p class="mt-4 max-w-2xl text-base leading-7 text-kids-text/70 sm:text-lg sm:leading-8">
          Cùng KidSpeak khám phá những kiến thức bổ ích, hoạt động mới và phương pháp giúp trẻ phát triển khả năng phát âm.
        </p>
        <a href="#news-list" class="mt-6 inline-flex min-h-11 items-center justify-center rounded-xl bg-kids-secondary px-5 py-2.5 text-sm font-bold text-kids-text shadow-sm transition hover:-translate-y-0.5 hover:shadow-md focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40">
          Khám phá bài viết <span class="ml-2" aria-hidden="true">↓</span>
        </a>
      </div>
      <div class="relative mx-auto flex w-full max-w-md items-center justify-center lg:max-w-lg">
        <div class="absolute h-64 w-64 rounded-full bg-kids-primary/20 blur-3xl sm:h-80 sm:w-80" aria-hidden="true"></div>
        <img :src="heroImage" alt="Bé vui vẻ học tập và luyện phát âm" class="relative z-10 h-56 w-full object-contain sm:h-72 lg:h-80" />
        <span class="absolute bottom-3 left-3 z-20 rounded-2xl border border-white/80 bg-white/90 px-4 py-2 text-sm font-bold text-kids-text shadow-md sm:bottom-5 sm:left-0">Mỗi ngày là cơ hội để con tiến bộ ✨</span>
      </div>
    </div>
  </section>
</template>
