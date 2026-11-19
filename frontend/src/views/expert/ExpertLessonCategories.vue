<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { notifyExpert } from '../../services/expertService'
import { expertLessonService } from '../../services/expertLessonService'

const router = useRouter()
const categories = ref([])
const pagination = ref(null)
const skip = ref(0)
const limit = 20
const loading = ref(false)
const errorMessage = ref('')
const saving = ref(false)
const dialogOpen = ref(false)
const editingCategory = ref(null)
const imageFile = ref(null)
const imagePreview = ref('')
const form = reactive({ name: '', description: '', order: 0 })
const pageCount = computed(() => pagination.value?.total_pages || 1)

function messageFrom(error) {
  return error?.message || 'Không thể xử lý yêu cầu. Vui lòng thử lại.'
}

function clearPreview() {
  if (imagePreview.value.startsWith('blob:')) URL.revokeObjectURL(imagePreview.value)
  imagePreview.value = ''
}

function resetForm() {
  clearPreview()
  form.name = ''
  form.description = ''
  form.order = 0
  imageFile.value = null
  editingCategory.value = null
}

async function loadCategories() {
  loading.value = true
  errorMessage.value = ''
  try {
    const response = await expertLessonService.listCategories({ skip: skip.value, limit })
    categories.value = response.data || []
    pagination.value = response.pagination || null
  } catch (error) {
    errorMessage.value = messageFrom(error)
  } finally {
    loading.value = false
  }
}

function openCreate() {
  resetForm()
  dialogOpen.value = true
}

function openEdit(category) {
  resetForm()
  editingCategory.value = category
  form.name = category.name
  form.description = category.description || ''
  form.order = category.order
  imagePreview.value = category.image || ''
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
  if (editingCategory.value?.image) imagePreview.value = editingCategory.value.image
}

async function saveCategory() {
  if (!form.name.trim()) {
    notifyExpert('Tên danh mục không được để trống.', 'error')
    return
  }
  if (!Number.isInteger(Number(form.order)) || Number(form.order) < 0) {
    notifyExpert('Thứ tự phải là số nguyên không âm.', 'error')
    return
  }

  saving.value = true
  const payload = {
    name: form.name.trim(),
    description: form.description,
    order: Number(form.order),
    image: imageFile.value,
  }
  try {
    if (editingCategory.value) {
      await expertLessonService.updateCategory(editingCategory.value.id, payload)
      notifyExpert('Đã cập nhật danh mục.')
    } else {
      await expertLessonService.createCategory(payload)
      notifyExpert('Đã tạo danh mục.')
    }
    dialogOpen.value = false
    resetForm()
    await loadCategories()
  } catch (error) {
    notifyExpert(messageFrom(error), 'error')
  } finally {
    saving.value = false
  }
}

async function deleteCategory(category) {
  if (!window.confirm(`Xóa danh mục “${category.name}”? Danh mục có bài học sẽ không thể xóa.`)) return
  try {
    await expertLessonService.deleteCategory(category.id)
    notifyExpert('Đã xóa danh mục.')
    if (categories.value.length === 1 && skip.value > 0) skip.value = Math.max(0, skip.value - limit)
    await loadCategories()
  } catch (error) {
    notifyExpert(messageFrom(error), 'error')
  }
}

function openVocabulary(category) {
  router.push({
    name: 'ExpertCategoryVocabularies',
    params: { categoryId: category.id },
  })
}

function formatDate(value) {
  return value ? new Intl.DateTimeFormat('vi-VN').format(new Date(value)) : '—'
}

onMounted(loadCategories)
onBeforeUnmount(clearPreview)
</script>

