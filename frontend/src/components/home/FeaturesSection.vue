<script setup>
import pronunciationImage from '../../assets/images/home/feature-pronunciation.svg'
import aiImage from '../../assets/images/home/feature-ai.svg'
import progressImage from '../../assets/images/home/feature-progress.svg'
import teacherImage from '../../assets/images/home/feature-teacher.svg'

const features = [
  {
    title: 'Luyện phát âm tương tác',
    description: 'Thực hành theo các bài tập sinh động, phù hợp với nhịp độ của từng bé.',
    image: pronunciationImage,
    alt: 'Minh họa hoạt động luyện phát âm',
  },
  {
    title: 'AI hỗ trợ phân tích giọng nói',
    description: 'Công cụ hỗ trợ đưa ra thông tin tham khảo sau khi trẻ thực hành và ghi âm.',
    image: aiImage,
    alt: 'Minh họa công nghệ hỗ trợ phân tích giọng nói',
  },
  {
    title: 'Theo dõi tiến độ luyện tập',
    description: 'Ghi nhận hoạt động luyện tập để gia đình cùng trẻ nhìn lại hành trình.',
    image: progressImage,
    alt: 'Minh họa theo dõi tiến độ học tập',
  },
  {
    title: 'Hỗ trợ giáo viên',
    description: 'Hỗ trợ giáo viên tham khảo hoạt động và kết quả luyện tập của học viên.',
    image: teacherImage,
    alt: 'Minh họa giáo viên hỗ trợ học viên',
  },
]
</script>

<template>
  <section id="research" class="scroll-mt-24 bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-2xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Học tập chủ động</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">Những tính năng nổi bật</h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Công cụ hỗ trợ trẻ, phụ huynh và giáo viên cùng tham gia vào hành trình luyện tập.
        </p>
      </div>

      <div class="mt-12 grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        <article
          v-for="(feature, index) in features"
          :key="feature.title"
          class="group overflow-hidden rounded-3xl border border-kids-text/10 bg-kids-bg/60 p-5 transition duration-200 hover:-translate-y-1 hover:border-kids-secondary/50 hover:bg-white hover:shadow-lg"
        >
          <div class="flex h-44 items-center justify-center rounded-2xl bg-white p-3">
            <img :src="feature.image" :alt="feature.alt" class="h-full w-full object-contain" loading="lazy" />
          </div>
          <span class="mt-5 inline-flex h-8 w-8 items-center justify-center rounded-lg bg-kids-primary/40 text-sm font-extrabold">
            {{ index + 1 }}
          </span>
          <h3 class="mt-3 text-lg font-bold text-kids-text">{{ feature.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ feature.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
