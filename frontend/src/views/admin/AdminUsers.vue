<script setup>
import { computed, reactive, ref, watch } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, formatDate, notify } from '../../data/adminMockData'

const search = ref('')
const roleFilter = ref('')
const statusFilter = ref('')
const page = ref(1)
const pageSize = 8
const modalOpen = ref(false)
const detailsOpen = ref(false)
const editing = ref(false)
const selectedUser = ref(null)
const form = reactive({ name: '', email: '', role: 'Student', status: 'Active' })

const filteredUsers = computed(() => adminData.users.filter((user) => {
  const query = search.value.trim().toLocaleLowerCase('vi')
  return (!query || `${user.name} ${user.email}`.toLocaleLowerCase('vi').includes(query))
    && (!roleFilter.value || user.role === roleFilter.value)
    && (!statusFilter.value || user.status === statusFilter.value)
}))
const pageCount = computed(() => Math.max(1, Math.ceil(filteredUsers.value.length / pageSize)))
const visibleUsers = computed(() => filteredUsers.value.slice((page.value - 1) * pageSize, page.value * pageSize))

watch([search, roleFilter, statusFilter], () => { page.value = 1 })
watch(pageCount, (count) => { if (page.value > count) page.value = count })

function openCreate() {
  editing.value = false
  selectedUser.value = null
  Object.assign(form, { name: '', email: '', role: 'Student', status: 'Active' })
  modalOpen.value = true
}

function openEdit(user) {
  editing.value = true
  selectedUser.value = user
  Object.assign(form, user)
  modalOpen.value = true
}

function saveUser() {
  if (editing.value && selectedUser.value) {
    Object.assign(selectedUser.value, form)
    notify('Đã cập nhật thông tin người dùng.')
  } else {
    adminData.users.unshift({ id: Math.max(0, ...adminData.users.map((user) => user.id)) + 1, ...form, joinedAt: new Date().toISOString().slice(0, 10) })
    notify('Đã thêm người dùng mới.')
  }
  modalOpen.value = false
}

function toggleLock(user) {
  user.status = user.status === 'Locked' ? 'Active' : 'Locked'
  notify(user.status === 'Locked' ? 'Đã khóa tài khoản.' : 'Đã mở khóa tài khoản.')
}

function initials(name) {
  return name.split(' ').slice(-2).map((part) => part[0]).join('').toLocaleUpperCase('vi')
}
</script>

