<script setup>
const steps = [
  { number: '01', title: 'Đăng ký tài khoản', description: 'Tạo tài khoản KidSpeak để bắt đầu hành trình.' },
  { number: '02', title: 'Lựa chọn bài tập', description: 'Chọn nội dung luyện tập phù hợp với buổi học.' },
  { number: '03', title: 'Thực hành và ghi âm', description: 'Bé nghe mẫu, luyện nói và ghi lại phần thực hành.' },
  { number: '04', title: 'Xem kết quả luyện tập', description: 'Cùng người lớn xem thông tin hỗ trợ và tiếp tục luyện tập.' },
]
</script>

<template>
  <section class="bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-2xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Bắt đầu thật đơn giản</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">
          Bắt đầu luyện phát âm chỉ với 4 bước
        </h2>
      </div>

      <ol class="mt-12 grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        <li
          v-for="step in steps"
          :key="step.number"
          class="relative rounded-3xl border border-kids-text/10 bg-white p-6 shadow-sm"
        >
          <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-kids-primary text-sm font-extrabold text-kids-text">
            {{ step.number }}
          </span>
          <h3 class="mt-5 text-lg font-bold text-kids-text">{{ step.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ step.description }}</p>
        </li>
      </ol>
    </div>
  </section>
</template>
