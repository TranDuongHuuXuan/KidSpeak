<script setup>
import { ref } from 'vue'
import AdminIcon from '../admin/AdminIcon.vue'

const props = defineProps({
  profile: { type: Object, required: true },
  previousRequest: { type: Object, default: null },
  submitting: { type: Boolean, default: false },
  serverError: { type: String, default: '' },
})
const emit = defineEmits(['cancel', 'submit'])
const form = ref({
  specialty: props.previousRequest?.specialty || '',
  experience: props.previousRequest?.experience || '',
  reason: props.previousRequest?.reason || '',
  introduction: props.previousRequest?.introduction || '',
})
const files = ref([])
const retainedDocuments = ref([...(props.previousRequest?.documents || [])])
const errorMessage = ref('')
const allowedExtensions = ['pdf', 'docx', 'jpg', 'jpeg', 'png', 'webp', 'xls', 'xlsx']
const maxFileSize = 10 * 1024 * 1024

function addFiles(event) {
  const selectedFiles = Array.from(event.currentTarget.files || [])
  errorMessage.value = ''
  for (const file of selectedFiles) {
    const extension = file.name.split('.').at(-1)?.toLowerCase()
    if (!allowedExtensions.includes(extension)) {
      errorMessage.value = 'Unsupported document format.'
      continue
    }
    if (file.size > maxFileSize) {
      errorMessage.value = `File ${file.name} exceeds the 10 MB limit.`
      continue
    }
    if (!files.value.some((item) => item.name === file.name && item.size === file.size)) files.value.push(file)
  }
  if (files.value.length + retainedDocuments.value.length > 5) {
    files.value = files.value.slice(0, Math.max(0, 5 - retainedDocuments.value.length))
    errorMessage.value = 'A request can contain at most 5 documents.'
  }
  event.currentTarget.value = ''
}

function removeFile(index) { files.value.splice(index, 1) }
function removePreviousDocument(index) { retainedDocuments.value.splice(index, 1) }

function submit() {
  errorMessage.value = ''
  const reason = form.value.reason.trim()
  if (!reason) {
    errorMessage.value = 'Please provide a reason for your teacher request.'
    return
  }
  emit('submit', {
    ...form.value,
    specialty: form.value.specialty.trim(),
    experience: form.value.experience.trim(),
    reason,
    introduction: form.value.introduction.trim(),
    files: [...files.value],
    previous_request_id: props.previousRequest?.id,
    keep_document_keys: retainedDocuments.value.map((item) => item.file_key),
  })
}
</script>

