<script setup>
import { computed, ref } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, formatDate, notify } from '../../data/adminMockData'

const search = ref('')
const statusFilter = ref('Pending')
const selectedRequest = ref(null)
const dialog = ref('')
const rejectionReason = ref('')
const filteredRequests = computed(() => adminData.teacherRequests.filter((request) => {
  const query = search.value.trim().toLocaleLowerCase('vi')
  return (!query || `${request.name} ${request.email}`.toLocaleLowerCase('vi').includes(query))
    && (!statusFilter.value || request.status === statusFilter.value)
}))

function approve(request) {
  request.status = 'Approved'
  const existingUser = adminData.users.find((user) => user.email === request.email)
  if (existingUser) {
    existingUser.role = 'Teacher'
    existingUser.status = 'Active'
  } else {
    adminData.users.push({ id: Math.max(0, ...adminData.users.map((user) => user.id)) + 1, name: request.name, email: request.email, role: 'Teacher', joinedAt: request.sentAt, status: 'Active' })
  }
  dialog.value = ''
  notify(`Đã phê duyệt quyền giáo viên cho ${request.name}.`)
}

function rejectRequest() {
  if (!selectedRequest.value || !rejectionReason.value.trim()) return
  selectedRequest.value.status = 'Rejected'
  selectedRequest.value.rejectionReason = rejectionReason.value.trim()
  dialog.value = ''
  rejectionReason.value = ''
  notify('Đã từ chối yêu cầu và lưu lý do.')
}
</script>

