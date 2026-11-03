<script setup>
const technologies = [
  { name: 'Vue.js', mark: 'VUE' },
  { name: 'FastAPI', mark: 'API' },
  { name: 'PostgreSQL', mark: 'PG' },
  { name: 'MinIO', mark: 'MINIO' },
  { name: 'Tailwind CSS', mark: 'TW' },
  { name: 'Vite', mark: 'VITE' },
]
</script>

<template>
  <section class="overflow-hidden bg-kids-bg py-12 sm:py-14">
    <div class="mx-auto max-w-screen-2xl px-5 text-center sm:px-8 lg:px-12">
      <h2 class="text-2xl font-extrabold text-kids-text sm:text-3xl">
        Technology Behind KidSpeak
      </h2>
      <p class="mt-2 text-sm leading-6 text-kids-text/70 sm:text-base">
        Những công nghệ hỗ trợ xây dựng trải nghiệm học tập tương tác.
      </p>
    </div>

    <div class="technology-marquee mt-8 w-full overflow-hidden" aria-label="Công nghệ sử dụng trong KidSpeak">
      <div class="technology-marquee__track flex w-max">
        <ul class="technology-marquee__group flex shrink-0 items-center gap-4 pr-4 sm:gap-6 sm:pr-6">
          <li
            v-for="technology in technologies"
            :key="technology.name"
            class="flex h-[72px] w-40 shrink-0 items-center justify-center gap-3 rounded-2xl border border-kids-text/10 bg-white px-4 shadow-sm sm:w-48"
          >
            <span class="flex h-9 min-w-9 items-center justify-center rounded-lg bg-kids-secondary/15 px-2 text-xs font-extrabold tracking-tight text-kids-text" aria-hidden="true">
              {{ technology.mark }}
            </span>
            <span class="whitespace-nowrap text-sm font-semibold text-kids-text">{{ technology.name }}</span>
          </li>
        </ul>

        <ul
          class="technology-marquee__group technology-marquee__duplicate flex shrink-0 items-center gap-4 pr-4 sm:gap-6 sm:pr-6"
          aria-hidden="true"
        >
          <li
            v-for="technology in technologies"
            :key="technology.name"
            class="flex h-[72px] w-40 shrink-0 items-center justify-center gap-3 rounded-2xl border border-kids-text/10 bg-white px-4 shadow-sm sm:w-48"
          >
            <span class="flex h-9 min-w-9 items-center justify-center rounded-lg bg-kids-secondary/15 px-2 text-xs font-extrabold tracking-tight text-kids-text">
              {{ technology.mark }}
            </span>
            <span class="whitespace-nowrap text-sm font-semibold text-kids-text">{{ technology.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.technology-marquee__track {
  animation: technology-marquee 32s linear infinite;
}

.technology-marquee:hover .technology-marquee__track,
.technology-marquee:focus-within .technology-marquee__track {
  animation-play-state: paused;
}

@keyframes technology-marquee {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(-50%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .technology-marquee__track {
    animation: none;
  }

  .technology-marquee__duplicate {
    display: none;
  }
}
</style>
