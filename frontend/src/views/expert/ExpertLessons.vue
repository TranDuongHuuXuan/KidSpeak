<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { notifyExpert } from '../../services/expertService'
import { expertLessonService } from '../../services/expertLessonService'

const route = useRoute()
const lessons = ref([])
const categories = ref([])
const pagination = ref(null)
const skip = ref(0)
const limit = 20
const loading = ref(false)
const errorMessage = ref('')
const saving = ref(false)
const dialogOpen = ref(false)
const editingLesson = ref(null)
const imageFile = ref(null)
const imagePreview = ref('')
const filters = reactive({
  search: '',
  category_id: route.query.category_id ? Number(route.query.category_id) : '',
  level: '',
  is_published: '',
})
const form = reactive({
  category_id: '',
  title: '',
  description: '',
  level: 'BEGINNER',
  order: 0,
  is_published: true,
})
const levels = [
  { value: 'BEGINNER', label: 'Cơ bản' },
  { value: 'INTERMEDIATE', label: 'Trung bình' },
  { value: 'ADVANCED', label: 'Nâng cao' },
]

function messageFrom(error) {
  return error?.message || 'Không thể xử lý yêu cầu. Vui lòng thử lại.'
}

function clearPreview() {
  if (imagePreview.value.startsWith('blob:')) URL.revokeObjectURL(imagePreview.value)
  imagePreview.value = ''
}

function resetForm() {
  clearPreview()
  editingLesson.value = null
  imageFile.value = null
  form.category_id = categories.value[0]?.id || ''
  form.title = ''
  form.description = ''
  form.level = 'BEGINNER'
  form.order = 0
  form.is_published = true
}

async function loadCategories() {
  const allCategories = []
  let pageSkip = 0
  let hasNextPage = true
  while (hasNextPage) {
    const response = await expertLessonService.listCategories({ skip: pageSkip, limit: 100 })
    allCategories.push(...(response.data || []))
    hasNextPage = Boolean(response.pagination?.has_next)
    pageSkip += 100
  }
  categories.value = allCategories
  if (!form.category_id && categories.value.length) form.category_id = categories.value[0].id
}

async function loadLessons() {
  loading.value = true
  errorMessage.value = ''
  const params = { skip: skip.value, limit }
  if (filters.search.trim()) params.search = filters.search.trim()
  if (filters.category_id) params.category_id = filters.category_id
  if (filters.level) params.level = filters.level
  if (filters.is_published !== '') params.is_published = filters.is_published
  try {
    const response = await expertLessonService.listLessons(params)
    lessons.value = response.data || []
    pagination.value = response.pagination || null
  } catch (error) {
    errorMessage.value = messageFrom(error)
  } finally {
    loading.value = false
  }
}

async function loadPage() {
  try {
    await loadCategories()
    await loadLessons()
  } catch (error) {
    errorMessage.value = messageFrom(error)
  }
}

function applyFilters() {
  skip.value = 0
  loadLessons()
}

function openCreate() {
  resetForm()
  dialogOpen.value = true
}

function openEdit(lesson) {
  resetForm()
  editingLesson.value = lesson
  form.category_id = lesson.category_id || ''
  form.title = lesson.title
  form.description = lesson.description || ''
  form.level = lesson.level || 'BEGINNER'
  form.order = lesson.order
  form.is_published = lesson.is_published
  imagePreview.value = lesson.image || ''
  dialogOpen.value = true
}

function selectImage(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
    notifyExpert('Chỉ hỗ trợ ảnh JPG, PNG hoặc WEBP.', 'error')
    event.target.value = ''
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    notifyExpert('Ảnh không được vượt quá 5 MiB.', 'error')
    event.target.value = ''
    return
  }
  clearPreview()
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

function clearSelectedImage() {
  clearPreview()
  imageFile.value = null
  if (editingLesson.value?.image) imagePreview.value = editingLesson.value.image
}

async function saveLesson() {
  if (!form.title.trim()) {
    notifyExpert('Tên chủ đề không được để trống.', 'error')
    return
  }
  if (!form.category_id) {
    notifyExpert('Vui lòng chọn danh mục.', 'error')
    return
  }
  if (!Number.isInteger(Number(form.order)) || Number(form.order) < 0) {
    notifyExpert('Thứ tự phải là số nguyên không âm.', 'error')
    return
  }

  saving.value = true
  const payload = {
    category_id: Number(form.category_id),
    title: form.title.trim(),
    description: form.description,
    level: form.level,
    order: Number(form.order),
    is_published: form.is_published,
    image: imageFile.value,
  }
  try {
    if (editingLesson.value) {
      await expertLessonService.updateLesson(editingLesson.value.id, payload)
      notifyExpert('Đã cập nhật bài học.')
    } else {
      await expertLessonService.createLesson(payload)
      notifyExpert('Đã tạo bài học.')
    }
    dialogOpen.value = false
    resetForm()
    await loadLessons()
  } catch (error) {
    notifyExpert(messageFrom(error), 'error')
  } finally {
    saving.value = false
  }
}

