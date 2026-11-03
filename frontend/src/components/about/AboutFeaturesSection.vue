<script setup>
import pronunciationImage from '../../assets/images/home/feature-pronunciation.svg'
import aiImage from '../../assets/images/home/feature-ai.svg'
import progressImage from '../../assets/images/home/feature-progress.svg'
import teacherImage from '../../assets/images/home/feature-teacher.svg'

const features = [
  {
    title: 'Luyện phát âm tương tác',
    description: 'Định hướng xây dựng các bài luyện trực quan để trẻ thực hành theo nội dung học tập.',
    status: 'Định hướng phát triển',
    image: pronunciationImage,
    alt: 'Minh họa trẻ luyện phát âm',
  },
  {
    title: 'AI hỗ trợ phân tích',
    description: 'AI service hiện chưa có endpoint xử lý âm thanh hoặc mô hình phân tích được nối với giao diện.',
    status: 'Chưa tích hợp',
    image: aiImage,
    alt: 'Minh họa phân tích giọng nói bằng công nghệ',
  },
  {
    title: 'Theo dõi tiến độ',
    description: 'Cơ sở dữ liệu có cấu trúc phiên luyện tập và kết quả; giao diện và API theo dõi chưa được triển khai.',
    status: 'Nền tảng dữ liệu',
    image: progressImage,
    alt: 'Minh họa theo dõi tiến độ học tập',
  },
  {
    title: 'Đồng hành cùng giáo viên',
    description: 'Hướng đến hỗ trợ phối hợp giữa gia đình và giáo viên trong quá trình trẻ luyện tập.',
    status: 'Định hướng phát triển',
    image: teacherImage,
    alt: 'Minh họa giáo viên hỗ trợ trẻ học tập',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Các hướng phát triển</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">KidSpeak hướng đến những trải nghiệm nào?</h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Các nội dung dưới đây phân biệt rõ định hướng sản phẩm với phần đã được triển khai trong mã nguồn hiện tại.
        </p>
      </div>

      <div class="mt-10 grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        <article
          v-for="feature in features"
          :key="feature.title"
          class="group rounded-3xl border border-kids-text/10 bg-kids-bg/60 p-5 transition duration-200 hover:-translate-y-1 hover:border-kids-secondary/50 hover:bg-white hover:shadow-lg"
        >
          <div class="flex h-40 items-center justify-center rounded-2xl bg-white p-3">
            <img :src="feature.image" :alt="feature.alt" class="h-full w-full object-contain" loading="lazy" />
          </div>
          <span class="mt-5 inline-flex rounded-full bg-kids-secondary/15 px-3 py-1 text-xs font-bold text-kids-text">
            {{ feature.status }}
          </span>
          <h3 class="mt-3 text-lg font-bold text-kids-text">{{ feature.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ feature.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
