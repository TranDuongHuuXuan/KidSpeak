<script setup>
import parentImage from '../../assets/images/home/parent.svg'

const values = [
  {
    number: '01',
    title: 'Sứ mệnh',
    description:
      'Hướng đến môi trường luyện phát âm thân thiện, tạo thêm cơ hội thực hành và khuyến khích trẻ giao tiếp tự tin.',
    icon: 'heart',
  },
  {
    number: '02',
    title: 'Tầm nhìn',
    description:
      'Từng bước ứng dụng công nghệ để xây dựng trải nghiệm học tập trực quan, dễ tiếp cận và phù hợp với trẻ.',
    icon: 'spark',
  },
  {
    number: '03',
    title: 'Giá trị cốt lõi',
    description:
      'Kiên nhẫn lắng nghe, đồng hành cùng gia đình và khuyến khích sự tiến bộ theo nhịp độ riêng.',
    icon: 'people',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-[0.9fr_1.1fr] lg:gap-16 lg:px-12">
      <div class="rounded-[2rem] bg-kids-bg p-5 sm:p-8">
        <img
          :src="parentImage"
          alt="Minh họa phụ huynh đồng hành cùng trẻ trong học tập"
          class="mx-auto h-auto max-h-[26rem] w-full object-contain"
          loading="lazy"
        />
      </div>

      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Điều chúng tôi hướng đến</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Mỗi hành trình học tập đều bắt đầu bằng sự đồng hành.
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          KidSpeak được xây dựng với mong muốn hỗ trợ trẻ, phụ huynh và giáo viên cùng tạo nên
          trải nghiệm luyện tập tích cực, kiên nhẫn và không áp lực.
        </p>

        <div class="mt-7 grid gap-4">
          <article
            v-for="value in values"
            :key="value.number"
            class="flex gap-4 rounded-2xl border border-kids-text/10 bg-kids-bg/60 p-4 sm:p-5"
          >
            <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-kids-secondary/20 text-xs font-extrabold text-kids-text">
              {{ value.number }}
            </span>
            <div>
              <h3 class="font-bold text-kids-text">{{ value.title }}</h3>
              <p class="mt-1 text-sm leading-6 text-kids-text/70">{{ value.description }}</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>