async function deleteLesson(lesson) {
  if (!window.confirm(`Xóa bài học “${lesson.title}”? Bài học có dữ liệu liên quan sẽ không thể xóa.`)) return
  try {
    await expertLessonService.deleteLesson(lesson.id)
    notifyExpert('Đã xóa bài học.')
    if (lessons.value.length === 1 && skip.value > 0) skip.value = Math.max(0, skip.value - limit)
    await loadLessons()
  } catch (error) {
    notifyExpert(messageFrom(error), 'error')
  }
}

function levelLabel(value) {
  return levels.find((level) => level.value === value)?.label || 'Chưa xác định'
}

function formatDate(value) {
  return value ? new Intl.DateTimeFormat('vi-VN').format(new Date(value)) : '—'
}

onMounted(loadPage)
onBeforeUnmount(clearPreview)
</script>

<template>
  <section class="space-y-5 p-4 sm:p-7 lg:p-8">
    <header class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p class="text-sm font-semibold text-blue-600">Nội dung học tập</p>
        <h1 class="mt-1 text-2xl font-extrabold text-slate-800 sm:text-3xl">Quản lý bài học</h1>
        <p class="mt-2 text-sm text-slate-500">Quản lý chủ đề, mức độ và trạng thái xuất bản.</p>
      </div>
      <button type="button" class="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white hover:bg-blue-700" @click="openCreate">
        <AdminIcon name="plus" :size="18" /> Thêm bài học
      </button>
    </header>

    <form class="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-2 xl:grid-cols-5" @submit.prevent="applyFilters">
      <label class="xl:col-span-2"><span class="sr-only">Tìm kiếm theo tên</span><input v-model="filters.search" type="search" placeholder="Tìm tên chủ đề…" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-sm outline-none focus:border-blue-500" /></label>
      <select v-model="filters.category_id" aria-label="Lọc theo danh mục" class="h-10 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700"><option value="">Tất cả danh mục</option><option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option></select>
      <select v-model="filters.level" aria-label="Lọc theo mức độ" class="h-10 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700"><option value="">Tất cả mức độ</option><option v-for="level in levels" :key="level.value" :value="level.value">{{ level.label }}</option></select>
      <div class="flex gap-2"><select v-model="filters.is_published" aria-label="Lọc trạng thái xuất bản" class="h-10 min-w-0 flex-1 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700"><option value="">Mọi trạng thái</option><option value="true">Đã xuất bản</option><option value="false">Bản nháp</option></select><button type="submit" class="rounded-xl bg-slate-800 px-3 text-sm font-semibold text-white">Lọc</button></div>
    </form>

    <div v-if="errorMessage" role="alert" class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
      <span>{{ errorMessage }}</span><button type="button" class="font-semibold underline" @click="loadPage">Thử lại</button>
    </div>

    <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="flex items-center justify-between border-b border-slate-100 px-5 py-4"><div><h2 class="font-bold text-slate-800">Danh sách bài học</h2><p class="mt-1 text-xs text-slate-500">{{ pagination?.total || 0 }} bài học phù hợp</p></div></div>
      <div v-if="loading" class="space-y-3 p-5" aria-live="polite"><div v-for="index in 5" :key="index" class="h-14 animate-pulse rounded-xl bg-slate-100"></div></div>
      <div v-else-if="!lessons.length && !errorMessage" class="px-5 py-16 text-center"><AdminIcon name="book" :size="28" class="mx-auto text-slate-300" /><p class="mt-3 font-semibold text-slate-600">Chưa có bài học phù hợp</p><p class="mt-1 text-sm text-slate-400">Thử thay đổi bộ lọc hoặc tạo bài học mới.</p></div>
      <div v-else class="overflow-x-auto">
        <table class="w-full min-w-[970px] text-left text-sm">
          <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500"><tr><th class="px-5 py-3">Chủ đề</th><th class="px-4 py-3">Danh mục</th><th class="px-4 py-3">Mức độ</th><th class="px-4 py-3">Người tạo</th><th class="px-4 py-3">Thứ tự</th><th class="px-4 py-3">Trạng thái</th><th class="px-4 py-3">Ngày tạo</th><th class="px-5 py-3 text-right">Thao tác</th></tr></thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="lesson in lessons" :key="lesson.id" class="hover:bg-slate-50/70">
              <td class="px-5 py-3.5"><div class="flex items-center gap-3"><img v-if="lesson.image" :src="lesson.image" :alt="lesson.title" class="h-11 w-11 rounded-lg object-cover" /><span v-else class="flex h-11 w-11 items-center justify-center rounded-lg bg-blue-50 text-blue-500"><AdminIcon name="image" :size="18" /></span><div class="max-w-[240px]"><p class="truncate font-semibold text-slate-800">{{ lesson.title }}</p><p class="line-clamp-1 text-xs text-slate-400">{{ lesson.description || 'Chưa có mô tả.' }}</p></div></div></td>
              <td class="px-4 py-3.5 text-slate-600">{{ lesson.category_name || '—' }}</td>
              <td class="px-4 py-3.5"><span class="rounded-lg bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700">{{ levelLabel(lesson.level) }}</span></td>
              <td class="px-4 py-3.5 text-slate-600">{{ lesson.creator_name || '—' }}</td>
              <td class="px-4 py-3.5 text-slate-600">{{ lesson.order }}</td>
              <td class="px-4 py-3.5"><span class="rounded-lg px-2.5 py-1 text-xs font-semibold" :class="lesson.is_published ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'">{{ lesson.is_published ? 'Đã xuất bản' : 'Bản nháp' }}</span></td>
              <td class="whitespace-nowrap px-4 py-3.5 text-slate-500">{{ formatDate(lesson.created_at) }}</td>
              <td class="px-5 py-3.5"><div class="flex justify-end gap-1"><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-blue-50 hover:text-blue-700" :aria-label="`Sửa ${lesson.title}`" @click="openEdit(lesson)"><AdminIcon name="edit" :size="17" /></button><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-rose-50 hover:text-rose-700" :aria-label="`Xóa ${lesson.title}`" @click="deleteLesson(lesson)"><AdminIcon name="delete" :size="17" /></button></div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <footer v-if="pagination && pagination.total_pages > 1" class="flex items-center justify-between border-t border-slate-100 px-5 py-3 text-sm"><span class="text-slate-500">Trang {{ pagination.current_page }} / {{ pagination.total_pages }}</span><div class="flex gap-2"><button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 disabled:opacity-40" :disabled="!pagination.has_prev" @click="skip = Math.max(0, skip - limit); loadLessons()">Trước</button><button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 disabled:opacity-40" :disabled="!pagination.has_next" @click="skip += limit; loadLessons()">Sau</button></div></footer>
    </div>

    <div v-if="dialogOpen" class="fixed inset-0 z-[60] flex items-center justify-center overflow-y-auto bg-slate-950/50 p-4" @click.self="dialogOpen = false; resetForm()">
      <form class="my-auto max-h-[92vh] w-full max-w-2xl space-y-4 overflow-y-auto rounded-2xl bg-white p-5 shadow-2xl sm:p-6" @submit.prevent="saveLesson">
        <div><h2 class="text-xl font-extrabold text-slate-800">{{ editingLesson ? 'Chỉnh sửa bài học' : 'Thêm bài học' }}</h2><p class="mt-1 text-sm text-slate-500">Người tạo được lấy từ tài khoản đang đăng nhập.</p></div>
        <label class="block text-sm font-semibold text-slate-700">Danh mục <span class="text-rose-500">*</span><select v-model="form.category_id" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option disabled value="">Chọn danh mục</option><option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option></select></label>
        <label class="block text-sm font-semibold text-slate-700">Tên chủ đề <span class="text-rose-500">*</span><input v-model.trim="form.title" required maxlength="300" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-blue-500" /></label>
        <label class="block text-sm font-semibold text-slate-700">Mô tả<textarea v-model="form.description" rows="3" class="mt-1.5 w-full rounded-xl border border-slate-200 p-3 font-normal outline-none focus:border-blue-500"></textarea></label>
        <div class="grid gap-4 sm:grid-cols-2">
          <label class="block text-sm font-semibold text-slate-700">Mức độ <select v-model="form.level" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option v-for="level in levels" :key="level.value" :value="level.value">{{ level.label }}</option></select></label>
          <label class="block text-sm font-semibold text-slate-700">Thứ tự hiển thị<input v-model.number="form.order" type="number" min="0" step="1" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal" /></label>
        </div>
        <label class="flex items-center gap-3 rounded-xl border border-slate-200 p-3 text-sm font-semibold text-slate-700"><input v-model="form.is_published" type="checkbox" class="h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500" /> Xuất bản bài học</label>
        <div><label class="block text-sm font-semibold text-slate-700">Ảnh đại diện</label><input type="file" accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp" class="mt-2 block w-full text-sm text-slate-500 file:mr-3 file:rounded-lg file:border-0 file:bg-blue-50 file:px-3 file:py-2 file:font-semibold file:text-blue-700" @change="selectImage" /><div v-if="imagePreview" class="mt-3 flex items-center gap-3"><img :src="imagePreview" alt="Ảnh xem trước" class="h-16 w-16 rounded-xl object-cover" /><button type="button" class="text-xs font-semibold text-rose-600" @click="clearSelectedImage">Bỏ ảnh đã chọn</button></div><p v-else class="mt-1 text-xs text-slate-400">JPG, PNG, WEBP · tối đa 5 MiB</p></div>
        <div class="flex justify-end gap-2 border-t border-slate-100 pt-4"><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600" @click="dialogOpen = false; resetForm()">Hủy</button><button type="submit" class="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50" :disabled="saving || !categories.length">{{ saving ? 'Đang lưu…' : 'Lưu bài học' }}</button></div>
      </form>
    </div>
  </section>
</template>
