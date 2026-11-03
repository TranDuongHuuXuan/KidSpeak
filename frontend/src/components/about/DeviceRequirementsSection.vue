<script setup>
import deviceImage from '../../assets/images/introduce/device-requirement.png'

const requirements = [
  {
    number: '01',
    title: 'Máy tính hoặc laptop',
    description: 'Dùng thiết bị có trình duyệt web tương thích để truy cập website.',
  },
  {
    number: '02',
    title: 'Microphone',
    description: 'Micro tích hợp hoặc micro rời đều có thể dùng nếu chức năng thu âm được hỗ trợ.',
  },
  {
    number: '03',
    title: 'Camera (không bắt buộc)',
    description: 'Chỉ cấp quyền camera nếu tính năng cụ thể yêu cầu; hiện chưa thấy chức năng dùng camera trong frontend.',
  },
  {
    number: '04',
    title: 'Kết nối Internet',
    description: 'Kết nối ổn định giúp truy cập website và các dịch vụ trực tuyến thuận tiện hơn.',
  },
]
</script>

<template>
  <section class="bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-[0.95fr_1.05fr] lg:gap-16 lg:px-12">
      <div class="overflow-hidden rounded-[2rem] border border-kids-text/5 bg-white p-3 shadow-sm sm:p-6">
        <img
          :src="deviceImage"
          alt="Minh họa người dùng học trực tuyến với máy tính và thiết bị âm thanh"
          class="mx-auto h-auto max-h-[27rem] w-full object-contain"
          loading="lazy"
        />
        <p class="mt-2 text-center text-xs text-kids-text/55">Hình minh họa thiết bị học tập.</p>
      </div>

      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Chuẩn bị trước khi học</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Chuẩn bị thiết bị phù hợp cho bé.
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Các gợi ý cơ bản để gia đình chuẩn bị môi trường học tập trực tuyến.
        </p>

        <ul class="mt-7 grid gap-3 sm:grid-cols-2">
          <li
            v-for="item in requirements"
            :key="item.number"
            class="rounded-2xl border border-kids-text/10 bg-white p-4"
          >
            <div class="flex items-center gap-3">
              <span class="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-kids-primary/35 text-xs font-extrabold">
                {{ item.number }}
              </span>
              <h3 class="text-sm font-bold text-kids-text">{{ item.title }}</h3>
            </div>
            <p class="mt-3 text-sm leading-6 text-kids-text/70">{{ item.description }}</p>
          </li>
        </ul>

        <p class="mt-4 rounded-xl bg-kids-secondary/10 px-4 py-3 text-sm leading-6 text-kids-text/75">
          Gợi ý: chọn không gian yên tĩnh để giọng nói dễ nghe hơn khi chức năng thu âm được tích hợp.
        </p>
      </div>
    </div>
  </section>
</template>
