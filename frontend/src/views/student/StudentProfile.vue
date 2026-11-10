<script setup>
import { computed, onMounted, ref } from 'vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import TeacherUpgradeForm from '../../components/student/TeacherUpgradeForm.vue'
import { studentAccountService } from '../../services/studentAccountService'

const profile = ref(null)
const draft = ref(null)
const editing = ref(false)
const changePassword = ref(false)
const showCurrentPassword = ref(false)
const showNewPassword = ref(false)
const showConfirmPassword = ref(false)
const passwordDraft = ref({ current: '', next: '', confirm: '' })
const upgradeHistory = ref([])
const upgradeFormOpen = ref(false)
const avatarInput = ref(null)
const errorMessage = ref('')
const successMessage = ref('')
const passwordMessage = ref('')
const today = new Date().toISOString().slice(0, 10)

const latestRequest = computed(() => upgradeHistory.value[0] || null)
const canRequestUpgrade = computed(() => profile.value?.role !== 'Giảng viên' && latestRequest.value?.status !== 'pending')

function cloneProfile(value) {
  return { ...value }
}

function formatDate(value, includeTime = false) {
  if (!value) return '—'
  const date = new Date(value)
  return date.toLocaleString('vi-VN', includeTime
    ? { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }
    : { day: '2-digit', month: 'long', year: 'numeric' })
}

function statusLabel(status) {
  return {
    pending: 'Đang chờ xét duyệt',
    approved: 'Đã được phê duyệt',
    rejected: 'Yêu cầu bị từ chối',
  }[status] || 'Chưa gửi yêu cầu'
}

function statusStyle(status) {
  return status === 'approved'
    ? 'bg-emerald-50 text-emerald-800'
    : status === 'rejected' ? 'bg-rose-50 text-rose-800' : 'bg-amber-50 text-amber-900'
}

function startEditing() {
  errorMessage.value = ''
  successMessage.value = ''
  draft.value = cloneProfile(profile.value)
  editing.value = true
}

function cancelEditing() {
  draft.value = null
  editing.value = false
  errorMessage.value = ''
  if (avatarInput.value) avatarInput.value.value = ''
}

function previewAvatar(event) {
  const file = event.currentTarget.files?.[0]
  event.currentTarget.value = ''
  if (!file) return
  errorMessage.value = ''
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Vui lòng chọn tệp hình ảnh.'
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    errorMessage.value = 'Ảnh đại diện không được lớn hơn 2 MB.'
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    if (typeof reader.result !== 'string' || !draft.value) {
      errorMessage.value = 'Không thể xem trước ảnh đã chọn.'
      return
    }
    draft.value.avatar = reader.result
  }
  reader.onerror = () => { errorMessage.value = 'Không thể đọc tệp hình ảnh.' }
  reader.readAsDataURL(file)
}

function removeAvatar() {
  if (draft.value) draft.value.avatar = ''
}

function saveProfile(event) {
  errorMessage.value = ''
  successMessage.value = ''
  if (!event.currentTarget.reportValidity()) return
  if (draft.value.phone && !/^[+()\d\s.-]{7,20}$/.test(draft.value.phone)) {
    errorMessage.value = 'Vui lòng nhập số điện thoại hợp lệ.'
    return
  }
  if (draft.value.birthDate && new Date(draft.value.birthDate) > new Date()) {
    errorMessage.value = 'Ngày sinh không thể ở trong tương lai.'
    return
  }
  try {
    profile.value = studentAccountService.saveProfile(draft.value)
    editing.value = false
    draft.value = null
    successMessage.value = 'Đã lưu hồ sơ trên trình duyệt này.'
  } catch (error) {
    console.error('Không thể lưu hồ sơ học sinh.', error)
    errorMessage.value = error.message || 'Không thể lưu hồ sơ. Hãy thử lại.'
  }
}

