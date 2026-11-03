<script setup>
import appExperienceImage from '../../assets/images/home/app-download.svg'
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-2 lg:gap-16 lg:px-12">
      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Một hành trình tích cực</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Khám phá trải nghiệm học tập cùng KidSpeak
        </h2>
        <p class="mt-5 text-base leading-7 text-kids-text/75">
          Mỗi buổi luyện tập là cơ hội để bé lắng nghe, thực hành và cùng người lớn nhìn lại những gì mình đã làm.
        </p>
        <p class="mt-4 text-sm leading-6 text-kids-text/65">
          Hình ảnh bên cạnh là minh họa hoạt động học tập; hiện chưa có ảnh chụp giao diện sản phẩm để giới thiệu tại đây.
        </p>
        <ul class="mt-6 flex flex-col gap-3">
          <li class="flex items-center gap-3 text-sm font-medium text-kids-text">
            <span class="flex h-7 w-7 items-center justify-center rounded-full bg-feedback-success/15 text-feedback-success" aria-hidden="true">✓</span>
            Tạo không khí luyện tập vui vẻ, không áp lực
          </li>
          <li class="flex items-center gap-3 text-sm font-medium text-kids-text">
            <span class="flex h-7 w-7 items-center justify-center rounded-full bg-feedback-success/15 text-feedback-success" aria-hidden="true">✓</span>
            Khuyến khích gia đình đồng hành cùng trẻ
          </li>
        </ul>
      </div>

      <div class="rounded-[2rem] bg-kids-bg p-5 sm:p-8">
        <div class="mx-auto flex min-h-72 max-w-xl items-center justify-center rounded-3xl bg-white p-4 sm:min-h-96 sm:p-7">
          <img
            :src="appExperienceImage"
            alt="Minh họa trải nghiệm KidSpeak trên thiết bị số"
            class="h-auto max-h-[28rem] w-full object-contain"
            loading="lazy"
          />
        </div>
      </div>
    </div>
  </section>
</template>
