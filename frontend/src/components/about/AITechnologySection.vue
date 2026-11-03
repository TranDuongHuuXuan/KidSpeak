<script setup>
import aiWorkflowImage from '../../assets/images/introduce/AI-technology.png'

const steps = [
  {
    number: '01',
    title: 'Thu âm giọng nói',
    description: 'Khi chức năng được tích hợp, trẻ sẽ nghe mẫu và đọc theo bài tập qua micro.',
  },
  {
    number: '02',
    title: 'Xử lý âm thanh',
    description: 'Âm thanh sẽ được tiếp nhận và chuẩn bị cho bước phân tích theo thiết kế hệ thống.',
  },
  {
    number: '03',
    title: 'Phân tích phát âm',
    description: 'Mô hình AI dự kiến hỗ trợ phân tích các tiêu chí được triển khai trong sản phẩm.',
  },
  {
    number: '04',
    title: 'Tham khảo phản hồi',
    description: 'Kết quả dự kiến hỗ trợ trẻ và người lớn lựa chọn nội dung luyện tập tiếp theo.',
  },
]
</script>

<template>
  <section id="ai-technology" class="scroll-mt-24 bg-kids-bg py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Công nghệ theo định hướng</p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          Công nghệ AI hoạt động như thế nào?
        </h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Đây là mô tả khái quát về quy trình mục tiêu, không phải chức năng đang hoạt động trên website hiện tại.
        </p>
      </div>

      <div class="mt-9 overflow-hidden rounded-[2rem] border border-kids-text/5 bg-white p-3 shadow-sm sm:p-6">
        <img
          :src="aiWorkflowImage"
          alt="Sơ đồ minh họa khái quát quá trình từ âm thanh qua xử lý và phân tích đến thông tin tham khảo"
          class="mx-auto h-auto max-h-[26rem] w-full object-contain"
          loading="lazy"
        />
        <p class="mt-2 text-center text-xs text-kids-text/55">Sơ đồ minh họa luồng xử lý dự kiến.</p>
      </div>

      <ol class="relative mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <li
          v-for="step in steps"
          :key="step.number"
          class="relative rounded-2xl border border-kids-text/10 bg-white p-5 shadow-sm"
        >
          <span class="inline-flex h-10 w-10 items-center justify-center rounded-xl bg-kids-primary/35 text-sm font-extrabold text-kids-text">
            {{ step.number }}
          </span>
          <h3 class="mt-4 font-bold text-kids-text">{{ step.title }}</h3>
          <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ step.description }}</p>
        </li>
      </ol>

      <div class="mt-7 rounded-2xl border border-feedback-warning/30 bg-feedback-warning/10 p-4 text-sm leading-6 text-kids-text sm:p-5">
        <strong class="font-bold">Tình trạng triển khai:</strong>
        mã nguồn AI hiện có các endpoint kiểm tra trạng thái dịch vụ; chưa thấy endpoint nhận/xử lý âm thanh
        hoặc mô hình phân tích được tích hợp. KidSpeak không đưa ra chẩn đoán và không thay thế chuyên gia.
      </div>
    </div>
  </section>
</template>
