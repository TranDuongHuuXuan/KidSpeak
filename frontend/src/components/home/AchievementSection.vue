<script setup>
import platformImage from '../../assets/images/home/about-kidspeak.png'
import practiceImage from '../../assets/images/home/feature-pronunciation.svg'
import familyImage from '../../assets/images/home/parent.svg'
import speechImage from '../../assets/images/home/feature-ai.svg'

const milestones = [
  {
    number: '01',
    status: 'Đã thực hiện',
    statusClass: 'bg-feedback-success/10 text-feedback-success',
    title: 'Phát triển nền tảng học tập',
    description:
      'Đã xây dựng website KidSpeak với trang chủ và các khu vực thông tin, đăng nhập, đăng ký. Đây là cột mốc sản phẩm trong dự án, không phải thành tích bên ngoài.',
    image: platformImage,
    alt: 'Minh họa nền tảng học tập KidSpeak',
  },
  {
    number: '02',
    status: 'Đang phát triển',
    statusClass: 'bg-kids-primary/20 text-kids-text',
    title: 'Hoàn thiện trải nghiệm luyện tập',
    description:
      'Từng bước hoàn thiện nội dung và trải nghiệm luyện phát âm tương tác, hướng đến môi trường học tập trực quan, thân thiện với trẻ.',
    image: practiceImage,
    alt: 'Minh họa hoạt động luyện phát âm',
  },
  {
    number: '03',
    status: 'Mục tiêu tương lai',
    statusClass: 'bg-kids-secondary/15 text-kids-text',
    title: 'Đồng hành cùng gia đình và giáo viên',
    description:
      'Hướng đến khả năng hỗ trợ phụ huynh và giáo viên theo dõi quá trình luyện tập, tăng sự phối hợp trong hành trình học của trẻ.',
    image: familyImage,
    alt: 'Minh họa gia đình đồng hành cùng trẻ',
  },
  {
    number: '04',
    status: 'Định hướng phát triển',
    statusClass: 'bg-kids-cta/10 text-kids-text',
    title: 'Nghiên cứu hỗ trợ phân tích giọng nói',
    description:
      'Định hướng phát triển công cụ hỗ trợ phân tích giọng nói và phản hồi phù hợp. Hiện chưa công bố số liệu về độ chính xác hay hiệu quả.',
    image: speechImage,
    alt: 'Minh họa công cụ hỗ trợ phân tích giọng nói',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">
          Các cột mốc sản phẩm
        </p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Những bước tiến trên hành trình phát triển KidSpeak.
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Mỗi bước phát triển đều hướng đến mục tiêu xây dựng môi trường luyện phát âm thân thiện,
          giúp trẻ tự tin hơn trong giao tiếp.
        </p>
      </div>

      <div class="mt-10 grid gap-5 sm:grid-cols-2 xl:mt-12">
        <article
          v-for="milestone in milestones"
          :key="milestone.number"
          class="group grid overflow-hidden rounded-3xl border border-kids-text/10 bg-kids-bg/50 transition duration-200 hover:-translate-y-1 hover:border-kids-secondary/40 hover:bg-white hover:shadow-lg sm:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]"
        >
          <div class="flex min-h-52 items-center justify-center bg-white p-5 sm:min-h-64 sm:p-6">
            <img
              :src="milestone.image"
              :alt="milestone.alt"
              class="h-48 w-full object-contain transition-transform duration-200 group-hover:scale-[1.03] sm:h-56"
              loading="lazy"
            />
          </div>
          <div class="flex flex-col p-5 sm:justify-center sm:p-7">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <span class="text-sm font-extrabold tracking-[0.12em] text-kids-secondary">
                {{ milestone.number }}
              </span>
              <span
                class="rounded-full px-3 py-1 text-xs font-bold"
                :class="milestone.statusClass"
              >
                {{ milestone.status }}
              </span>
            </div>
            <h3 class="mt-4 text-xl font-bold leading-snug text-kids-text">
              {{ milestone.title }}
            </h3>
            <p class="mt-3 text-sm leading-6 text-kids-text/70">
              {{ milestone.description }}
            </p>
          </div>
        </article>
      </div>

      <p class="mx-auto mt-7 max-w-3xl text-center text-xs leading-5 text-kids-text/60">
        Đây là các cột mốc và định hướng phát triển sản phẩm trong dự án; không đại diện cho giải thưởng,
        chứng nhận, kết quả nghiên cứu hay số liệu người dùng.
      </p>
    </div>
  </section>
</template>
