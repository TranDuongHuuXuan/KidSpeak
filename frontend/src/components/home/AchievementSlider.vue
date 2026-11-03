```vue
<script setup>
import childImage from '../../assets/images/home/child.svg'
import pronunciationImage from '../../assets/images/home/feature-pronunciation.svg'
import teacherImage from '../../assets/images/home/teacher.svg'
import parentImage from '../../assets/images/home/parent.svg'
import learningImage from '../../assets/images/home/app-download.svg'

const highlights = [
  {
    image: pronunciationImage,
    alt: 'Minh họa trẻ luyện phát âm',
    caption: 'Khơi gợi hứng thú luyện phát âm',
  },
  {
    image: childImage,
    alt: 'Minh họa trẻ khám phá hoạt động học tập',
    caption: 'Tạo không gian học tập thân thiện',
  },
  {
    image: teacherImage,
    alt: 'Minh họa giáo viên hướng dẫn trẻ',
    caption: 'Khuyến khích giáo viên đồng hành',
  },
  {
    image: parentImage,
    alt: 'Minh họa phụ huynh đồng hành cùng trẻ',
    caption: 'Gia đình cùng khích lệ bé',
  },
  {
    image: learningImage,
    alt: 'Minh họa trải nghiệm học tập trên thiết bị số',
    caption: 'Từng bước xây dựng trải nghiệm số',
  },
  {
    image: childImage,
    alt: 'Minh họa trẻ học tập vui vẻ',
    caption: 'Khám phá kiến thức qua hình ảnh',
  },
  {
    image: pronunciationImage,
    alt: 'Minh họa hoạt động luyện tập phát âm',
    caption: 'Luyện tập phát âm mỗi ngày',
  },
  {
    image: teacherImage,
    alt: 'Minh họa giáo viên hỗ trợ học sinh',
    caption: 'Tăng cường sự đồng hành của giáo viên',
  },
  {
    image: parentImage,
    alt: 'Minh họa gia đình khích lệ trẻ',
    caption: 'Xây dựng thói quen học tập tại nhà',
  },
  {
    image: learningImage,
    alt: 'Minh họa nền tảng học tập trực tuyến',
    caption: 'Phát triển trải nghiệm học tập số',
  },
]
</script>

<template>
  <section class="overflow-hidden bg-kids-bg py-14 sm:py-16">
    <div class="mx-auto max-w-screen-2xl px-5 text-center sm:px-8 lg:px-12">
      <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">
        Hành trình KidSpeak
      </p>

      <h2 class="mt-3 text-2xl font-extrabold leading-tight text-kids-text sm:text-3xl">
        KidSpeak – Hành trình kiến tạo trải nghiệm học tập.
      </h2>

      <p class="mx-auto mt-3 max-w-3xl text-sm leading-6 text-kids-text/70 sm:text-base">
        Cùng nhìn lại những giá trị và bước tiến trong quá trình xây dựng nền tảng luyện phát âm.
        Hình ảnh dưới đây là minh họa cho hoạt động và định hướng sản phẩm,
        không phải ảnh sự kiện thực tế.
      </p>
    </div>

    <div class="achievement-marquee mt-10 w-full overflow-hidden">
      <div class="achievement-marquee__track flex w-max">
        <!-- Nhóm ảnh thứ nhất -->
        <ul class="achievement-marquee__group flex shrink-0 items-stretch gap-5 pr-5 sm:gap-6 sm:pr-6">
          <li
            v-for="(highlight, index) in highlights"
            :key="`first-${index}`"
            class="w-64 shrink-0 overflow-hidden rounded-3xl border border-kids-text/10 bg-white p-3 shadow-sm transition-shadow duration-300 hover:shadow-lg sm:w-72"
          >
            <div class="flex h-48 items-center justify-center rounded-2xl bg-kids-secondary/10 p-4 sm:h-52">
              <img
                :src="highlight.image"
                :alt="highlight.alt"
                class="h-full w-full object-contain"
                loading="lazy"
                draggable="false"
              />
            </div>

            <p class="px-2 py-4 text-sm font-semibold text-kids-text">
              {{ highlight.caption }}
            </p>
          </li>
        </ul>

        <!-- Nhóm ảnh thứ hai: nhân đôi để tạo vòng lặp liên tục -->
        <ul
          class="achievement-marquee__group flex shrink-0 items-stretch gap-5 pr-5 sm:gap-6 sm:pr-6"
          aria-hidden="true"
        >
          <li
            v-for="(highlight, index) in highlights"
            :key="`second-${index}`"
            class="w-64 shrink-0 overflow-hidden rounded-3xl border border-kids-text/10 bg-white p-3 shadow-sm sm:w-72"
          >
            <div class="flex h-48 items-center justify-center rounded-2xl bg-kids-secondary/10 p-4 sm:h-52">
              <img
                :src="highlight.image"
                alt=""
                class="h-full w-full object-contain"
                loading="lazy"
                draggable="false"
              />
            </div>

            <p class="px-2 py-4 text-sm font-semibold text-kids-text">
              {{ highlight.caption }}
            </p>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.achievement-marquee__track {
  animation: achievement-marquee 45s linear infinite;
  will-change: transform;
}

.achievement-marquee:hover .achievement-marquee__track {
  animation-play-state: paused;
}

@keyframes achievement-marquee {
  from {
    transform: translateX(0);
  }

  to {
    transform: translateX(-50%);
  }
}

</style>
