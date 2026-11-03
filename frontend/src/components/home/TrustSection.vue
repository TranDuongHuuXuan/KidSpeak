<script setup>
const technologies = [
  {
    name: 'Vue.js',
    mark: 'V',
    description: 'Xây dựng giao diện tương tác.',
  },
  {
    name: 'FastAPI',
    mark: 'API',
    description: 'Cung cấp backend API.',
  },
  {
    name: 'PostgreSQL',
    mark: 'PG',
    description: 'Lưu trữ dữ liệu hệ thống.',
  },
  {
    name: 'MinIO',
    mark: 'M',
    description: 'Lưu trữ tệp media.',
  },
]
</script>

<template>
  <section class="bg-white py-14 sm:py-16">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">
          Technology Behind KidSpeak
        </p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Cam kết xây dựng trải nghiệm học tập đáng tin cậy.
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Được xây dựng trên nền tảng công nghệ hiện đại, hỗ trợ trải nghiệm học tập và phân tích phát âm.
        </p>
      </div>

      <div class="mt-9 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <article
          v-for="technology in technologies"
          :key="technology.name"
          class="flex items-center gap-4 rounded-2xl border border-kids-text/10 bg-kids-bg/50 p-4 transition-colors duration-200 hover:border-kids-secondary/50 hover:bg-white"
        >
          <span class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-kids-secondary/15 text-sm font-extrabold tracking-tight text-kids-text" aria-hidden="true">
            {{ technology.mark }}
          </span>
          <div>
            <h3 class="font-bold text-kids-text">{{ technology.name }}</h3>
            <p class="mt-1 text-xs leading-5 text-kids-text/65">{{ technology.description }}</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