<template>
  <div class="fixed inset-0 z-[60] flex items-end justify-center bg-slate-950/45 p-0 backdrop-blur-[2px] sm:items-center sm:p-5" role="presentation" @click.self="emit('cancel')">
    <section class="max-h-[94dvh] w-full max-w-2xl overflow-y-auto rounded-t-3xl bg-white p-5 shadow-2xl sm:rounded-3xl sm:p-7" role="dialog" aria-modal="true" aria-labelledby="teacher-upgrade-form-title">
      <header class="flex items-start justify-between gap-3">
        <div><p class="text-xs font-extrabold uppercase tracking-wider text-kids-cta">Cùng sẻ chia kiến thức</p><h2 id="teacher-upgrade-form-title" class="mt-1 text-xl font-extrabold text-kids-text">Yêu cầu nâng cấp giảng viên</h2><p class="mt-2 text-xs leading-5 text-slate-500">Điền thông tin để quản trị viên xem xét. Gửi yêu cầu không tự đổi vai trò tài khoản.</p></div>
        <button type="button" class="rounded-xl p-2 text-slate-400 hover:bg-slate-100" aria-label="Đóng biểu mẫu" @click="emit('cancel')"><AdminIcon name="close" /></button>
      </header>

      <form class="mt-5 space-y-4" @submit.prevent="submit">
        <div class="grid gap-3 sm:grid-cols-2">
          <label class="space-y-1.5 text-xs font-bold text-slate-600">Họ và tên
            <input :value="profile.name" readonly class="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 px-3 text-xs font-normal text-slate-500" />
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600">Email
            <input :value="profile.email" readonly class="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 px-3 text-xs font-normal text-slate-500" />
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600 sm:col-span-2">Ngày sinh
            <input :value="profile.dateOfBirth ? new Date(profile.dateOfBirth).toLocaleDateString('vi-VN') : 'Chưa cập nhật'" readonly class="h-10 w-full rounded-xl border border-slate-200 bg-slate-50 px-3 text-xs font-normal text-slate-500" />
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600 sm:col-span-2">Chuyên môn <span class="font-normal text-slate-400">(không bắt buộc)</span>
            <input v-model="form.specialty" maxlength="120" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-xs font-normal outline-none focus:border-sky-400" placeholder="Ví dụ: Giáo dục mầm non, ngôn ngữ học" />
            <span class="block font-normal text-slate-400">Lĩnh vực bạn có kiến thức hoặc chứng chỉ chuyên môn.</span>
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600 sm:col-span-2">Kinh nghiệm giảng dạy <span class="font-normal text-slate-400">(không bắt buộc)</span>
            <textarea v-model="form.experience" rows="2" maxlength="4000" class="w-full rounded-xl border border-slate-200 p-3 text-xs font-normal outline-none focus:border-sky-400" placeholder="Mô tả thời gian hoặc kinh nghiệm liên quan"></textarea>
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600 sm:col-span-2">Lý do muốn trở thành giảng viên <span class="text-rose-500">*</span>
            <textarea v-model="form.reason" required rows="3" maxlength="2000" class="w-full rounded-xl border border-slate-200 p-3 text-xs font-normal outline-none focus:border-sky-400" placeholder="Chia sẻ động lực và điều bạn muốn đóng góp"></textarea>
          </label>
          <label class="space-y-1.5 text-xs font-bold text-slate-600 sm:col-span-2">Giới thiệu bản thân <span class="font-normal text-slate-400">(không bắt buộc)</span>
            <textarea v-model="form.introduction" rows="3" maxlength="2000" class="w-full rounded-xl border border-slate-200 p-3 text-xs font-normal outline-none focus:border-sky-400" placeholder="Thông tin bổ sung để quản trị viên hiểu rõ hơn về bạn"></textarea>
          </label>
        </div>

        <div>
          <p v-if="previousRequest" class="mb-2 rounded-lg bg-amber-50 p-2 text-[11px] text-amber-900">Resubmitting rejected request #{{ previousRequest.id }}. Keep or remove previous documents below.</p>
          <ul v-if="retainedDocuments.length" class="mb-3 space-y-1.5">
            <li v-for="(document, index) in retainedDocuments" :key="document.file_key" class="flex items-center gap-2 rounded-lg bg-amber-50 px-3 py-2 text-[10px] text-slate-600"><AdminIcon name="attach" :size="14" /><span class="min-w-0 flex-1 truncate">{{ document.file_name }}</span><span>{{ (document.file_size / 1024 / 1024).toFixed(2) }} MB</span><button type="button" class="rounded p-1 text-rose-600" aria-label="Remove previous document" @click="removePreviousDocument(index)"><AdminIcon name="delete" :size="14" /></button></li>
          </ul>
          <p class="text-xs font-bold text-slate-600">Tài liệu minh chứng <span class="font-normal text-slate-400">(không bắt buộc)</span></p>
          <p class="mt-1 text-[10px] text-slate-400">Images (JPG, PNG, WebP), DOCX, Excel (XLS/XLSX) and PDF; max 10 MB per file, 5 files total. Private storage.</p>
          <label class="mt-2 flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-dashed border-sky-300 bg-sky-50/60 px-4 py-4 text-xs font-bold text-sky-800 transition hover:bg-sky-50">
            <AdminIcon name="upload" :size="17" /> Chọn tài liệu
          <input type="file" class="sr-only" multiple accept=".pdf,.docx,.jpg,.jpeg,.png,.webp,.xls,.xlsx" aria-label="Chọn tài liệu minh chứng" @change="addFiles" />
          </label>
          <ul v-if="files.length" class="mt-2 space-y-1.5">
            <li v-for="(file, index) in files" :key="`${file.name}-${file.size}`" class="flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-2 text-[10px] text-slate-600">
              <AdminIcon name="attach" :size="14" /><span class="min-w-0 flex-1 truncate">{{ file.name }}</span><span>{{ (file.size / 1024 / 1024).toFixed(2) }} MB</span>
              <button type="button" class="rounded p-1 text-rose-600 hover:bg-rose-50" :aria-label="`Xóa tệp ${file.name}`" @click="removeFile(index)"><AdminIcon name="delete" :size="14" /></button>
            </li>
          </ul>
        </div>
        <p v-if="serverError" class="rounded-xl bg-rose-50 px-3 py-2 text-xs text-rose-700" role="alert">{{ serverError }}</p>
        <p v-if="errorMessage" class="rounded-xl bg-rose-50 px-3 py-2 text-xs text-rose-700" role="alert">{{ errorMessage }}</p>
        <div class="flex flex-col-reverse gap-2 border-t border-slate-100 pt-4 sm:flex-row sm:justify-end">
          <button type="button" :disabled="submitting" class="min-h-10 rounded-xl border border-slate-200 px-4 text-xs font-bold text-slate-600 hover:bg-slate-50 disabled:opacity-50" @click="emit('cancel')">Hủy</button>
          <button type="submit" :disabled="submitting" class="inline-flex min-h-10 items-center justify-center gap-2 rounded-xl bg-kids-cta px-4 text-xs font-extrabold text-white hover:bg-orange-600"><AdminIcon name="send" :size="15" /> {{ submitting ? 'Submitting...' : 'Submit request' }}</button>
        </div>
      </form>
    </section>
  </div>
</template>
