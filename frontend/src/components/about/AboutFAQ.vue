<script setup>
import { ref } from 'vue'

const openIndex = ref(0)
const questions = [
  {
    question: 'KidSpeak dành cho đối tượng nào?',
    answer:
      'KidSpeak hướng đến trẻ em luyện phát âm và những người lớn đồng hành như phụ huynh, giáo viên. Trang web hiện tại đang trong quá trình phát triển.',
  },
  {
    question: 'Trẻ cần thiết bị gì để sử dụng?',
    answer:
      'Hiện có thể truy cập các trang giới thiệu, đăng ký và đăng nhập bằng trình duyệt web. Chức năng luyện tập có dùng micro chưa được tích hợp vào giao diện.',
  },
  {
    question: 'Có cần micro rời không?',
    answer:
      'Không nhất thiết; micro tích hợp trên thiết bị có thể dùng nếu chức năng thu âm được triển khai. Hiện website chưa có luồng thu âm.',
  },
  {
    question: 'Tại sao hệ thống không nhận giọng nói?',
    answer:
      'Trong mã nguồn hiện tại chưa có chức năng ghi âm ở frontend hoặc endpoint AI nhận âm thanh. Vì vậy, chưa thể nhận diện giọng nói thông qua giao diện website.',
  },
  {
    question: 'AI hỗ trợ phân tích phát âm như thế nào?',
    answer:
      'Đây là định hướng sản phẩm. AI service hiện có endpoint trạng thái dịch vụ; chưa thấy endpoint xử lý âm thanh hoặc mô hình phân tích được tích hợp.',
  },
  {
    question: 'Phụ huynh có thể theo dõi kết quả luyện tập không?',
    answer:
      'Cơ sở dữ liệu có cấu trúc phiên luyện tập và trường kết quả, nhưng hiện chưa có API/giao diện để phụ huynh xem dữ liệu này.',
  },
  {
    question: 'KidSpeak có thay thế chuyên gia âm ngữ trị liệu không?',
    answer:
      'Không. KidSpeak được định hướng là công cụ hỗ trợ luyện tập, không chẩn đoán và không thay thế tư vấn từ chuyên gia y tế hoặc âm ngữ trị liệu.',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-4xl px-5 sm:px-8">
      <div class="text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Giải đáp cùng KidSpeak</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">Câu hỏi thường gặp</h2>
      </div>

      <div class="mt-8 divide-y divide-kids-text/10 rounded-3xl border border-kids-text/10 bg-kids-bg/40 px-4 sm:px-6">
        <article v-for="(item, index) in questions" :key="item.question" class="py-1">
          <h3>
            <button
              :id="`about-faq-trigger-${index}`"
              type="button"
              class="flex min-h-16 w-full items-center justify-between gap-4 py-4 text-left text-sm font-bold text-kids-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary sm:text-base"
              :aria-expanded="openIndex === index"
              :aria-controls="`about-faq-panel-${index}`"
              @click="openIndex = openIndex === index ? -1 : index"
            >
              {{ item.question }}
              <span
                class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-kids-secondary/15 text-lg transition-transform duration-200"
                :class="{ 'rotate-45': openIndex === index }"
                aria-hidden="true"
              >
                +
              </span>
            </button>
          </h3>
          <div
            :id="`about-faq-panel-${index}`"
            role="region"
            :aria-labelledby="`about-faq-trigger-${index}`"
            class="grid transition-[grid-template-rows] duration-300 ease-out"
            :class="openIndex === index ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'"
            :aria-hidden="openIndex !== index"
          >
            <div class="overflow-hidden">
              <p class="pb-5 pr-10 text-sm leading-6 text-kids-text/70">{{ item.answer }}</p>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>
