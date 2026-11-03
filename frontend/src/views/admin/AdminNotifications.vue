<script setup>
import { computed, reactive, ref } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, formatDate, notify } from '../../data/adminMockData'

const search = ref('')
const statusFilter = ref('')
const audienceFilter = ref('')
const modalOpen = ref(false)
const deleteTarget = ref(null)
const editingNotice = ref(null)
const form = reactive({ title: '', content: '', audience: 'Tất cả người dùng', type: 'Hệ thống' })

const filteredNotifications = computed(() => adminData.notifications.filter((notice) => {
  const query = search.value.trim().toLocaleLowerCase('vi')
  return (!query || `${notice.title} ${notice.content}`.toLocaleLowerCase('vi').includes(query))
    && (!statusFilter.value || notice.status === statusFilter.value)
    && (!audienceFilter.value || notice.audience === audienceFilter.value)
}))

function openCreate() {
  editingNotice.value = null
  Object.assign(form, { title: '', content: '', audience: 'Tất cả người dùng', type: 'Hệ thống' })
  modalOpen.value = true
}

function openEdit(notice) {
  editingNotice.value = notice
  Object.assign(form, notice)
  modalOpen.value = true
}

function saveNotice() {
  if (editingNotice.value) {
    Object.assign(editingNotice.value, form)
    notify('Đã cập nhật thông báo.')
  } else {
    adminData.notifications.unshift({ id: Math.max(0, ...adminData.notifications.map((notice) => notice.id)) + 1, ...form, createdAt: new Date().toISOString().slice(0, 10), status: 'Draft' })
    notify('Đã tạo thông báo mới.')
  }
  modalOpen.value = false
}

function toggleSend(notice) {
  notice.status = notice.status === 'Sent' ? 'Draft' : 'Sent'
  notify(notice.status === 'Sent' ? 'Đã gửi thông báo.' : 'Đã chuyển thông báo về bản nháp.')
}

function deleteNotice() {
  if (!deleteTarget.value) return
  adminData.notifications.splice(adminData.notifications.indexOf(deleteTarget.value), 1)
  deleteTarget.value = null
  notify('Đã xóa thông báo.')
}
</script>

<template>
  <AdminPageShell title="Thông báo hệ thống" description="Soạn, chỉnh sửa và gửi thông báo đến đúng nhóm người dùng.">
    <template #actions><button type="button" class="inline-flex items-center gap-2 rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700" @click="openCreate"><AdminIcon name="plus" :size="18" />Tạo thông báo</button></template>
    <div class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm lg:flex-row">
      <label class="relative min-w-0 flex-1"><AdminIcon name="search" :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input v-model="search" type="search" placeholder="Tìm tiêu đề, nội dung..." class="h-11 w-full rounded-xl border border-slate-200 pl-10 pr-3 text-sm outline-none focus:border-admin-cta" /></label>
      <select v-model="audienceFilter" class="h-11 rounded-xl border border-slate-200 bg-white px-3 text-sm"><option value="">Tất cả đối tượng</option><option>Tất cả người dùng</option><option>Giáo viên</option><option>Học viên</option></select>
      <select v-model="statusFilter" class="h-11 rounded-xl border border-slate-200 bg-white px-3 text-sm"><option value="">Tất cả trạng thái</option><option value="Draft">Bản nháp</option><option value="Sent">Đã gửi</option></select>
    </div>
    <div class="space-y-3">
      <article v-for="notice in filteredNotifications" :key="notice.id" class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-start">
          <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-admin-cta"><AdminIcon name="bell" /></span>
          <div class="min-w-0 flex-1"><div class="flex flex-wrap items-center gap-2"><h3 class="font-bold text-slate-800">{{ notice.title }}</h3><AdminBadge :status="notice.status" /></div><p class="mt-2 text-sm leading-6 text-slate-500">{{ notice.content }}</p><div class="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs text-slate-400"><span>Người nhận: {{ notice.audience }}</span><span>Loại: {{ notice.type }}</span><span>{{ formatDate(notice.createdAt) }}</span></div></div>
          <div class="flex shrink-0 gap-1"><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100" title="Chỉnh sửa" @click="openEdit(notice)"><AdminIcon name="edit" :size="17" /></button><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-rose-50 hover:text-rose-600" title="Xóa" @click="deleteTarget = notice"><AdminIcon name="close" :size="17" /></button><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-50" @click="toggleSend(notice)">{{ notice.status === 'Sent' ? 'Thu hồi' : 'Gửi ngay' }}</button></div>
        </div>
      </article>
      <div v-if="!filteredNotifications.length" class="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center"><p class="font-semibold text-slate-700">Chưa có thông báo phù hợp</p><p class="mt-1 text-sm text-slate-400">Điều chỉnh bộ lọc hoặc tạo thông báo mới.</p></div>
    </div>

    <AdminModal v-model="modalOpen" :title="editingNotice ? 'Chỉnh sửa thông báo' : 'Tạo thông báo mới'" @submit="saveNotice">
      <div class="space-y-4"><label class="block text-sm font-semibold">Tiêu đề<input v-model.trim="form.title" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" placeholder="Tiêu đề thông báo" /></label><label class="block text-sm font-semibold">Nội dung<textarea v-model.trim="form.content" required rows="4" class="mt-1.5 w-full rounded-xl border border-slate-200 p-3 font-normal outline-none focus:border-admin-cta" placeholder="Nội dung gửi đến người dùng..." /></label><div class="grid gap-4 sm:grid-cols-2"><label class="block text-sm font-semibold">Đối tượng nhận<select v-model="form.audience" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option>Tất cả người dùng</option><option>Giáo viên</option><option>Học viên</option></select></label><label class="block text-sm font-semibold">Loại thông báo<select v-model="form.type" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 font-normal"><option>Hệ thống</option><option>Cập nhật</option><option>Sự kiện</option></select></label></div></div>
    </AdminModal>
    <AdminModal :model-value="Boolean(deleteTarget)" title="Xóa thông báo" @update:model-value="deleteTarget = null" @submit="deleteNotice"><p class="text-sm leading-6 text-slate-600">Bạn có chắc muốn xóa thông báo <strong>{{ deleteTarget?.title }}</strong>?</p><template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold" @click="deleteTarget = null">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white">Xóa thông báo</button></template></AdminModal>
  </AdminPageShell>
</template>
