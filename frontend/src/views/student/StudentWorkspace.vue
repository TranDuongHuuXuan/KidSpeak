<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'

const route = useRoute()

const sections = {
  topics: { icon: 'book', message: 'Các chủ đề học tập sẽ xuất hiện tại đây để con khám phá và luyện từ mới.' },
  pronunciation: { icon: 'microphone', message: 'Khu vực luyện phát âm sẽ giúp con tập nói và nhận phản hồi cho từng từ.' },
  results: { icon: 'chart', message: 'Kết quả các bài học và điểm luyện phát âm của con sẽ được tổng hợp tại đây.' },
  achievements: { icon: 'trophy', message: 'Những huy hiệu con đạt được sẽ được lưu lại trong bộ sưu tập này.' },
  messages: { icon: 'message', message: 'Tin nhắn từ thầy cô sẽ được hiển thị tại đây.' },
  profile: { icon: 'profile', message: 'Thông tin hồ sơ học sinh sẽ được quản lý tại đây.' },
}

const section = computed(() => sections[route.meta.studentSection] || sections.topics)
</script>

<template>
  <section class="mx-auto flex min-h-full max-w-4xl items-center justify-center p-5 sm:p-8">
    <article class="w-full rounded-3xl border border-amber-100 bg-white p-7 text-center shadow-sm sm:p-10">
      <span class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-50 text-amber-700"><AdminIcon :name="section.icon" :size="28" /></span>
      <p class="mt-5 text-xs font-extrabold uppercase tracking-wider text-kids-cta">{{ route.meta.studentSection === 'pronunciation' ? 'Cùng luyện nói' : 'Sắp ra mắt' }}</p>
      <h2 class="mt-2 text-2xl font-extrabold text-kids-text">{{ route.meta.title }}</h2>
      <p class="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500">{{ route.meta.studentSection === 'pronunciation' ? 'Chọn một chủ đề rồi nhấn “Luyện phát âm” ở từ con muốn tập nhé.' : section.message }}</p>
      <p v-if="route.meta.studentSection !== 'pronunciation'" class="mt-4 text-xs text-slate-400">Mục này sẽ được hoàn thiện trong bước tiếp theo.</p>
      <RouterLink :to="{ name: route.meta.studentSection === 'pronunciation' ? 'StudentTopics' : 'StudentDashboard' }" class="mt-6 inline-flex items-center gap-2 rounded-xl bg-kids-primary px-5 py-3 text-sm font-extrabold text-kids-text transition hover:bg-amber-400">
        <AdminIcon :name="route.meta.studentSection === 'pronunciation' ? 'book' : 'dashboard'" :size="17" />{{ route.meta.studentSection === 'pronunciation' ? 'Chọn chủ đề' : 'Về tổng quan' }}
      </RouterLink>
    </article>
  </section>
</template>
