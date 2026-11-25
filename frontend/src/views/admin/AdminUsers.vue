<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { toast } from '../../composable/useToast'
import { adminUserService } from '../../services/adminUserService'

const search = ref('')
const debouncedSearch = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const createdFilter = ref('')
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const errorMessage = ref('')
const users = ref([])
const total = ref(0)
const totalPages = ref(0)
const editOpen = ref(false)
const detailsOpen = ref(false)
const saving = ref(false)
const selectedUser = ref(null)
const formError = ref('')
const form = reactive({ full_name: '', email: '', avatar: '', date_of_birth: '' })

const fromDate = computed(() => {
  if (!createdFilter.value) return ''
  const date = new Date()
  if (createdFilter.value === 'today') return date.toISOString().slice(0, 10)
  date.setDate(date.getDate() - (createdFilter.value === '7days' ? 6 : 29))
  return date.toISOString().slice(0, 10)
})
const toDate = computed(() => createdFilter.value ? new Date().toISOString().slice(0, 10) : '')
const firstRow = computed(() => total.value ? (page.value - 1) * pageSize + 1 : 0)
const lastRow = computed(() => Math.min(page.value * pageSize, total.value))

let debounceTimer
watch(search, (value) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { debouncedSearch.value = value.trim() }, 350)
})
watch([debouncedSearch, roleFilter, statusFilter, createdFilter], () => {
  page.value = 1
  void loadUsers()
})
watch(page, () => void loadUsers())