function submitPassword(event) {
  passwordMessage.value = ''
  if (!event.currentTarget.reportValidity()) return
  if (passwordDraft.value.next.length < 8) {
    passwordMessage.value = 'Mật khẩu mới cần có ít nhất 8 ký tự.'
    return
  }
  if (passwordDraft.value.next === passwordDraft.value.current) {
    passwordMessage.value = 'Mật khẩu mới cần khác mật khẩu hiện tại.'
    return
  }
  if (passwordDraft.value.next !== passwordDraft.value.confirm) {
    passwordMessage.value = 'Mật khẩu xác nhận chưa trùng khớp.'
    return
  }
  try {
    studentAccountService.updatePassword(passwordDraft.value.current, passwordDraft.value.next)
    successMessage.value = 'Đã cập nhật mật khẩu mô phỏng trên trình duyệt này.'
    passwordMessage.value = ''
    passwordDraft.value = { current: '', next: '', confirm: '' }
    changePassword.value = false
  } catch (error) {
    console.error('Không thể cập nhật mật khẩu mô phỏng.', error)
    passwordMessage.value = error.message || 'Không thể cập nhật mật khẩu.'
  }
}

function submitUpgrade(details) {
  try {
    const request = studentAccountService.submitUpgradeRequest(details)
    upgradeHistory.value.unshift(request)
    upgradeFormOpen.value = false
    successMessage.value = 'Đã gửi yêu cầu nâng cấp. Yêu cầu đang chờ quản trị viên xem xét.'
  } catch (error) {
    console.error('Không thể gửi yêu cầu nâng cấp mô phỏng.', error)
    errorMessage.value = error.message || 'Không thể gửi yêu cầu. Hãy thử lại.'
  }
}

function loadProfile() {
  errorMessage.value = ''
  try {
    profile.value = studentAccountService.getProfile()
    upgradeHistory.value = studentAccountService.getUpgradeHistory()
  } catch (error) {
    console.error('Không thể tải hồ sơ học sinh.', error)
    errorMessage.value = error.message || 'Không thể tải hồ sơ trên trình duyệt này.'
  }
}

onMounted(loadProfile)
</script>

