<script setup>
import aboutImage from '../../assets/images/home/about-kidspeak.png'
</script>

<template>
  <section id="about" class="scroll-mt-24 bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-2 lg:gap-16 lg:px-12">
      <div class="relative">
        <div class="absolute -bottom-4 -left-4 h-2/3 w-2/3 rounded-[2rem] bg-kids-secondary/20"></div>
        <div class="relative overflow-hidden rounded-[2rem] bg-white p-3 shadow-lg sm:p-5">
          <img
            :src="aboutImage"
            alt="Minh họa giáo viên cùng trẻ thực hành ngôn ngữ trong lớp học"
            class="h-auto max-h-[32rem] w-full rounded-3xl object-contain"
            loading="lazy"
          />
        </div>
        <span class="absolute -right-2 top-5 rounded-2xl bg-kids-primary px-4 py-3 text-sm font-bold shadow-md sm:-right-4">
          Cùng bé luyện tập
        </span>
      </div>

      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Về KidSpeak</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          KidSpeak – Đồng hành cùng bé trên hành trình luyện phát âm
        </h2>
        <p class="mt-5 text-base leading-7 text-kids-text/75">
          KidSpeak là hệ thống hỗ trợ trẻ thực hành phát âm thông qua các hoạt động tương tác. Công nghệ AI có thể hỗ trợ phân tích giọng nói và cung cấp thông tin tham khảo cho quá trình luyện tập.
        </p>
        <p class="mt-4 text-base leading-7 text-kids-text/75">
          Nền tảng được xây dựng để gia đình và giáo viên cùng đồng hành, khuyến khích trẻ luyện tập tích cực mà không tạo áp lực. Kết quả phân tích chỉ phục vụ hỗ trợ học tập, không thay thế đánh giá chuyên môn.
        </p>

        <div class="mt-7 grid gap-3 sm:grid-cols-2">
          <div class="flex items-start gap-3 rounded-2xl bg-white p-4">
            <span class="mt-1 h-3 w-3 shrink-0 rounded-full bg-kids-cta"></span>
            <p class="text-sm font-semibold leading-6 text-kids-text">Bài tập gần gũi, khuyến khích trẻ chủ động thực hành</p>
          </div>
          <div class="flex items-start gap-3 rounded-2xl bg-white p-4">
            <span class="mt-1 h-3 w-3 shrink-0 rounded-full bg-kids-secondary"></span>
            <p class="text-sm font-semibold leading-6 text-kids-text">Thông tin tham khảo giúp nhìn lại tiến trình luyện tập</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