<template>
  <AdminPageShell title="Quản lý người dùng" description="Tìm kiếm, cập nhật vai trò và quản lý trạng thái tài khoản trên hệ thống.">
    <template #actions>
      <button type="button" class="inline-flex items-center gap-2 rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700" @click="openCreate"><AdminIcon name="plus" :size="18" />Thêm người dùng</button>
    </template>

    <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="flex flex-col gap-3 border-b border-slate-100 p-4 lg:flex-row">
        <label class="relative min-w-0 flex-1">
          <AdminIcon name="search" :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input v-model="search" type="search" placeholder="Tìm theo tên hoặc email..." class="h-11 w-full rounded-xl border border-slate-200 pl-10 pr-3 text-sm outline-none transition focus:border-admin-cta focus:ring-2 focus:ring-blue-100" />
        </label>
        <label class="relative"><span class="sr-only">Lọc vai trò</span><select v-model="roleFilter" class="h-11 w-full min-w-40 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600 outline-none focus:border-admin-cta"><option value="">Tất cả vai trò</option><option>Admin</option><option>Teacher</option><option>Student</option></select></label>
        <label class="relative"><span class="sr-only">Lọc trạng thái</span><select v-model="statusFilter" class="h-11 w-full min-w-40 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600 outline-none focus:border-admin-cta"><option value="">Tất cả trạng thái</option><option value="Active">Hoạt động</option><option value="Pending">Chờ xử lý</option><option value="Locked">Đã khóa</option></select></label>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full min-w-[850px] text-left text-sm">
          <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500"><tr><th class="px-5 py-3.5">Người dùng</th><th class="px-4 py-3.5">Vai trò</th><th class="px-4 py-3.5">Ngày đăng ký</th><th class="px-4 py-3.5">Trạng thái</th><th class="px-5 py-3.5 text-right">Thao tác</th></tr></thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="user in visibleUsers" :key="user.id" class="hover:bg-slate-50/70">
              <td class="px-5 py-4"><div class="flex items-center gap-3"><span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-100 text-xs font-bold text-amber-800">{{ initials(user.name) }}</span><span class="min-w-0"><span class="block font-semibold text-slate-700">{{ user.name }}</span><span class="mt-0.5 block text-xs text-slate-400">{{ user.email }}</span></span></div></td>
              <td class="px-4 py-4"><span class="rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">{{ user.role }}</span></td>
              <td class="whitespace-nowrap px-4 py-4 text-slate-500">{{ formatDate(user.joinedAt) }}</td>
              <td class="px-4 py-4"><AdminBadge :status="user.status" /></td>
              <td class="px-5 py-4"><div class="flex justify-end gap-1">
                <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-blue-50 hover:text-blue-700" title="Xem chi tiết" @click="selectedUser = user; detailsOpen = true"><AdminIcon name="eye" :size="17" /></button>
                <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-800" title="Chỉnh sửa" @click="openEdit(user)"><AdminIcon name="edit" :size="17" /></button>
                <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-rose-50 hover:text-rose-700" :title="user.status === 'Locked' ? 'Mở khóa tài khoản' : 'Khóa tài khoản'" @click="toggleLock(user)"><AdminIcon :name="user.status === 'Locked' ? 'unlock' : 'lock'" :size="17" /></button>
              </div></td>
            </tr>
            <tr v-if="!visibleUsers.length"><td colspan="5" class="px-5 py-14 text-center"><div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-slate-400"><AdminIcon name="search" /></div><p class="mt-3 text-sm font-semibold text-slate-600">Không tìm thấy người dùng</p><p class="mt-1 text-xs text-slate-400">Thử thay đổi từ khóa hoặc bộ lọc.</p></td></tr>
          </tbody>
        </table>
      </div>
      <footer class="flex flex-col items-center justify-between gap-3 border-t border-slate-100 px-5 py-4 text-xs text-slate-500 sm:flex-row">
        <span>Hiển thị {{ filteredUsers.length ? (page - 1) * pageSize + 1 : 0 }}–{{ Math.min(page * pageSize, filteredUsers.length) }} trong {{ filteredUsers.length }} người dùng</span>
        <div class="flex items-center gap-2"><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 font-semibold hover:bg-slate-50 disabled:opacity-40" :disabled="page <= 1" @click="page--">Trước</button><span class="px-2 font-semibold text-slate-700">{{ page }} / {{ pageCount }}</span><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 font-semibold hover:bg-slate-50 disabled:opacity-40" :disabled="page >= pageCount" @click="page++">Tiếp</button></div>
      </footer>
    </div>

    <AdminModal v-model="modalOpen" :title="editing ? 'Chỉnh sửa người dùng' : 'Thêm người dùng mới'" @submit="saveUser">
      <div class="space-y-4">
        <label class="block text-sm font-semibold text-slate-700">Họ và tên<input v-model.trim="form.name" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" placeholder="Nhập họ tên" /></label>
        <label class="block text-sm font-semibold text-slate-700">Email<input v-model.trim="form.email" type="email" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" placeholder="name@example.com" /></label>
        <div class="grid gap-4 sm:grid-cols-2"><label class="block text-sm font-semibold text-slate-700">Vai trò<select v-model="form.role" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option>Student</option><option>Teacher</option><option>Admin</option><option>Guest</option></select></label><label class="block text-sm font-semibold text-slate-700">Trạng thái<select v-model="form.status" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option value="Active">Hoạt động</option><option value="Pending">Chờ xử lý</option><option value="Locked">Đã khóa</option></select></label></div>
      </div>
    </AdminModal>
    <AdminModal v-model="detailsOpen" title="Thông tin người dùng">
      <div v-if="selectedUser" class="space-y-4">
        <div class="flex items-center gap-4"><span class="flex h-14 w-14 items-center justify-center rounded-full bg-amber-100 text-lg font-bold text-amber-800">{{ initials(selectedUser.name) }}</span><div><h3 class="font-bold text-slate-800">{{ selectedUser.name }}</h3><p class="text-sm text-slate-500">{{ selectedUser.email }}</p></div></div>
        <dl class="grid grid-cols-2 gap-3 text-sm"><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Vai trò</dt><dd class="mt-1 font-semibold">{{ selectedUser.role }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Trạng thái</dt><dd class="mt-1"><AdminBadge :status="selectedUser.status" /></dd></div><div class="col-span-2 rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày đăng ký</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedUser.joinedAt) }}</dd></div></dl>
      </div>
      <template #actions><button type="button" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white" @click="detailsOpen = false">Đóng</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