<template>
  <section class="space-y-5 p-4 sm:p-7 lg:p-8">
    <header class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p class="text-sm font-semibold text-blue-600">Nội dung học tập</p>
        <h1 class="mt-1 text-2xl font-extrabold text-slate-800 sm:text-3xl">Quản lý chủ đề</h1>
        <p class="mt-2 text-sm text-slate-500">Tạo và sắp xếp danh mục bài học cho học viên.</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <RouterLink :to="{ name: 'ExpertLessons' }" class="inline-flex h-11 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700 hover:bg-slate-50">
          <AdminIcon name="book" :size="17" /> Quản lý bài học
        </RouterLink>
        <button type="button" class="inline-flex h-11 items-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white hover:bg-blue-700" @click="openCreate">
          <AdminIcon name="plus" :size="18" /> Thêm danh mục
        </button>
      </div>
    </header>

    <div v-if="errorMessage" role="alert" class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700">
      <span>{{ errorMessage }}</span>
      <button type="button" class="font-semibold underline" @click="loadCategories">Thử lại</button>
    </div>

    <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 px-5 py-4">
        <div><h2 class="font-bold text-slate-800">Danh mục bài học</h2><p class="mt-1 text-xs text-slate-500">{{ pagination?.total || 0 }} danh mục</p></div>
        <span class="text-xs text-slate-400">Sắp xếp theo thứ tự hiển thị</span>
      </div>
      <div v-if="loading" class="space-y-3 p-5" aria-live="polite">
        <div v-for="index in 4" :key="index" class="h-16 animate-pulse rounded-xl bg-slate-100"></div>
      </div>
      <div v-else-if="!categories.length && !errorMessage" class="px-5 py-16 text-center">
        <AdminIcon name="lessons" :size="28" class="mx-auto text-slate-300" />
        <p class="mt-3 font-semibold text-slate-600">Chưa có danh mục nào</p>
        <p class="mt-1 text-sm text-slate-400">Tạo danh mục đầu tiên để bắt đầu thêm bài học.</p>
      </div>
      <div v-else class="divide-y divide-slate-100">
        <article v-for="category in categories" :key="category.id" class="flex flex-col gap-4 p-4 sm:flex-row sm:items-center sm:px-5">
          <img v-if="category.image" :src="category.image" :alt="category.name" class="h-16 w-16 shrink-0 rounded-xl bg-slate-100 object-cover" />
          <div v-else class="flex h-16 w-16 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-500"><AdminIcon name="image" :size="24" /></div>
          <div class="min-w-0 flex-1">
            <div class="flex flex-wrap items-center gap-2"><h3 class="font-bold text-slate-800">{{ category.name }}</h3><span class="rounded-md bg-slate-100 px-2 py-1 text-xs text-slate-500">Thứ tự {{ category.order }}</span></div>
            <p class="mt-1 line-clamp-2 text-sm text-slate-500">{{ category.description || 'Chưa có mô tả.' }}</p>
            <p class="mt-1 text-xs text-slate-400">Tạo {{ formatDate(category.created_at) }} · Cập nhật {{ formatDate(category.updated_at) }}</p>
          </div>
          <div class="flex flex-wrap gap-2 sm:justify-end">
            <button type="button" class="inline-flex h-9 items-center gap-1.5 rounded-lg border border-blue-100 px-3 text-xs font-semibold text-blue-700 hover:bg-blue-50" @click="openVocabulary(category)">
              <AdminIcon name="book" :size="15" /> Danh sách từ vựng
            </button>
            <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-blue-700" :aria-label="`Sửa ${category.name}`" @click="openEdit(category)"><AdminIcon name="edit" :size="17" /></button>
            <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-rose-50 hover:text-rose-700" :aria-label="`Xóa ${category.name}`" @click="deleteCategory(category)"><AdminIcon name="delete" :size="17" /></button>
          </div>
        </article>
      </div>
      <footer v-if="pageCount > 1" class="flex items-center justify-between border-t border-slate-100 px-5 py-3 text-sm">
        <span class="text-slate-500">Trang {{ pagination?.current_page }} / {{ pageCount }}</span>
        <div class="flex gap-2">
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 disabled:opacity-40" :disabled="!pagination?.has_prev" @click="skip = Math.max(0, skip - limit); loadCategories()">Trước</button>
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 disabled:opacity-40" :disabled="!pagination?.has_next" @click="skip += limit; loadCategories()">Sau</button>
        </div>
      </footer>
    </div>

    <div v-if="dialogOpen" class="fixed inset-0 z-[60] flex items-center justify-center overflow-y-auto bg-slate-950/50 p-4" @click.self="dialogOpen = false; resetForm()">
      <form class="my-auto w-full max-w-xl space-y-4 rounded-2xl bg-white p-5 shadow-2xl sm:p-6" @submit.prevent="saveCategory">
        <div><h2 class="text-xl font-extrabold text-slate-800">{{ editingCategory ? 'Chỉnh sửa danh mục' : 'Thêm danh mục' }}</h2><p class="mt-1 text-sm text-slate-500">Thông tin được lưu vào hệ thống sau khi xác nhận.</p></div>
        <label class="block text-sm font-semibold text-slate-700">Tên danh mục <span class="text-rose-500">*</span><input v-model.trim="form.name" required maxlength="200" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-blue-500" /></label>
        <label class="block text-sm font-semibold text-slate-700">Mô tả<textarea v-model="form.description" rows="3" class="mt-1.5 w-full rounded-xl border border-slate-200 p-3 font-normal outline-none focus:border-blue-500"></textarea></label>
        <label class="block text-sm font-semibold text-slate-700">Thứ tự hiển thị<input v-model.number="form.order" type="number" min="0" step="1" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-blue-500" /></label>
        <div>
          <label class="block text-sm font-semibold text-slate-700">Ảnh đại diện</label>
          <input type="file" accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp" class="mt-2 block w-full text-sm text-slate-500 file:mr-3 file:rounded-lg file:border-0 file:bg-blue-50 file:px-3 file:py-2 file:font-semibold file:text-blue-700" @change="selectImage" />
          <div v-if="imagePreview" class="mt-3 flex items-center gap-3"><img :src="imagePreview" alt="Ảnh xem trước" class="h-16 w-16 rounded-xl object-cover" /><button type="button" class="text-xs font-semibold text-rose-600" @click="clearSelectedImage">Bỏ ảnh đã chọn</button></div>
          <p v-else class="mt-1 text-xs text-slate-400">JPG, PNG, WEBP · tối đa 5 MiB</p>
        </div>
        <div class="flex justify-end gap-2 border-t border-slate-100 pt-4">
          <button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600" @click="dialogOpen = false; resetForm()">Hủy</button>
          <button type="submit" class="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50" :disabled="saving">{{ saving ? 'Đang lưu…' : 'Lưu danh mục' }}</button>
        </div>
      </form>
    </div>
  </section>
</template>
