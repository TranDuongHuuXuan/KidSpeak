<script setup>
import childImage from '../../assets/images/home/child.svg'

const steps = [
  'Đăng ký hoặc đăng nhập tài khoản.',
  'Chọn hồ sơ học viên.',
  'Lựa chọn bài luyện phát âm.',
  'Nghe mẫu và ghi âm giọng nói.',
  'Xem phản hồi và tiếp tục luyện tập.',
]
</script>

<template>
  <section class="bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Lộ trình sử dụng</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Bắt đầu hành trình luyện phát âm cùng KidSpeak.
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Các bước dưới đây mô tả quy trình mục tiêu của sản phẩm, không phải toàn bộ luồng đã có trên website hiện tại.
        </p>
      </div>

      <div class="mt-10 grid items-center gap-8 lg:grid-cols-[0.8fr_1.2fr] lg:gap-14">
        <div class="rounded-[2rem] bg-white p-5 shadow-sm sm:p-8">
          <img
            :src="childImage"
            alt="Minh họa trẻ khám phá hoạt động học tập"
            class="mx-auto h-auto max-h-80 w-full object-contain"
            loading="lazy"
          />
          <p class="mt-2 text-center text-xs text-kids-text/55">Minh họa hoạt động học tập, không phải ảnh chụp sản phẩm.</p>
        </div>

        <ol class="grid gap-3 sm:grid-cols-2">
          <li
            v-for="(step, index) in steps"
            :key="step"
            class="flex gap-4 rounded-2xl border border-kids-text/10 bg-white p-4 sm:p-5"
          >
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-kids-primary/40 text-sm font-extrabold text-kids-text">
              {{ String(index + 1).padStart(2, '0') }}
            </span>
            <p class="pt-1.5 text-sm font-semibold leading-6 text-kids-text/80">{{ step }}</p>
          </li>
        </ol>
      </div>

      <p class="mx-auto mt-6 max-w-3xl rounded-xl border border-feedback-warning/25 bg-feedback-warning/10 px-4 py-3 text-center text-sm leading-6 text-kids-text/75">
        Hiện website đã có đăng ký/đăng nhập; hồ sơ học viên, bài tập, thu âm và phản hồi luyện tập chưa có luồng giao diện được tích hợp.
      </p>
    </div>
  </section>
</template>