<template>
  <AdminPageShell title="Xác thực giáo viên" description="Kiểm tra hồ sơ và phê duyệt quyền hoạt động cho giáo viên.">
    <div class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row">
      <label class="relative min-w-0 flex-1"><AdminIcon name="search" :size="18" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input v-model="search" type="search" class="h-11 w-full rounded-xl border border-slate-200 pl-10 pr-3 text-sm outline-none focus:border-admin-cta" placeholder="Tìm theo tên hoặc email..." /></label>
      <select v-model="statusFilter" class="h-11 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600"><option value="">Tất cả trạng thái</option><option value="Pending">Chờ xử lý</option><option value="Approved">Đã phê duyệt</option><option value="Rejected">Từ chối</option></select>
    </div>
    <div class="space-y-3">
      <article v-for="request in filteredRequests" :key="request.id" class="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:flex-row lg:items-center">
        <div class="flex min-w-0 flex-1 items-center gap-4"><span class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-violet-100 text-sm font-bold text-violet-700">{{ request.name.split(' ').slice(-2).map((part) => part[0]).join('') }}</span><div class="min-w-0 flex-1"><div class="flex flex-wrap items-center gap-2"><h3 class="font-bold text-slate-800">{{ request.name }}</h3><AdminBadge :status="request.status" /></div><p class="mt-1 text-sm text-slate-500">{{ request.email }}</p><p class="mt-1 text-xs text-slate-400">Gửi yêu cầu {{ formatDate(request.sentAt) }} · {{ request.document }}</p></div></div>
        <div class="flex flex-wrap gap-2"><button type="button" class="inline-flex items-center gap-2 rounded-xl border border-slate-200 px-3.5 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="selectedRequest = request; dialog = 'details'"><AdminIcon name="eye" :size="17" />Xem hồ sơ</button><template v-if="request.status === 'Pending'"><button type="button" class="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-3.5 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700" @click="approve(request)"><AdminIcon name="check" :size="17" />Phê duyệt</button><button type="button" class="inline-flex items-center gap-2 rounded-xl border border-rose-200 px-3.5 py-2.5 text-sm font-semibold text-rose-700 hover:bg-rose-50" @click="selectedRequest = request; rejectionReason = ''; dialog = 'reject'"><AdminIcon name="close" :size="17" />Từ chối</button></template></div>
      </article>
      <div v-if="!filteredRequests.length" class="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center"><p class="font-semibold text-slate-700">Không có yêu cầu phù hợp</p><p class="mt-1 text-sm text-slate-400">Thay đổi bộ lọc để xem thêm hồ sơ.</p></div>
    </div>

    <AdminModal :model-value="dialog === 'details'" title="Hồ sơ xác thực giáo viên" @update:model-value="dialog = ''">
      <div v-if="selectedRequest" class="space-y-4">
        <div class="flex items-center gap-3"><span class="flex h-12 w-12 items-center justify-center rounded-full bg-violet-100 font-bold text-violet-700">{{ selectedRequest.name.slice(0, 1) }}</span><div><h3 class="font-bold text-slate-800">{{ selectedRequest.name }}</h3><p class="text-sm text-slate-500">{{ selectedRequest.email }}</p></div></div>
        <div>
          <h4 class="mb-2 text-sm font-bold text-slate-700">Thông tin cá nhân</h4>
          <dl class="grid gap-2 text-sm sm:grid-cols-2">
            <div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Số điện thoại</dt><dd class="mt-1 font-semibold">{{ selectedRequest.phone }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày sinh</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedRequest.dateOfBirth) }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Trình độ chuyên môn</dt><dd class="mt-1 font-semibold">{{ selectedRequest.specialization }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Trường đào tạo</dt><dd class="mt-1 font-semibold">{{ selectedRequest.education }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Địa chỉ</dt><dd class="mt-1 font-semibold">{{ selectedRequest.address }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Kinh nghiệm giảng dạy</dt><dd class="mt-1">{{ selectedRequest.experience }}</dd></div>
            <div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Ngày gửi yêu cầu</dt><dd class="mt-1 font-semibold">{{ formatDate(selectedRequest.sentAt) }}</dd></div>
          </dl>
        </div>
        <div>
          <div class="mb-2 flex items-center justify-between gap-2">
            <h4 class="text-sm font-bold text-slate-700">Chứng chỉ &amp; bằng cấp</h4>
            <span class="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700">{{ selectedRequest.certificates?.length || 0 }} hồ sơ</span>
          </div>
          <div v-if="selectedRequest.certificates?.length" class="space-y-2">
            <article v-for="(certificate, index) in selectedRequest.certificates" :key="`${certificate.name}-${index}`" class="flex items-start gap-3 rounded-xl border border-slate-200 p-3">
              <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-700"><AdminIcon name="lessons" :size="19" /></span>
              <div class="min-w-0 flex-1">
                <h5 class="text-sm font-semibold text-slate-700">{{ certificate.name }}</h5>
                <p class="mt-1 text-xs leading-5 text-slate-500">{{ certificate.issuer }} · {{ certificate.year }}</p>
                <span class="mt-2 inline-flex rounded-full px-2 py-0.5 text-[11px] font-semibold" :class="certificate.status === 'Đã xác thực' ? 'bg-emerald-50 text-emerald-700' : certificate.status === 'Đã cung cấp' ? 'bg-blue-50 text-blue-700' : 'bg-amber-50 text-amber-700'">{{ certificate.status }}</span>
              </div>
            </article>
          </div>
          <p v-else class="rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-400">Chưa có chứng chỉ hoặc bằng cấp được cung cấp.</p>
        </div>
        <div class="rounded-xl bg-slate-50 p-3 text-sm"><p class="text-xs text-slate-400">Hồ sơ xác thực</p><p class="mt-1 font-semibold">{{ selectedRequest.document }}</p></div>
        <div v-if="selectedRequest.rejectionReason" class="rounded-xl bg-rose-50 p-3 text-rose-700"><p class="text-xs">Lý do từ chối</p><p class="mt-1">{{ selectedRequest.rejectionReason }}</p></div>
      </div>
      <template #actions><button type="button" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white" @click="dialog = ''">Đóng</button></template>
    </AdminModal>
    <AdminModal :model-value="dialog === 'reject'" title="Từ chối yêu cầu giáo viên" @update:model-value="dialog = ''" @submit="rejectRequest">
      <p class="mb-3 text-sm text-slate-600">Nhập lý do từ chối hồ sơ của <strong>{{ selectedRequest?.name }}</strong>.</p><textarea v-model.trim="rejectionReason" required rows="4" class="w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-admin-cta" placeholder="Ví dụ: Vui lòng bổ sung chứng chỉ chuyên môn." />
      <template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold" @click="dialog = ''">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700">Xác nhận từ chối</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
