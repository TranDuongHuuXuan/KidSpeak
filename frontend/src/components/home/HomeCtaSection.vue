<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section id="contact" class="scroll-mt-24 bg-kids-bg px-5 py-14 sm:px-8 sm:py-20">
    <div class="mx-auto max-w-5xl rounded-[2rem] bg-kids-primary/35 px-6 py-10 text-center sm:px-12 sm:py-14">
      <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-text/70">Cùng bắt đầu hôm nay</p>
      <h2 class="mx-auto mt-3 max-w-3xl text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
        Bắt đầu hành trình luyện phát âm cùng KidSpeak!
      </h2>
      <p class="mx-auto mt-4 max-w-2xl text-base leading-7 text-kids-text/75">
        Mỗi ngày một chút luyện tập, mỗi bước nhỏ là một hành trình tiến bộ.
      </p>
      <RouterLink
        :to="{ name: 'Register' }"
        class="mt-7 inline-flex min-h-12 items-center justify-center rounded-2xl bg-kids-cta px-7 py-3 font-bold text-kids-text shadow-sm transition hover:-translate-y-0.5 hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/50 active:translate-y-0"
      >
        Bắt đầu ngay
      </RouterLink>
    </div>
  </section>
</template>