async function loadUsers() {
  loading.value = true
  errorMessage.value = ''
  try {
    const result = await adminUserService.list({
      search: debouncedSearch.value || undefined,
      role_id: roleFilter.value || undefined,
      is_active: statusFilter.value === '' ? undefined : statusFilter.value === 'active',
      created_from: fromDate.value || undefined,
      created_to: toDate.value || undefined,
      page: page.value,
      page_size: pageSize,
    })
    users.value = result?.items || []
    total.value = result?.total || 0
    totalPages.value = result?.total_pages || 0
    if (!totalPages.value && page.value > 1) page.value = 1
  } catch (error) {
    errorMessage.value = error?.message || 'Không thể tải danh sách người dùng.'
    users.value = []
    total.value = 0
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

function resetFilters() {
  search.value = ''
  debouncedSearch.value = ''
  roleFilter.value = ''
  statusFilter.value = ''
  createdFilter.value = ''
  page.value = 1
  void loadUsers()
}

function initials(name = '') {
  return name.trim().split(/\s+/).slice(-2).map((part) => part[0] || '').join('').toLocaleUpperCase('vi') || '?'
}

function formatDate(value) {
  if (!value) return '—'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? '—' : new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium' }).format(date)
}

function roleName(user) {
  return user.role_id === 3 ? 'Expert' : 'Student'
}

function openEdit(user) {
  selectedUser.value = user
  Object.assign(form, {
    full_name: user.full_name || '',
    email: user.email || '',
    avatar: user.avatar || '',
    date_of_birth: user.date_of_birth ? new Date(user.date_of_birth).toISOString().slice(0, 10) : '',
  })
  formError.value = ''
  editOpen.value = true
}

async function saveUser() {
  if (!selectedUser.value || saving.value) return
  if (!form.full_name.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) {
    formError.value = 'Vui lòng nhập họ tên và email hợp lệ.'
    return
  }
  saving.value = true
  formError.value = ''
  try {
    const updated = await adminUserService.update(selectedUser.value.id, {
      full_name: form.full_name.trim(),
      email: form.email.trim(),
      avatar: form.avatar.trim() || null,
      date_of_birth: form.date_of_birth || null,
    })
    selectedUser.value = updated
    editOpen.value = false
    toast.success('Đã cập nhật thông tin người dùng.')
    await loadUsers()
  } catch (error) {
    formError.value = error?.message || 'Không thể cập nhật người dùng.'
  } finally {
    saving.value = false
  }
}

async function openDetails(user) {
  detailsOpen.value = true
  selectedUser.value = user
  try {
    selectedUser.value = await adminUserService.get(user.id)
  } catch (error) {
    detailsOpen.value = false
    toast.error('Không thể tải chi tiết', error?.message || 'Vui lòng thử lại.')
  }
}

async function toggleActive(user) {
  const activate = !user.is_active
  const confirmed = await toast.confirm(
    activate ? `Kích hoạt lại tài khoản ${user.full_name}?` : `Khóa tài khoản ${user.full_name}?`,
    { title: activate ? 'Xác nhận kích hoạt' : 'Xác nhận khóa tài khoản', confirmText: activate ? 'Kích hoạt' : 'Khóa tài khoản', tone: activate ? 'primary' : 'danger' },
  )
  if (!confirmed) return
  try {
    const updated = await adminUserService.setActive(user.id, activate)
    const index = users.value.findIndex((item) => item.id === user.id)
    if (index >= 0) users.value[index] = updated
    if (selectedUser.value?.id === user.id) selectedUser.value = updated
    toast.success(activate ? 'Đã kích hoạt tài khoản.' : 'Đã khóa tài khoản.')
    await loadUsers()
  } catch (error) {
    toast.error('Thao tác thất bại', error?.message || 'Không thể cập nhật trạng thái tài khoản.')
  }
}

onMounted(loadUsers)
</script>

<template>
  <AdminPageShell title="Quản lý người dùng" description="Tìm kiếm, xem và quản lý tài khoản Student và Expert.">
    <div class="space-y-4">
      <section class="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-2 xl:grid-cols-[minmax(240px,1fr)_180px_180px_190px_auto]">
        <label class="relative min-w-0">
          <span class="sr-only">Tìm kiếm người dùng</span>
          <AdminIcon name="search" :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input v-model="search" type="search" placeholder="Tìm theo tên hoặc email..." class="h-11 w-full rounded-xl border border-slate-200 pl-10 pr-3 text-sm outline-none focus:border-admin-cta focus:ring-2 focus:ring-blue-100" />
        </label>
        <label><span class="sr-only">Lọc vai trò</span><select v-model="roleFilter" class="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600"><option value="">Tất cả vai trò</option><option value="2">Student</option><option value="3">Expert</option></select></label>
        <label><span class="sr-only">Lọc trạng thái</span><select v-model="statusFilter" class="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600"><option value="">Tất cả trạng thái</option><option value="active">Active</option><option value="inactive">Inactive</option></select></label>
        <label><span class="sr-only">Lọc ngày tạo</span><select v-model="createdFilter" class="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600"><option value="">Mọi thời điểm</option><option value="today">Hôm nay</option><option value="7days">7 ngày gần nhất</option><option value="30days">30 ngày gần nhất</option></select></label>
        <button type="button" class="h-11 rounded-xl border border-slate-200 px-4 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="resetFilters">Đặt lại lọc</button>
      </section>

      <section class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div class="flex items-center justify-between border-b border-slate-100 px-5 py-4">
          <h2 class="font-bold text-slate-800">Danh sách tài khoản</h2>
          <span class="text-sm text-slate-500">{{ total }} người dùng</span>
        </div>
        <div v-if="loading" class="flex min-h-56 items-center justify-center text-sm font-medium text-slate-500" role="status">Đang tải danh sách người dùng…</div>
        <div v-else-if="errorMessage" class="flex min-h-56 flex-col items-center justify-center gap-3 px-5 text-center">
          <p class="text-sm text-rose-600">{{ errorMessage }}</p>
          <button type="button" class="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold" @click="loadUsers">Thử lại</button>
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full min-w-[1050px] text-left text-sm">
            <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500"><tr><th class="px-4 py-3">STT</th><th class="px-4 py-3">Người dùng</th><th class="px-4 py-3">Vai trò</th><th class="px-4 py-3">Ngày tạo</th><th class="px-4 py-3">Cập nhật</th><th class="px-4 py-3">Trạng thái</th><th class="px-4 py-3 text-right">Thao tác</th></tr></thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="(user, index) in users" :key="user.id" class="hover:bg-slate-50/70">
                <td class="px-4 py-4 text-slate-500">{{ (page - 1) * pageSize + index + 1 }}</td>
                <td class="px-4 py-4"><div class="flex items-center gap-3"><img v-if="user.avatar?.startsWith('http')" :src="user.avatar" :alt="user.full_name" class="h-10 w-10 rounded-full object-cover" /><span v-else class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 text-xs font-bold text-amber-800">{{ initials(user.full_name) }}</span><span class="min-w-0"><span class="block font-semibold text-slate-700">{{ user.full_name }}</span><span class="block text-xs text-slate-400">{{ user.email }}</span></span></div></td>
                <td class="px-4 py-4"><span class="rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">{{ roleName(user) }}</span></td>
                <td class="whitespace-nowrap px-4 py-4 text-slate-500">{{ formatDate(user.created_at) }}</td>
                <td class="whitespace-nowrap px-4 py-4 text-slate-500">{{ formatDate(user.updated_at) }}</td>
                <td class="px-4 py-4"><AdminBadge :status="user.is_active ? 'Active' : 'Inactive'" /></td>
                <td class="px-4 py-4"><div class="flex justify-end gap-1"><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-blue-50 hover:text-blue-700" title="Xem chi tiết" @click="openDetails(user)"><AdminIcon name="eye" :size="17" /></button><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-800" title="Chỉnh sửa" @click="openEdit(user)"><AdminIcon name="edit" :size="17" /></button><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-rose-50 hover:text-rose-700" :title="user.is_active ? 'Khóa tài khoản' : 'Kích hoạt tài khoản'" @click="toggleActive(user)"><AdminIcon :name="user.is_active ? 'lock' : 'unlock'" :size="17" /></button></div></td>
              </tr>
              <tr v-if="!users.length"><td colspan="7" class="px-5 py-16 text-center"><p class="font-semibold text-slate-600">Không tìm thấy người dùng</p><p class="mt-1 text-xs text-slate-400">Thử thay đổi từ khóa hoặc bộ lọc.</p></td></tr>
            </tbody>
          </table>
        </div>
        <footer v-if="!loading && !errorMessage" class="flex flex-col items-center justify-between gap-3 border-t border-slate-100 px-5 py-4 text-xs text-slate-500 sm:flex-row"><span>Hiển thị {{ firstRow }}–{{ lastRow }} trong {{ total }} người dùng</span><div class="flex items-center gap-2"><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 font-semibold hover:bg-slate-50 disabled:opacity-40" :disabled="page <= 1" @click="page--">Trước</button><span class="px-2 font-semibold text-slate-700">{{ totalPages ? page : 0 }} / {{ totalPages }}</span><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 font-semibold hover:bg-slate-50 disabled:opacity-40" :disabled="page >= totalPages" @click="page++">Tiếp</button></div></footer>
      </section>
    </div>

    <AdminModal v-model="editOpen" title="Chỉnh sửa thông tin người dùng" size="max-w-2xl" @submit="saveUser">
      <div class="space-y-4">
        <label class="block text-sm font-semibold text-slate-700">Họ và tên<input v-model.trim="form.full_name" required minlength="2" maxlength="100" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
        <label class="block text-sm font-semibold text-slate-700">Email<input v-model.trim="form.email" type="email" required maxlength="255" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
        <label class="block text-sm font-semibold text-slate-700">Avatar URL hoặc key<input v-model.trim="form.avatar" maxlength="500" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
        <label class="block text-sm font-semibold text-slate-700">Ngày sinh<input v-model="form.date_of_birth" type="date" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
        <p v-if="formError" class="text-sm text-rose-600" role="alert">{{ formError }}</p>
      </div>
      <template #actions><button type="submit" :disabled="saving" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-60">{{ saving ? 'Đang lưu…' : 'Lưu thay đổi' }}</button></template>
    </AdminModal>

    <AdminModal v-model="detailsOpen" title="Chi tiết người dùng" size="max-w-2xl">
      <div v-if="selectedUser" class="space-y-4">
        <div class="flex items-center gap-4"><img v-if="selectedUser.avatar?.startsWith('http')" :src="selectedUser.avatar" :alt="selectedUser.full_name" class="h-14 w-14 rounded-full object-cover" /><span v-else class="flex h-14 w-14 items-center justify-center rounded-full bg-amber-100 text-lg font-bold text-amber-800">{{ initials(selectedUser.full_name) }}</span><div><h3 class="font-bold text-slate-800">{{ selectedUser.full_name }}</h3><p class="text-sm text-slate-500">{{ selectedUser.email }}</p></div></div>
        <dl class="grid gap-3 text-sm sm:grid-cols-2"><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">ID</dt><dd class="mt-1 font-semibold">{{ selectedUser.id }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Vai trò</dt><dd class="mt-1 font-semibold">{{ roleName(selectedUser) }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Trạng thái</dt><dd class="mt-1"><AdminBadge :status="selectedUser.is_active ? 'Active' : 'Inactive'" /></dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày sinh</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedUser.date_of_birth) }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày tạo</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedUser.created_at) }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Cập nhật gần nhất</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedUser.updated_at) }}</dd></div>
          <template v-if="selectedUser.role_id === 3"><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Chuyên môn</dt><dd class="mt-1 font-semibold">{{ selectedUser.specialty || 'Chưa có thông tin' }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Kinh nghiệm giảng dạy</dt><dd class="mt-1 whitespace-pre-wrap font-semibold">{{ selectedUser.teaching_experience || 'Chưa có thông tin' }}</dd></div><div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Giới thiệu giáo viên</dt><dd class="mt-1 whitespace-pre-wrap font-semibold">{{ selectedUser.teacher_introduction || 'Chưa có thông tin' }}</dd></div></template>
          <template v-else><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Khóa học đã đăng ký</dt><dd class="mt-1 font-semibold">{{ selectedUser.course_enrollment_count ?? 0 }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Phiên luyện tập</dt><dd class="mt-1 font-semibold">{{ selectedUser.practice_session_count ?? 0 }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Kết quả luyện tập đã lưu</dt><dd class="mt-1 font-semibold">{{ selectedUser.practice_history_count ?? 0 }}</dd></div></template>
        </dl>
      </div>
      <template #actions><button type="button" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white" @click="detailsOpen = false">Đóng</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
