<script setup>
import { computed, onMounted, ref } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { expertUpgradeService } from '../../services/expertUpgradeService'
import { toast } from '../../composable/useToast'

const requests = ref([])
const search = ref('')
const emailFilter = ref('')
const reasonFilter = ref('')
const experienceFilter = ref('')
const statusFilter = ref('')
const selectedRequest = ref(null)
const dialog = ref('')
const rejectionReason = ref('')
const errorMessage = ref('')
const loading = ref(false)
const page = ref(1)
const pagination = ref(null)
const approvalNote = ref('')
const documentPreview = ref(null)
const filteredRequests = computed(() => requests.value.filter((request) => {
  return !statusFilter.value || request.status === statusFilter.value
}))

async function loadRequests() {
  loading.value = true
  errorMessage.value = ''
  try {
    const result = await expertUpgradeService.list(statusFilter.value, {
      search: search.value,
      email: emailFilter.value,
      reason: reasonFilter.value,
      experience: experienceFilter.value,
    }, page.value)
    requests.value = result.items
    pagination.value = result.pagination
  } catch (error) {
    errorMessage.value = error.message || 'Không thể tải hồ sơ nâng cấp.'
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  page.value = 1
  loadRequests()
}

async function review(status, note = '') {
  if (!selectedRequest.value) return
  if (status === 'rejected' && !note.trim()) {
    errorMessage.value = 'Vui lòng nhập lý do từ chối.'
    return
  }
  if (status === 'approved' && !await toast.confirm('Ph\u00ea duy\u1ec7t y\u00eau c\u1ea7u gi\u00e1o vi\u00ean n\u00e0y?', { title: 'X\u00e1c nh\u1eadn ph\u00ea duy\u1ec7t', confirmText: 'Ph\u00ea duy\u1ec7t' })) return
  errorMessage.value = ''
  try {
    const updated = await expertUpgradeService.review(selectedRequest.value.id, status, note)
    const index = requests.value.findIndex((item) => item.id === updated.id)
    if (index >= 0) requests.value.splice(index, 1, updated)
    selectedRequest.value = updated
    dialog.value = ''
    if (status !== statusFilter.value && statusFilter.value) {
      requests.value = requests.value.filter((item) => item.id !== updated.id)
      dialog.value = ''
    }
    rejectionReason.value = ''
  } catch (error) {
    errorMessage.value = error.message || 'Không thể cập nhật kết quả xét duyệt.'
  }
}

async function openDocument(request, index, download = false) {
  errorMessage.value = ''
  try {
    const result = await expertUpgradeService.documentUrl(request.id, index, download)
    if (download || !['application/pdf', 'image/jpeg', 'image/png', 'image/webp'].includes(result.file_type)) {
      window.open(result.url, '_blank', 'noopener,noreferrer')
      return
    }
    documentPreview.value = result
    dialog.value = 'preview'
  } catch (error) {
    errorMessage.value = error.message || 'Không thể truy xuất tài liệu.'
  }
}

function formatDate(value) {
  return value ? new Date(value).toLocaleString('vi-VN') : '—'
}

onMounted(loadRequests)
</script>

<template>
  <AdminPageShell title="Xác thực chuyên gia" description="Xem hồ sơ nâng cấp Student lên Expert và xét duyệt tài liệu minh chứng.">
    <div class="grid gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:grid-cols-2 xl:grid-cols-6">
      <label class="space-y-1 text-xs font-semibold text-slate-600"><span>Applicant name</span><input v-model.trim="search" @keyup.enter="applyFilters" type="search" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal outline-none focus:border-admin-cta" placeholder="Search by name" /></label>
      <label class="space-y-1 text-xs font-semibold text-slate-600"><span>Email</span><input v-model.trim="emailFilter" @keyup.enter="applyFilters" type="search" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal outline-none focus:border-admin-cta" placeholder="Filter by email" /></label>
      <label class="space-y-1 text-xs font-semibold text-slate-600"><span>Registration reason</span><input v-model.trim="reasonFilter" @keyup.enter="applyFilters" type="search" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal outline-none focus:border-admin-cta" placeholder="Filter by reason" /></label>
      <label class="space-y-1 text-xs font-semibold text-slate-600"><span>Teaching experience</span><input v-model.trim="experienceFilter" @keyup.enter="applyFilters" type="search" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal outline-none focus:border-admin-cta" placeholder="Filter by experience" /></label>
      <label class="space-y-1 text-xs font-semibold text-slate-600"><span>Status</span><select v-model="statusFilter" class="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm font-normal text-slate-600" @change="applyFilters"><option value="">All statuses</option><option value="pending">Pending</option><option value="approved">Approved</option><option value="rejected">Rejected</option><option value="activated">Activated</option></select></label>
      <button type="button" class="self-end rounded-xl bg-admin-cta px-4 py-3 text-sm font-semibold text-white hover:bg-blue-700" @click="applyFilters">Apply filters</button>
    </div>
    <p v-if="errorMessage" class="rounded-xl bg-rose-50 p-3 text-sm text-rose-700" role="alert">{{ errorMessage }}</p>
    <p v-if="loading" class="p-8 text-center text-sm text-slate-500">Đang tải hồ sơ…</p>
    <div v-else class="space-y-3">
      <div class="overflow-x-auto rounded-2xl border border-slate-200 bg-white shadow-sm">
        <table class="min-w-full divide-y divide-slate-100 text-left text-sm">
          <thead class="bg-slate-50 text-xs uppercase tracking-wide text-slate-500"><tr><th class="px-4 py-3">ID</th><th class="px-4 py-3">Full name / Email</th><th class="px-4 py-3">Specialty</th><th class="px-4 py-3">Experience</th><th class="px-4 py-3">Status</th><th class="px-4 py-3">Submitted</th><th class="px-4 py-3">Action</th></tr></thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="request in filteredRequests" :key="request.id" class="align-top hover:bg-slate-50/70">
              <td class="px-4 py-4 font-semibold text-slate-700">{{ request.id }}</td>
              <td class="min-w-56 px-4 py-4"><div class="flex items-center gap-3"><img v-if="request.applicant_avatar_url" :src="request.applicant_avatar_url" :alt="request.applicant_name" class="h-10 w-10 rounded-full object-cover" /><span v-else class="flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 font-bold">{{ request.applicant_name?.slice(0, 1) }}</span><div><p class="font-semibold text-slate-800">{{ request.applicant_name }}</p><p class="text-xs text-slate-500">{{ request.applicant_email }}</p></div></div></td>
              <td class="max-w-48 px-4 py-4 text-slate-600">{{ request.specialty || '&#8212;' }}</td>
              <td class="max-w-64 px-4 py-4"><p class="line-clamp-2 text-xs text-slate-600">{{ request.experience || '&#8212;' }}</p></td>
              <td class="px-4 py-4"><AdminBadge :status="request.status" /></td>
              <td class="whitespace-nowrap px-4 py-4 text-xs text-slate-500">{{ formatDate(request.submitted_at) }}</td>
              <td class="px-4 py-4"><div class="flex flex-wrap gap-2"><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-700" @click="selectedRequest = request; dialog = 'details'">Details</button><template v-if="request.status === 'pending'"><button type="button" class="rounded-lg bg-emerald-600 px-3 py-2 text-xs font-semibold text-white" @click="selectedRequest = request; approvalNote = ''; dialog = 'approve'">Approve</button><button type="button" class="rounded-lg border border-rose-200 px-3 py-2 text-xs font-semibold text-rose-700" @click="selectedRequest = request; rejectionReason = ''; dialog = 'reject'">Reject</button></template></div></td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="pagination && pagination.total_pages > 1" class="flex items-center justify-between rounded-xl bg-white p-3 text-sm"><span>Page {{ pagination.current_page }} / {{ pagination.total_pages }} | {{ pagination.total }} requests</span><div class="flex gap-2"><button type="button" class="rounded-lg border px-3 py-2 disabled:opacity-40" :disabled="!pagination.has_prev" @click="page--; loadRequests()">Previous</button><button type="button" class="rounded-lg border px-3 py-2 disabled:opacity-40" :disabled="!pagination.has_next" @click="page++; loadRequests()">Next</button></div></div>
      <div v-if="!filteredRequests.length" class="rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center text-sm text-slate-500">No matching requests.</div>
    </div>
    <AdminModal :model-value="dialog === 'details'" title="Chi tiết hồ sơ Expert" @update:model-value="dialog = ''">
      <div v-if="selectedRequest" class="space-y-4 text-sm">
        <div class="flex items-center gap-3"><img v-if="selectedRequest.applicant_avatar_url" :src="selectedRequest.applicant_avatar_url" :alt="selectedRequest.applicant.full_name" class="h-14 w-14 rounded-full object-cover" /><span v-else class="flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 font-bold">{{ selectedRequest.applicant_name?.slice(0, 1) }}</span><div><h3 class="font-bold text-slate-800">{{ selectedRequest.applicant.full_name || selectedRequest.applicant_name }}</h3><p class="text-slate-500">{{ selectedRequest.applicant.email || selectedRequest.applicant_email }}</p></div></div>
        <section><h4 class="mb-2 font-bold text-slate-700">Thông tin tài khoản</h4><dl class="grid gap-2 sm:grid-cols-2"><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Mã người dùng</dt><dd>{{ selectedRequest.applicant.id }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Vai trò</dt><dd>{{ selectedRequest.applicant.role_name || '—' }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày sinh</dt><dd>{{ selectedRequest.applicant.date_of_birth ? formatDate(selectedRequest.applicant.date_of_birth) : '—' }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ảnh đại diện</dt><dd>{{ selectedRequest.applicant.avatar ? 'Đã thiết lập' : 'Chưa có' }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày tạo tài khoản</dt><dd>{{ formatDate(selectedRequest.applicant.created_at) }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Cập nhật hồ sơ</dt><dd>{{ formatDate(selectedRequest.applicant.updated_at) }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Tình trạng tài khoản</dt><dd>{{ selectedRequest.applicant.is_active ? 'Đang hoạt động' : 'Đã khóa' }}</dd></div></dl></section>
        <dl class="grid gap-2 sm:grid-cols-2"><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Chuyên môn đăng ký</dt><dd>{{ selectedRequest.specialty || '—' }}</dd></div><div class="rounded-xl bg-slate-50 p-3"><dt class="text-xs text-slate-400">Ngày gửi yêu cầu</dt><dd>{{ formatDate(selectedRequest.submitted_at) }}</dd></div><div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Kinh nghiệm</dt><dd class="whitespace-pre-wrap">{{ selectedRequest.experience || '—' }}</dd></div><div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Lý do</dt><dd class="whitespace-pre-wrap">{{ selectedRequest.reason }}</dd></div><div class="rounded-xl bg-slate-50 p-3 sm:col-span-2"><dt class="text-xs text-slate-400">Giới thiệu</dt><dd class="whitespace-pre-wrap">{{ selectedRequest.introduction || '—' }}</dd></div></dl>
        <section><h4 class="mb-2 font-bold text-slate-700">Uploaded documents</h4><ul v-if="selectedRequest.documents?.length" class="space-y-2"><li v-for="(document, index) in selectedRequest.documents" :key="document.file_key" class="flex flex-wrap items-center gap-2 rounded-xl border border-slate-200 p-3"><span class="min-w-0 flex-1 truncate font-medium">{{ document.file_name }}</span><span class="text-xs text-slate-500">{{ document.file_type }} | {{ (document.file_size / 1024 / 1024).toFixed(2) }} MB</span><span class="w-full text-[10px] text-slate-400">Uploaded {{ document.uploaded_at ? formatDate(document.uploaded_at) : 'time unavailable for older files' }}</span><button v-if="['application/pdf', 'image/jpeg', 'image/png', 'image/webp'].includes(document.file_type)" type="button" class="rounded-lg bg-admin-cta px-3 py-2 text-xs font-bold text-white" @click="openDocument(selectedRequest, index)">Preview</button><button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold text-slate-700" @click="openDocument(selectedRequest, index, true)">Download</button></li></ul><p v-else class="rounded-xl border border-dashed p-4 text-slate-400">No documents attached.</p></section>
        <div class="rounded-xl bg-slate-50 p-3 text-sm"><p><strong>Status:</strong> {{ selectedRequest.status }}</p><p><strong>Review note:</strong> {{ selectedRequest.review_note || '&#8212;' }}</p><p><strong>Reviewed by:</strong> {{ selectedRequest.reviewer_name || selectedRequest.reviewed_by || '&#8212;' }}</p><p><strong>Reviewed at:</strong> {{ formatDate(selectedRequest.reviewed_at) }}</p></div>
      </div>
      <template #actions><button type="button" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white" @click="dialog = ''">Đóng</button></template>
    </AdminModal>
    <AdminModal :model-value="dialog === 'approve'" title="Approve teacher request" @update:model-value="dialog = ''" @submit="review('approved', approvalNote)">
      <p class="mb-3 text-sm text-slate-600">Approval does not change the applicant role. The student must activate the role from their profile.</p>
      <textarea v-model.trim="approvalNote" rows="3" maxlength="2000" class="w-full rounded-xl border border-slate-200 p-3 text-sm" placeholder="Optional review note" />
      <template #actions><button type="button" class="rounded-xl border px-4 py-2.5 text-sm" @click="dialog = ''">Cancel</button><button type="submit" class="rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white">Confirm approval</button></template>
    </AdminModal>
    <AdminModal :model-value="dialog === 'preview'" :title="documentPreview?.file_name || 'Document preview'" size="max-w-5xl" @update:model-value="dialog = ''">
      <img v-if="documentPreview?.file_type?.startsWith('image/')" :src="documentPreview.url" :alt="documentPreview.file_name" class="mx-auto max-h-[70vh] max-w-full object-contain" />
      <iframe v-else-if="documentPreview?.file_type === 'application/pdf'" :src="documentPreview.url" :title="documentPreview.file_name" class="h-[70vh] w-full" />
      <template #actions><button type="button" class="rounded-xl border px-4 py-2.5 text-sm" @click="dialog = ''">Close preview</button></template>
    </AdminModal>
    <AdminModal :model-value="dialog === 'reject'" title="Từ chối hồ sơ Expert" @update:model-value="dialog = ''" @submit="review('rejected', rejectionReason)">
      <textarea v-model.trim="rejectionReason" required rows="4" class="w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-admin-cta" placeholder="Nhập lý do từ chối hồ sơ." />
      <template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm" @click="dialog = ''">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white">Xác nhận từ chối</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
