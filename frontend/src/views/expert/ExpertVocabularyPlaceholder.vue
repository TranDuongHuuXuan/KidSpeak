<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { expertLessonService } from '../../services/expertLessonService'

const route = useRoute()
const category = ref(null)
const loading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  try {
    const response = await expertLessonService.getCategory(route.params.categoryId)
    category.value = response.data
  } catch (error) {
    errorMessage.value = error?.message || 'Không thể tải thông tin danh mục.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="p-4 sm:p-7 lg:p-8">
    <div class="mx-auto max-w-3xl rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
      <RouterLink :to="{ name: 'ExpertLessonCategories' }" class="text-sm font-semibold text-blue-600 hover:text-blue-700">← Quay lại danh mục</RouterLink>
      <p class="mt-6 text-sm font-semibold text-blue-600">Điều hướng từ danh mục</p>
      <h1 class="mt-1 text-2xl font-extrabold text-slate-800">Quản lý từ vựng</h1>
      <p v-if="loading" class="mt-3 text-sm text-slate-500">Đang tải danh mục…</p>
      <p v-else-if="errorMessage" role="alert" class="mt-3 text-sm text-rose-600">{{ errorMessage }}</p>
      <template v-else>
        <p class="mt-3 text-sm text-slate-500">Danh mục: <strong class="text-slate-700">{{ category?.name }}</strong> · ID {{ route.params.categoryId }}</p>
        <div class="mt-6 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-sm leading-6 text-slate-500">
          Khu vực này là điểm điều hướng cho module từ vựng. Chức năng CRUD từ vựng chưa được triển khai theo phạm vi yêu cầu.
        </div>
      </template>
      <RouterLink :to="{ name: 'ExpertLessons', query: { category_id: route.params.categoryId } }" class="mt-5 inline-flex rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">Xem bài học trong danh mục</RouterLink>
    </div>
  </section>
</template>
