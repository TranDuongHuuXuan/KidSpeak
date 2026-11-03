<script setup>
import problemImage from '../../assets/images/home/problem.png'

const challenges = [
  {
    number: '01',
    title: 'Một số âm cần thêm thời gian',
    description: 'Có những âm trẻ cần được nghe mẫu và luyện đi luyện lại theo tốc độ phù hợp.',
  },
  {
    number: '02',
    title: 'Khó duy trì thói quen luyện tập',
    description: 'Lịch sinh hoạt bận rộn khiến việc dành thời gian thực hành đều đặn trở nên khó khăn.',
  },
  {
    number: '03',
    title: 'Tiến bộ không phải lúc nào cũng dễ thấy',
    description: 'Gia đình và giáo viên cần cách ghi nhận quá trình luyện tập theo từng giai đoạn.',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Mỗi bé một nhịp độ</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Mỗi trẻ đều có một hành trình phát triển ngôn ngữ riêng
        </h2>
        <p class="mt-4 text-base leading-7 text-kids-text/70">
          Những thử thách thường gặp có thể được hỗ trợ bằng việc thực hành nhẹ nhàng, thường xuyên và có người đồng hành.
        </p>
      </div>

      <div class="mt-12 grid items-center gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:gap-12">
        <div class="overflow-hidden rounded-[2rem] bg-kids-bg p-4 sm:p-6">
          <img
            :src="problemImage"
            alt="Minh họa một bạn nhỏ đang khám phá cách phát âm"
            class="mx-auto h-auto max-h-[25rem] w-full object-contain"
            loading="lazy"
          />
        </div>

        <div class="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
          <article
            v-for="challenge in challenges"
            :key="challenge.number"
            class="flex gap-4 rounded-2xl border border-kids-text/10 bg-kids-bg/70 p-5 transition duration-200 hover:-translate-y-0.5 hover:border-kids-secondary/50 hover:shadow-md"
          >
            <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-kids-primary/35 text-sm font-extrabold text-kids-text">
              {{ challenge.number }}
            </span>
            <div>
              <h3 class="font-bold text-kids-text">{{ challenge.title }}</h3>
              <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ challenge.description }}</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>
