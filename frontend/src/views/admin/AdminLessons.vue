<script setup>
import { computed, ref } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, formatDate, notify } from '../../data/adminMockData'

const statusFilter = ref('Pending')
const selectedLesson = ref(null)
const dialog = ref('')
const rejectionReason = ref('')
const filteredLessons = computed(() => adminData.lessons.filter((lesson) => !statusFilter.value || lesson.status === statusFilter.value))

function approveLesson(lesson) {
  lesson.status = 'Approved'
  lesson.note = ''
  dialog.value = ''
  notify(`Đã phê duyệt bài học “${lesson.title}”.`)
}

function rejectLesson() {
  if (!selectedLesson.value || !rejectionReason.value.trim()) return
  selectedLesson.value.status = 'Rejected'
  selectedLesson.value.note = rejectionReason.value.trim()
  dialog.value = ''
  rejectionReason.value = ''
  notify('Đã từ chối bài học và lưu ghi chú.')
}
</script>

<template>
  <AdminPageShell title="Kiểm duyệt bài học" description="Xem trước nội dung giáo viên gửi, sau đó phê duyệt hoặc phản hồi để chỉnh sửa.">
    <div class="flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
      <div><p class="font-semibold text-slate-700">Danh sách nội dung</p><p class="mt-1 text-xs text-slate-400">{{ filteredLessons.length }} bài học phù hợp bộ lọc</p></div>
      <label class="flex items-center gap-2 text-sm text-slate-500"><span>Trạng thái</span><select v-model="statusFilter" class="h-10 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700"><option value="">Tất cả</option><option value="Draft">Bản nháp</option><option value="Pending">Chờ duyệt</option><option value="Approved">Đã phê duyệt</option><option value="Rejected">Từ chối</option></select></label>
    </div>
    <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="overflow-x-auto"><table class="w-full min-w-[820px] text-left text-sm">
        <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500"><tr><th class="px-5 py-3.5">Bài học</th><th class="px-4 py-3.5">Giáo viên</th><th class="px-4 py-3.5">Chủ đề</th><th class="px-4 py-3.5">Ngày gửi</th><th class="px-4 py-3.5">Trạng thái</th><th class="px-5 py-3.5 text-right">Thao tác</th></tr></thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="lesson in filteredLessons" :key="lesson.id" class="hover:bg-slate-50/70">
            <td class="px-5 py-4"><div class="flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-xl">{{ lesson.image }}</span><span class="font-semibold text-slate-700">{{ lesson.title }}</span></div></td>
            <td class="whitespace-nowrap px-4 py-4 text-slate-600">{{ lesson.teacher }}</td><td class="px-4 py-4"><span class="rounded-lg bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700">{{ lesson.topic }}</span></td>
            <td class="whitespace-nowrap px-4 py-4 text-slate-500">{{ formatDate(lesson.submittedAt) }}</td><td class="px-4 py-4"><AdminBadge :status="lesson.status" /></td>
            <td class="px-5 py-4"><div class="flex justify-end gap-1"><button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-blue-50 hover:text-blue-700" title="Xem trước nội dung" @click="selectedLesson = lesson; dialog = 'preview'"><AdminIcon name="eye" :size="17" /></button><template v-if="lesson.status === 'Pending'"><button type="button" class="rounded-lg p-2 text-emerald-600 hover:bg-emerald-50" title="Phê duyệt" @click="approveLesson(lesson)"><AdminIcon name="check" :size="18" /></button><button type="button" class="rounded-lg p-2 text-rose-600 hover:bg-rose-50" title="Từ chối" @click="selectedLesson = lesson; rejectionReason = ''; dialog = 'reject'"><AdminIcon name="close" :size="18" /></button></template></div></td>
          </tr>
          <tr v-if="!filteredLessons.length"><td colspan="6" class="px-5 py-14 text-center text-sm text-slate-400">Không có bài học phù hợp với trạng thái này.</td></tr>
        </tbody>
      </table></div>
    </div>

    <AdminModal :model-value="dialog === 'preview'" title="Xem trước bài học" size="max-w-2xl" @update:model-value="dialog = ''">
      <div v-if="selectedLesson" class="space-y-5">
        <div class="flex flex-wrap items-start justify-between gap-3"><div><p class="text-xs font-semibold uppercase tracking-wide text-admin-cta">{{ selectedLesson.topic }}</p><h3 class="mt-1 text-xl font-extrabold text-slate-800">{{ selectedLesson.title }}</h3><p class="mt-1 text-sm text-slate-500">Giáo viên {{ selectedLesson.teacher }} · {{ formatDate(selectedLesson.submittedAt) }}</p></div><AdminBadge :status="selectedLesson.status" /></div>
        <div class="flex min-h-36 items-center justify-center rounded-2xl bg-amber-50 text-6xl">{{ selectedLesson.image }}</div>
        <div><h4 class="text-sm font-bold text-slate-700">Mô tả</h4><p class="mt-1 text-sm leading-6 text-slate-500">{{ selectedLesson.description }}</p></div>
        <div><h4 class="text-sm font-bold text-slate-700">Từ vựng / âm cần luyện</h4><div class="mt-2 flex flex-wrap gap-2"><span v-for="word in selectedLesson.vocabulary" :key="word" class="rounded-lg bg-blue-50 px-3 py-1.5 text-sm font-semibold text-blue-700">{{ word }}</span></div></div>
        <div class="rounded-xl border border-slate-100 p-4"><h4 class="text-sm font-bold text-slate-700">Hướng dẫn phát âm</h4><p class="mt-1 text-sm leading-6 text-slate-500">{{ selectedLesson.guide }}</p><p class="mt-3 text-xs text-slate-400">{{ selectedLesson.audio }}</p></div>
        <p v-if="selectedLesson.note" class="rounded-xl bg-rose-50 p-3 text-sm text-rose-700"><strong>Ghi chú:</strong> {{ selectedLesson.note }}</p>
      </div>
      <template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600" @click="dialog = ''">Đóng</button><template v-if="selectedLesson?.status === 'Pending'"><button type="button" class="rounded-xl border border-rose-200 px-4 py-2.5 text-sm font-semibold text-rose-700" @click="rejectionReason = ''; dialog = 'reject'">Từ chối</button><button type="button" class="rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-emerald-700" @click="approveLesson(selectedLesson)">Phê duyệt</button></template></template>
    </AdminModal>
    <AdminModal :model-value="dialog === 'reject'" title="Từ chối bài học" @update:model-value="dialog = ''" @submit="rejectLesson">
      <p class="mb-3 text-sm text-slate-600">Ghi chú để giáo viên chỉnh sửa bài <strong>{{ selectedLesson?.title }}</strong>.</p><textarea v-model.trim="rejectionReason" required rows="4" class="w-full rounded-xl border border-slate-200 p-3 text-sm outline-none focus:border-admin-cta" placeholder="Nêu rõ nội dung cần bổ sung hoặc chỉnh sửa..." />
      <template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold" @click="dialog = ''">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white">Xác nhận từ chối</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
