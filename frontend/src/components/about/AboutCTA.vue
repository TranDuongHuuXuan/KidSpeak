<script setup>
import { RouterLink } from 'vue-router'
import familyImage from '../../assets/images/home/parent.svg'
</script>

<template>
  <section class="bg-kids-bg px-5 py-14 sm:px-8 sm:py-20">
    <div class="mx-auto grid max-w-screen-xl items-center gap-8 overflow-hidden rounded-[2rem] bg-kids-secondary/20 px-6 py-8 sm:px-10 lg:grid-cols-[1fr_0.7fr] lg:px-14 lg:py-10">
      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-text/65">Cùng đồng hành</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Cùng KidSpeak tạo nên hành trình học tập tích cực cho bé!
        </h2>
        <p class="mt-4 max-w-2xl leading-7 text-kids-text/75">
          Bắt đầu khám phá những hoạt động luyện phát âm thân thiện và đồng hành cùng bé mỗi ngày.
        </p>
        <RouterLink
          :to="{ name: 'Register' }"
          class="mt-6 inline-flex min-h-12 items-center justify-center rounded-xl bg-kids-cta px-6 text-sm font-bold text-white transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-cta/30"
        >
          Bắt đầu trải nghiệm
        </RouterLink>
      </div>
      <img
        :src="familyImage"
        alt="Minh họa gia đình đồng hành cùng trẻ"
        class="mx-auto h-auto max-h-64 w-full max-w-sm object-contain"
        loading="lazy"
      />
    </div>
  </section>
</template>