<template>
  <section class="mx-auto max-w-[1180px] space-y-5 p-4 sm:p-6 xl:p-8">
    <header class="flex flex-wrap items-end justify-between gap-3">
      <div><p class="text-xs font-extrabold uppercase tracking-[0.16em] text-kids-cta">Không gian của con</p><h2 class="mt-1 text-2xl font-extrabold text-kids-text sm:text-3xl">Hồ sơ cá nhân</h2><p class="mt-2 text-sm text-slate-500">Quản lý thông tin và tùy chọn bảo mật trong bản demo.</p></div>
      <span class="rounded-full bg-sky-50 px-3 py-1.5 text-[10px] font-bold text-sky-800">Dữ liệu lưu trên trình duyệt</span>
    </header>

    <p v-if="successMessage" class="rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-xs font-semibold text-emerald-800" role="status">{{ successMessage }}</p>
    <p v-if="errorMessage" class="rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-xs font-semibold text-rose-800" role="alert">{{ errorMessage }}</p>
    <div v-if="!profile" class="rounded-2xl bg-white p-8 text-center text-sm text-slate-500">Chưa tải được hồ sơ. <button type="button" class="font-bold text-sky-700" @click="loadProfile">Thử lại</button></div>
    <template v-else>
      <form class="overflow-hidden rounded-3xl border border-amber-100 bg-white shadow-sm" @submit.prevent="saveProfile">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-amber-100 bg-gradient-to-r from-amber-50/80 to-sky-50/60 px-4 py-4 sm:px-6">
          <div class="flex items-center gap-3">
            <div class="flex h-[68px] w-[68px] shrink-0 items-center justify-center overflow-hidden rounded-full border-4 border-white bg-kids-secondary/25 text-lg font-extrabold text-sky-800 shadow-sm">
              <img v-if="editing ? draft?.avatar : profile.avatar" :src="editing ? draft.avatar : profile.avatar" alt="Ảnh đại diện học sinh" class="h-full w-full object-cover" />
              <span v-else>{{ profile.name.split(' ').map((part) => part[0]).slice(0, 2).join('') }}</span>
            </div>
            <div><h3 class="text-base font-extrabold text-kids-text">{{ profile.name }}</h3><p class="mt-1 text-xs text-slate-500">{{ profile.role }} · {{ profile.username }}</p>
              <div v-if="editing" class="mt-2 flex flex-wrap gap-2">
                <label class="inline-flex cursor-pointer items-center gap-1.5 rounded-lg border border-sky-200 bg-white px-3 py-2 text-[10px] font-bold text-sky-800 hover:bg-sky-50"><AdminIcon name="image" :size="14" />{{ draft.avatar ? 'Đổi ảnh' : 'Chọn ảnh' }}<input ref="avatarInput" type="file" accept="image/*" class="sr-only" aria-label="Chọn ảnh đại diện" @change="previewAvatar" /></label>
                <button v-if="draft.avatar" type="button" class="rounded-lg border border-rose-100 bg-white px-3 py-2 text-[10px] font-bold text-rose-600 hover:bg-rose-50" @click="removeAvatar">Xóa ảnh</button>
                <span class="self-center text-[9px] text-slate-400">Ảnh tối đa 2 MB · xem trước trước khi lưu</span>
              </div>
            </div>
          </div>
          <div v-if="!editing"><button type="button" class="inline-flex min-h-10 items-center gap-2 rounded-xl bg-kids-primary px-4 text-xs font-extrabold text-kids-text hover:bg-amber-400" @click="startEditing"><AdminIcon name="edit" :size="15" />Chỉnh sửa hồ sơ</button></div>
          <div v-else class="flex gap-2"><button type="button" class="min-h-10 rounded-xl border border-slate-200 bg-white px-4 text-xs font-bold text-slate-600 hover:bg-slate-50" @click="cancelEditing">Hủy</button><button type="submit" class="inline-flex min-h-10 items-center gap-2 rounded-xl bg-kids-cta px-4 text-xs font-extrabold text-white hover:bg-orange-600"><AdminIcon name="check" :size="15" />Lưu thay đổi</button></div>
        </div>

        <div class="grid gap-5 p-4 sm:p-6 lg:grid-cols-2">
          <div class="space-y-4">
            <h4 class="flex items-center gap-2 text-xs font-extrabold text-slate-700"><AdminIcon name="profile" :size="16" class="text-sky-700" />Thông tin cá nhân</h4>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Họ và tên
              <input v-if="editing" v-model="draft.name" required minlength="2" maxlength="100" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-xs font-normal outline-none focus:border-sky-400" />
              <span v-else class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-700">{{ profile.name }}</span>
            </label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Số điện thoại
              <input v-if="editing" v-model="draft.phone" type="tel" maxlength="20" placeholder="Số điện thoại" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-xs font-normal outline-none focus:border-sky-400" />
              <span v-else class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-700">{{ profile.phone || 'Chưa cập nhật' }}</span>
            </label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Ngày sinh
              <input v-if="editing" v-model="draft.birthDate" type="date" :max="today" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-xs font-normal outline-none focus:border-sky-400" />
              <span v-else class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-700">{{ profile.birthDate ? formatDate(profile.birthDate) : 'Chưa cập nhật' }}</span>
            </label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Giới tính
              <select v-if="editing" v-model="draft.gender" class="h-10 w-full rounded-xl border border-slate-200 bg-white px-3 text-xs font-normal outline-none focus:border-sky-400"><option value="">Chưa chọn</option><option value="Nữ">Nữ</option><option value="Nam">Nam</option><option value="Khác">Khác</option></select>
              <span v-else class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-700">{{ profile.gender || 'Chưa cập nhật' }}</span>
            </label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Địa chỉ
              <input v-if="editing" v-model="draft.address" maxlength="200" class="h-10 w-full rounded-xl border border-slate-200 px-3 text-xs font-normal outline-none focus:border-sky-400" />
              <span v-else class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-700">{{ profile.address || 'Chưa cập nhật' }}</span>
            </label>
          </div>
          <div class="space-y-4">
            <h4 class="flex items-center gap-2 text-xs font-extrabold text-slate-700"><AdminIcon name="lock" :size="16" class="text-violet-700" />Thông tin tài khoản</h4>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Tên đăng nhập<span class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-500">{{ profile.username }}</span></label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Email<span class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-500">{{ profile.email }}</span></label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Vai trò tài khoản<span class="flex min-h-10 items-center justify-between rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-500">{{ profile.role }}<AdminIcon name="lock" :size="14" /></span></label>
            <label class="block space-y-1.5 text-[11px] font-bold text-slate-600">Ngày tham gia<span class="flex min-h-10 items-center rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-500">{{ formatDate(profile.joinedAt) }}</span></label>
            <div class="rounded-2xl border border-violet-100 bg-violet-50/60 p-4">
              <div class="flex items-center justify-between gap-3"><div><h4 class="text-xs font-extrabold text-violet-950">Bảo mật tài khoản</h4><p class="mt-1 text-[10px] text-violet-800">Đổi mật khẩu được mô phỏng trên trình duyệt.</p></div><button type="button" class="rounded-lg border border-violet-200 bg-white px-3 py-2 text-[10px] font-bold text-violet-800 hover:bg-violet-100" @click="changePassword = !changePassword">{{ changePassword ? 'Đóng' : 'Đổi mật khẩu' }}</button></div>
              <form v-if="changePassword" class="mt-4 space-y-3" @submit.prevent="submitPassword">
                <label class="block space-y-1 text-[10px] font-bold text-slate-600">Mật khẩu hiện tại<span class="relative block"><input v-model="passwordDraft.current" required :type="showCurrentPassword ? 'text' : 'password'" autocomplete="current-password" class="h-10 w-full rounded-xl border border-slate-200 bg-white px-3 pr-10 text-xs outline-none focus:border-violet-400" /><button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-slate-400" :aria-label="showCurrentPassword ? 'Ẩn mật khẩu hiện tại' : 'Hiện mật khẩu hiện tại'" @click="showCurrentPassword = !showCurrentPassword"><AdminIcon :name="showCurrentPassword ? 'eye' : 'eyeOff'" :size="15" /></button></span></label>
                <label class="block space-y-1 text-[10px] font-bold text-slate-600">Mật khẩu mới<span class="relative block"><input v-model="passwordDraft.next" required minlength="8" :type="showNewPassword ? 'text' : 'password'" autocomplete="new-password" class="h-10 w-full rounded-xl border border-slate-200 bg-white px-3 pr-10 text-xs outline-none focus:border-violet-400" /><button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-slate-400" :aria-label="showNewPassword ? 'Ẩn mật khẩu mới' : 'Hiện mật khẩu mới'" @click="showNewPassword = !showNewPassword"><AdminIcon :name="showNewPassword ? 'eye' : 'eyeOff'" :size="15" /></button></span><span class="text-[9px] font-normal text-slate-400">Ít nhất 8 ký tự</span></label>
                <label class="block space-y-1 text-[10px] font-bold text-slate-600">Xác nhận mật khẩu mới<span class="relative block"><input v-model="passwordDraft.confirm" required minlength="8" :type="showConfirmPassword ? 'text' : 'password'" autocomplete="new-password" class="h-10 w-full rounded-xl border border-slate-200 bg-white px-3 pr-10 text-xs outline-none focus:border-violet-400" /><button type="button" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-slate-400" :aria-label="showConfirmPassword ? 'Ẩn xác nhận mật khẩu' : 'Hiện xác nhận mật khẩu'" @click="showConfirmPassword = !showConfirmPassword"><AdminIcon :name="showConfirmPassword ? 'eye' : 'eyeOff'" :size="15" /></button></span></label>
                <p v-if="passwordMessage" class="text-[10px] text-violet-900" role="status">{{ passwordMessage }}</p>
                <button type="submit" class="min-h-9 rounded-lg bg-violet-700 px-3 text-[10px] font-bold text-white hover:bg-violet-800">Cập nhật mật khẩu</button>
              </form>
            </div>
          </div>
        </div>
        <p v-if="editing && errorMessage" class="mx-4 mb-4 rounded-xl bg-rose-50 px-3 py-2 text-xs text-rose-700 sm:mx-6" role="alert">{{ errorMessage }}</p>
      </form>

      <section class="overflow-hidden rounded-3xl border border-sky-100 bg-white shadow-sm" aria-labelledby="teacher-upgrade-heading">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-sky-100 bg-gradient-to-r from-sky-50 to-white px-4 py-4 sm:px-6">
          <div class="flex items-center gap-3"><span class="flex h-11 w-11 items-center justify-center rounded-xl bg-sky-100 text-sky-800"><AdminIcon name="education" :size="21" /></span><div><h3 id="teacher-upgrade-heading" class="text-base font-extrabold text-kids-text">Nâng cấp tài khoản giảng viên</h3><p class="mt-1 text-[10px] text-slate-500">Chia sẻ kiến thức và đồng hành cùng người học.</p></div></div>
          <span class="rounded-full px-3 py-1.5 text-[10px] font-extrabold" :class="latestRequest ? statusStyle(latestRequest.status) : 'bg-slate-100 text-slate-600'">{{ latestRequest ? statusLabel(latestRequest.status) : `Vai trò hiện tại: ${profile.role}` }}</span>
        </div>
        <div class="grid gap-5 p-4 sm:p-6 lg:grid-cols-[1fr_auto] lg:items-center">
          <div>
            <template v-if="profile.role === 'Giảng viên'">
              <p class="text-sm font-bold text-emerald-800">Tài khoản của bạn đã được cập nhật vai trò Giảng viên trong dữ liệu mô phỏng.</p>
              <p class="mt-1 text-xs leading-5 text-slate-500">Không cần gửi yêu cầu nâng cấp mới.</p>
            </template>
            <template v-else-if="latestRequest?.status === 'pending'">
              <p class="text-sm font-bold text-amber-900">Yêu cầu của bạn đã được gửi và đang chờ quản trị viên xem xét.</p>
              <p class="mt-1 text-xs text-slate-500">Mã {{ latestRequest.id }} · Gửi ngày {{ formatDate(latestRequest.submittedAt, true) }}. Vai trò hiện tại vẫn là {{ profile.role }}.</p>
              <p class="mt-2 text-[10px] text-slate-400">Không thể gửi yêu cầu mới khi yêu cầu này chưa được xử lý.</p>
            </template>
            <template v-else-if="latestRequest?.status === 'approved'">
              <p class="text-sm font-bold text-emerald-800">Yêu cầu nâng cấp đã được chấp thuận.</p>
              <p class="mt-1 text-xs text-slate-500">Vai trò tài khoản đã chuyển sang Giảng viên trong dữ liệu mô phỏng.</p>
            </template>
            <template v-else-if="latestRequest?.status === 'rejected'">
              <p class="text-sm font-bold text-rose-800">Yêu cầu trước đó chưa được chấp thuận.</p>
              <p class="mt-1 text-xs text-slate-500">{{ latestRequest.note || 'Không có ghi chú từ người xét duyệt.' }} Bạn có thể cập nhật thông tin và gửi lại.</p>
            </template>
            <template v-else>
              <p class="text-xs leading-5 text-slate-600">Giảng viên có thể chia sẻ chủ đề, theo dõi tiến độ học tập và trao đổi cùng học sinh được phân công. Quản trị viên sẽ xem xét thông tin trước khi thay đổi vai trò.</p>
              <p class="mt-2 text-[10px] text-slate-400">Hãy chuẩn bị thông tin chuyên môn và lý do muốn tham gia giảng dạy.</p>
            </template>
          </div>
          <button v-if="canRequestUpgrade" type="button" class="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-kids-cta px-4 text-xs font-extrabold text-white hover:bg-orange-600" @click="upgradeFormOpen = true"><AdminIcon name="send" :size="15" />Gửi yêu cầu nâng cấp tài khoản</button>
        </div>
        <div v-if="upgradeHistory.length" class="border-t border-slate-100 px-4 py-4 sm:px-6">
          <h4 class="text-xs font-extrabold text-slate-700">Lịch sử yêu cầu</h4>
          <div class="mt-3 space-y-2">
            <article v-for="request in upgradeHistory" :key="request.id" class="grid gap-2 rounded-xl bg-slate-50 p-3 sm:grid-cols-[1fr_auto] sm:items-center">
              <div><p class="text-[11px] font-bold text-slate-700">{{ request.id }} · {{ formatDate(request.submittedAt, true) }}</p><p v-if="request.reviewedAt" class="mt-1 text-[10px] text-slate-500">Xét duyệt {{ formatDate(request.reviewedAt, true) }}<span v-if="request.note"> · {{ request.note }}</span></p><p v-else class="mt-1 text-[10px] text-slate-500">Chưa có ngày xét duyệt</p></div>
              <span class="w-fit rounded-full px-2.5 py-1 text-[9px] font-bold" :class="statusStyle(request.status)">{{ statusLabel(request.status) }}</span>
            </article>
          </div>
        </div>
      </section>
    </template>

    <TeacherUpgradeForm v-if="upgradeFormOpen && profile" :profile="profile" @cancel="upgradeFormOpen = false" @submit="submitUpgrade" />
  </section>
</template>
