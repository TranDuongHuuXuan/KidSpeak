<script setup>
import childImage from '../../assets/images/home/child.svg'
import parentImage from '../../assets/images/home/parent.svg'
import teacherImage from '../../assets/images/home/teacher.svg'

const audiences = [
  {
    title: 'Trẻ em',
    description: 'Thực hành phát âm thông qua các hoạt động gần gũi, khuyến khích sự tự tin khi giao tiếp.',
    image: childImage,
    alt: 'Minh họa trẻ em đang học tập',
  },
  {
    title: 'Phụ huynh',
    description: 'Đồng hành cùng con trong các buổi luyện tập và quan sát quá trình thực hành.',
    image: parentImage,
    alt: 'Minh họa phụ huynh đồng hành cùng trẻ',
  },
  {
    title: 'Giáo viên',
    description: 'Tham khảo hoạt động luyện tập để hỗ trợ học viên và phối hợp với gia đình.',
    image: teacherImage,
    alt: 'Minh họa giáo viên hướng dẫn học viên',
  },
]
</script>

<template>
  <section class="bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-2xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Cùng nhau đồng hành</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">KidSpeak dành cho ai?</h2>
      </div>

      <div class="mt-12 grid gap-5 md:grid-cols-3">
        <article
          v-for="audience in audiences"
          :key="audience.title"
          class="rounded-3xl border border-kids-text/10 bg-white p-5 text-center transition duration-200 hover:-translate-y-1 hover:shadow-lg sm:p-6"
        >
          <div class="mx-auto flex h-48 items-center justify-center rounded-2xl bg-kids-bg p-3">
            <img :src="audience.image" :alt="audience.alt" class="h-full w-full object-contain" loading="lazy" />
          </div>
          <h3 class="mt-5 text-xl font-bold text-kids-text">{{ audience.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ audience.description }}</p>
        </article>
      </div>
    </div>
  </section>
</template>
