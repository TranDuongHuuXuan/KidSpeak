<script setup>
const questions = [
  {
    question: 'KidSpeak là gì?',
    answer: 'KidSpeak là hệ thống hỗ trợ trẻ luyện phát âm qua các bài tập tương tác và công cụ hỗ trợ phân tích giọng nói.',
  },
  {
    question: 'AI phân tích phát âm như thế nào?',
    answer: 'AI hỗ trợ phân tích giọng nói được ghi âm trong quá trình thực hành và cung cấp thông tin tham khảo. Kết quả không phải là chẩn đoán hay đánh giá chuyên môn.',
  },
  {
    question: 'Trẻ có thể luyện tập trên thiết bị nào?',
    answer: 'KidSpeak được phát triển dưới dạng website và có thể sử dụng trên thiết bị có trình duyệt web hiện đại. Trải nghiệm cụ thể tùy thuộc vào thiết bị và kết nối mạng.',
  },
  {
    question: 'Giáo viên có thể theo dõi kết quả không?',
    answer: 'Hệ thống hướng tới hỗ trợ giáo viên tham khảo hoạt động và kết quả luyện tập. Vui lòng xác nhận các tính năng khả dụng theo cấu hình triển khai của trường.',
  },
  {
    question: 'Dữ liệu giọng nói được bảo vệ như thế nào?',
    answer: 'Vui lòng tham khảo chính sách bảo mật chính thức của đơn vị vận hành trước khi ghi âm hoặc gửi dữ liệu. Trang hiện chưa công bố chi tiết chính sách xử lý dữ liệu.',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-3xl px-5 sm:px-8">
      <div class="text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Giải đáp</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">Bạn có thắc mắc?</h2>
      </div>

      <div class="mt-10 flex flex-col gap-3">
        <details
          v-for="(item, index) in questions"
          :key="item.question"
          class="group rounded-2xl border border-kids-text/10 bg-kids-bg/50 px-5 py-4 open:bg-kids-bg"
          :open="index === 0"
        >
          <summary class="flex cursor-pointer list-none items-center justify-between gap-4 font-semibold text-kids-text marker:hidden focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary [&::-webkit-details-marker]:hidden">
            {{ item.question }}
            <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-white text-lg text-kids-text transition-transform group-open:rotate-45" aria-hidden="true">+</span>
          </summary>
          <p class="pt-3 pr-10 text-sm leading-6 text-kids-text/75">{{ item.answer }}</p>
        </details>
      </div>
    </div>
  </section>
</template>
