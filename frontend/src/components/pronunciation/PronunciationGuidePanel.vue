<script setup>
import AdminIcon from '../admin/AdminIcon.vue'

defineProps({
  word: { type: Object, required: true },
})

const parts = [
  { key: 'initial', label: 'Âm đầu', icon: 'microphone' },
  { key: 'final', label: 'Phần vần', icon: 'book' },
  { key: 'tone', label: 'Thanh điệu', icon: 'chart' },
]
</script>

<template>
  <section class="rounded-3xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6" aria-labelledby="pronunciation-guide-heading">
    <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Danh mục 2</p>
    <h2 id="pronunciation-guide-heading" class="mt-1 text-lg font-extrabold text-kids-text">Hướng dẫn bé phát âm</h2>
    <p class="mt-1 text-xs text-slate-500">Chưa có dữ liệu ngữ âm chuyên biệt đã xác minh cho từ này.</p>

    <div class="mt-4 grid gap-3 md:grid-cols-3">
      <article v-for="part in parts" :key="part.key" class="rounded-2xl bg-kids-bg p-4">
        <div class="flex items-center gap-2 text-sky-800"><AdminIcon :name="part.icon" :size="17" /><h3 class="text-sm font-extrabold">{{ part.label }}</h3></div>
        <p class="mt-2 text-xs leading-5 text-slate-500">{{ word.pronunciationGuide?.[part.key] || 'Hướng dẫn riêng cho phần này đang được cập nhật.' }}</p>
      </article>
    </div>

    <div class="mt-3 grid gap-3 sm:grid-cols-2">
      <div class="rounded-2xl border border-slate-100 p-4">
        <h3 class="flex items-center gap-2 text-sm font-extrabold text-kids-text"><AdminIcon name="image" :size="16" class="text-violet-600" />Khẩu hình, môi và lưỡi</h3>
        <p class="mt-2 text-xs leading-5 text-slate-500">{{ word.pronunciationGuide?.mouthShape || word.pronunciationGuide?.tongueAndLips || 'Chưa có hình hoặc chỉ dẫn khẩu hình đã xác minh. Con đọc nhẹ nhàng theo từng tiếng, không cần cố ép môi hay lưỡi.' }}</p>
      </div>
      <div class="rounded-2xl border border-slate-100 p-4">
        <h3 class="flex items-center gap-2 text-sm font-extrabold text-kids-text"><AdminIcon name="sparkles" :size="16" class="text-amber-500" />Lỗi thường gặp và cách sửa</h3>
        <template v-if="word.pronunciationGuide?.commonMistakes?.length">
          <ul class="mt-2 list-inside list-disc space-y-1 text-xs leading-5 text-slate-500"><li v-for="mistake in word.pronunciationGuide.commonMistakes" :key="mistake">{{ mistake }}</li></ul>
        </template>
        <p v-else class="mt-2 text-xs leading-5 text-slate-500">Chưa có lỗi thường gặp được xác minh cho từ này. Hãy nghe lại bản thân và nhờ người lớn hỗ trợ nếu cần.</p>
      </div>
    </div>
    <p class="mt-3 rounded-xl bg-sky-50 px-4 py-3 text-[11px] leading-5 text-sky-900">Các mục đang cập nhật không phải hướng dẫn chuyên môn. Không có dữ liệu âm vị thì giao diện sẽ không tự suy đoán cách phát âm.</p>
  </section>
</template>
