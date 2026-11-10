<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { expertData } from '../../data/expertMockData'
import { expertService, notifyExpert } from '../../services/expertService'

const route = useRoute()
const router = useRouter()
const search = ref('')
const statusFilter = ref('')
const page = ref(1)
const pageSize = 8
const modalOpen = ref(false)
const editing = ref(null)
const selected = ref(null)
const selectedTab = ref('Tổng quan')
const form = ref({})
const messageSearch = ref('')
const messageDraft = ref('')
const messageList = ref(null)
const profileImageKey = 'kidspeak-expert-profile-image'
const profileImage = ref('')
const profile = ref({ name: 'Trần Thị Ngọc', email: 'ngoc.tran@kidspeak.vn', specialization: 'Giáo dục mầm non · Luyện phát âm', phone: '0901 234 567', bio: 'Đồng hành cùng trẻ trong hành trình phát triển ngôn ngữ và phát âm tự tin.' })

const configs = {
  topics: {
    collection: 'topics',
    title: 'Quản lý chủ đề',
    description: 'Tạo và tổ chức các chủ đề học tập thuộc phạm vi giảng dạy của bạn.',
    action: 'Tạo chủ đề',
    columns: [['id', 'Mã chủ đề'], ['title', 'Tiêu đề'], ['level', 'Cấp độ'], ['order', 'Thứ tự'], ['words', 'Từ vựng'], ['status', 'Trạng thái'], ['createdAt', 'Ngày tạo']],
    fields: [
      { key: 'title', label: 'Tiêu đề chủ đề', required: true },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
      { key: 'level', label: 'Cấp độ', type: 'select', options: ['Cơ bản', 'Trung cấp', 'Nâng cao'] },
      { key: 'order', label: 'Thứ tự hiển thị', type: 'number' },
      { key: 'status', label: 'Trạng thái', type: 'select', options: ['Bản nháp', 'Đã xuất bản', 'Ẩn'] },
      { key: 'words', label: 'Số từ vựng', type: 'number' },
    ],
  },
  vocabulary: {
    collection: 'vocabulary',
    title: 'Quản lý từ vựng',
    description: 'Quản lý từ chuẩn, phiên âm và tư liệu minh họa cho chủ đề.',
    action: 'Thêm từ vựng',
    columns: [['id', 'Mã từ'], ['word', 'Từ chuẩn'], ['phonetic', 'Phiên âm'], ['topic', 'Chủ đề'], ['media', 'Hình ảnh'], ['order', 'Thứ tự'], ['status', 'Trạng thái']],
    fields: [
      { key: 'word', label: 'Từ chuẩn', required: true },
      { key: 'topic', label: 'Chủ đề', type: 'select', options: expertData.topics.map((topic) => topic.title) },
      { key: 'phonetic', label: 'Phiên âm' },
      { key: 'meaning', label: 'Ý nghĩa', type: 'textarea' },
      { key: 'order', label: 'Thứ tự hiển thị', type: 'number' },
      { key: 'media', label: 'Tên hình ảnh (tùy chọn)' },
      { key: 'status', label: 'Trạng thái', type: 'select', options: ['Bản nháp', 'Đã xuất bản', 'Ẩn'] },
    ],
  },
  paths: {
    collection: 'paths',
    title: 'Lộ trình học tập',
    description: 'Thiết kế, sắp xếp và theo dõi các lộ trình cho học viên được phân công.',
    action: 'Tạo lộ trình',
    columns: [['id', 'Mã lộ trình'], ['title', 'Tên lộ trình'], ['level', 'Cấp độ'], ['topics', 'Chủ đề'], ['students', 'Học viên'], ['duration', 'Thời lượng'], ['status', 'Trạng thái']],
    fields: [
      { key: 'title', label: 'Tên lộ trình', required: true },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
      { key: 'goal', label: 'Mục tiêu học tập', type: 'textarea' },
      { key: 'level', label: 'Cấp độ', type: 'select', options: ['Cơ bản', 'Trung cấp', 'Nâng cao'] },
      { key: 'duration', label: 'Thời gian dự kiến' },
      { key: 'topics', label: 'Số chủ đề', type: 'number' },
      { key: 'students', label: 'Số học viên được áp dụng', type: 'number' },
      { key: 'status', label: 'Trạng thái', type: 'select', options: ['Bản nháp', 'Đang triển khai', 'Đã hoàn thành'] },
    ],
  },
  progress: {
    collection: 'students',
    title: 'Tiến độ học tập',
    description: 'Theo dõi tiến độ và xác định học viên cần được hỗ trợ.',
    columns: [['id', 'Mã học viên'], ['name', 'Học viên'], ['path', 'Lộ trình'], ['completed', 'Chủ đề hoàn thành'], ['progress', 'Tiến độ'], ['score', 'Điểm luyện tập'], ['pronunciation', 'Phát âm'], ['lastActive', 'Hoạt động gần nhất'], ['status', 'Tình trạng']],
  },
  students: {
    collection: 'students',
    title: 'Theo dõi học viên',
    description: 'Xem hồ sơ, lộ trình và lịch sử luyện tập của học viên được phân công.',
    columns: [['id', 'Mã học viên'], ['name', 'Học viên'], ['className', 'Lớp'], ['path', 'Lộ trình'], ['progress', 'Tiến độ'], ['score', 'Điểm TB'], ['lastActive', 'Hoạt động gần nhất'], ['status', 'Tình trạng']],
  },
  resources: {
    collection: 'resources',
    title: 'Kho học liệu',
    description: 'Sắp xếp học liệu theo chủ đề để sử dụng trong nội dung giảng dạy.',
    action: 'Thêm học liệu',
    columns: [['id', 'Mã tài nguyên'], ['title', 'Tên học liệu'], ['type', 'Loại'], ['topic', 'Chủ đề liên quan'], ['format', 'Tệp'], ['updatedAt', 'Cập nhật'], ['status', 'Trạng thái']],
    fields: [
      { key: 'title', label: 'Tên tài nguyên', required: true },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
      { key: 'type', label: 'Loại tài nguyên', type: 'select', options: ['Hình ảnh', 'Âm thanh', 'Video', 'Tài liệu', 'Bài tập'] },
      { key: 'topic', label: 'Chủ đề liên quan', type: 'select', options: expertData.topics.map((topic) => topic.title) },
      { key: 'format', label: 'Tên tệp / định dạng' },
      { key: 'status', label: 'Trạng thái', type: 'select', options: ['Bản nháp', 'Đang sử dụng', 'Ẩn'] },
    ],
  },
}

const section = computed(() => route.meta.expertSection)
const config = computed(() => configs[section.value])
const isMessages = computed(() => section.value === 'messages')
const isProfile = computed(() => section.value === 'profile')
const isSettings = computed(() => section.value === 'settings')
watch(isProfile, (visible) => {
  if (!visible) return
  try {
    profileImage.value = localStorage.getItem(profileImageKey) || ''
  } catch {
    notifyExpert('Không thể đọc ảnh hồ sơ đã lưu trong trình duyệt.', 'error')
  }
}, { immediate: true })
const rawRows = computed(() => config.value ? expertData[config.value.collection] : [])
const filters = computed(() => [...new Set(rawRows.value.map((row) => row.status).filter(Boolean))])
const filteredRows = computed(() => rawRows.value.filter((row) => {
  const query = search.value.trim().toLocaleLowerCase('vi')
  const matchesSearch = !query || Object.values(row).some((value) => String(value).toLocaleLowerCase('vi').includes(query))
  const matchesStatus = !statusFilter.value || row.status === statusFilter.value
  const matchesSupportFilter = route.query.status !== 'Cần hỗ trợ' || row.status === 'Cần hỗ trợ'
  return matchesSearch && matchesStatus && matchesSupportFilter
}))
const pageCount = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / pageSize)))
const pageRows = computed(() => filteredRows.value.slice((page.value - 1) * pageSize, page.value * pageSize))
const conversations = computed(() => expertData.conversations.filter((item) => {
  const query = messageSearch.value.trim().toLocaleLowerCase('vi')
  return !query || item.name.toLocaleLowerCase('vi').includes(query) || item.preview.toLocaleLowerCase('vi').includes(query)
}))
const activeConversation = ref(expertData.conversations[0] || null)
const detailTabs = ['Tổng quan', 'Lịch sử luyện tập', 'Phân tích phát âm', 'Nhận xét']

watch([search, statusFilter, () => route.query.status], () => { page.value = 1 })
watch(() => route.query.q, (query) => { search.value = String(query || '') }, { immediate: true })
watch(() => route.query.student, (studentId) => {
  if (studentId) activeConversation.value = expertData.conversations.find((item) => item.studentId === studentId) || activeConversation.value
}, { immediate: true })
watch(() => route.query.create, (create) => {
  if (create === '1' && config.value?.fields) {
    openCreate()
    router.replace({ name: route.name, query: { ...route.query, create: undefined } })
  }
}, { immediate: true })
watch(() => activeConversation.value?.messages.length, async () => {
  await nextTick()
  if (messageList.value) messageList.value.scrollTop = messageList.value.scrollHeight
})

const pageDescription = computed(() => config.value?.description || (
  isMessages.value ? 'Trao đổi trực tiếp với học viên được phân công. Tin nhắn đang lưu trong dữ liệu demo trên trình duyệt.' :
    isProfile.value ? 'Thông tin chuyên môn hiển thị trong không gian giảng viên.' :
      isSettings.value ? 'Tùy chỉnh thông báo và trải nghiệm làm việc của bạn.' : ''
))

function openCreate() {
  editing.value = null
  form.value = {}
  config.value.fields.forEach((field) => {
    form.value[field.key] = field.type === 'number' ? 0 : field.options?.[0] || ''
  })
  if (section.value === 'topics') Object.assign(form.value, { order: expertData.topics.length + 1, words: 0, status: 'Bản nháp' })
  if (section.value === 'vocabulary') Object.assign(form.value, { order: 1, status: 'Bản nháp' })
  if (section.value === 'paths') Object.assign(form.value, { topics: 0, students: 0, duration: '4 tuần', status: 'Bản nháp' })
  if (section.value === 'resources') Object.assign(form.value, { format: '', status: 'Bản nháp' })
  modalOpen.value = true
}

function openEdit(row) {
  editing.value = row
  form.value = { ...row }
  modalOpen.value = true
}

function saveRecord() {
  const missing = config.value.fields.find((field) => field.required && !String(form.value[field.key] || '').trim())
  if (missing) {
    notifyExpert(`Vui lòng nhập ${missing.label.toLocaleLowerCase('vi')}.`, 'error')
    return
  }
  try {
    const updates = { ...form.value }
    if (section.value === 'topics') updates.createdAt = editing.value?.createdAt || new Date().toISOString().slice(0, 10)
    if (section.value === 'paths') updates.createdAt = editing.value?.createdAt || new Date().toISOString().slice(0, 10)
    if (section.value === 'resources') updates.updatedAt = new Date().toISOString().slice(0, 10)
    if (editing.value) expertService.update(config.value.collection, editing.value.id, updates)
    else expertService.create(config.value.collection, updates)
    modalOpen.value = false
    notifyExpert(editing.value ? 'Đã cập nhật dữ liệu demo.' : 'Đã thêm dữ liệu demo.')
  } catch (error) {
    notifyExpert(error.message || 'Không thể lưu thay đổi.', 'error')
  }
}

function removeRecord(row) {
  if (!window.confirm(`Bạn có chắc muốn xóa “${row.title || row.word || row.name}”?`)) return
  try {
    expertService.remove(config.value.collection, row.id)
    notifyExpert('Đã xóa khỏi dữ liệu demo.')
  } catch (error) {
    notifyExpert(error.message || 'Không thể xóa mục này.', 'error')
  }
}

function viewStudent(student) {
  selected.value = student
  selectedTab.value = 'Tổng quan'
}

function messageStudent(student) {
  router.push({ name: 'ExpertMessages', query: { student: student.id } })
}

function adjustDifficulty(student) {
  if (!window.confirm(`Xác nhận điều chỉnh độ khó cho ${student.name}? Thay đổi này chỉ áp dụng trong dữ liệu demo.`)) return
  student.status = 'Đang theo dõi'
  notifyExpert('Đã cập nhật trạng thái theo dõi trong dữ liệu demo.')
}

function assignPractice(student) {
  notifyExpert(`Đã ghi nhận yêu cầu giao bài luyện cho ${student.name} trong phiên demo.`)
}

function markRead(conversation) {
  activeConversation.value = conversation
  conversation.unread = 0
}

function sendMessage() {
  const text = messageDraft.value.trim()
  if (!text || !activeConversation.value) return
  try {
    expertService.sendMessage(activeConversation.value.studentId, text)
    messageDraft.value = ''
  } catch (error) {
    notifyExpert(error.message || 'Không thể gửi tin nhắn.', 'error')
  }
}

function saveProfile(event) {
  if (!event.currentTarget.reportValidity()) return
  notifyExpert('Đã lưu hồ sơ trong phiên demo.')
}

function updateProfileImage(event) {
  const input = event.currentTarget
  const file = input.files?.[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    notifyExpert('Vui lòng chọn tệp hình ảnh.', 'error')
    input.value = ''
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    notifyExpert('Ảnh đại diện không được lớn hơn 2 MB.', 'error')
    input.value = ''
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    if (typeof reader.result !== 'string') {
      notifyExpert('Không thể đọc tệp hình ảnh.', 'error')
      return
    }

    try {
      localStorage.setItem(profileImageKey, reader.result)
      profileImage.value = reader.result
      notifyExpert('Đã cập nhật ảnh đại diện trên trình duyệt này.')
    } catch {
      notifyExpert('Không thể lưu ảnh trong trình duyệt. Hãy thử ảnh nhỏ hơn.', 'error')
    }
  }
  reader.onerror = () => notifyExpert('Không thể đọc tệp hình ảnh.', 'error')
  reader.readAsDataURL(file)
  input.value = ''
}

function removeProfileImage() {
  try {
    localStorage.removeItem(profileImageKey)
    profileImage.value = ''
    notifyExpert('Đã xóa ảnh đại diện đã lưu.')
  } catch {
    notifyExpert('Không thể xóa ảnh đại diện khỏi bộ nhớ trình duyệt.', 'error')
  }
}

function saveSettings() {
  notifyExpert('Đã lưu tùy chọn trong phiên demo.')
}

function ttsNotice() {
  notifyExpert('Google Text-to-Speech chưa được kết nối. Cần cấu hình API ở backend trước khi tạo âm thanh.', 'error')
}
</script>

<template>
  <section :class="isMessages || isProfile ? 'h-full min-h-0 p-0' : 'space-y-6 p-4 sm:p-7 lg:p-8'">
    <div v-if="!isMessages && !isProfile" class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p class="text-sm font-semibold text-blue-600">KidSpeak · Giảng viên</p>
        <h2 class="mt-1 text-2xl font-extrabold tracking-tight text-slate-800 sm:text-3xl">{{ config?.title || (isMessages ? 'Tin nhắn' : isProfile ? 'Hồ sơ cá nhân' : 'Cài đặt') }}</h2>
        <p class="mt-2 max-w-3xl text-sm leading-6 text-slate-500">{{ pageDescription }}</p>
      </div>
      <button v-if="config?.action" type="button" class="inline-flex items-center justify-center gap-2 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-blue-200" @click="openCreate">
        <AdminIcon name="plus" :size="17" />{{ config.action }}
      </button>
    </div>

    <template v-if="config">
      <div v-if="section === 'progress'" class="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <article v-for="stat in [
          { label: 'Tổng học viên', value: expertData.students.length, color: 'text-slate-800' },
          { label: 'Tiến bộ tốt', value: expertData.students.filter((item) => item.progress >= 60).length, color: 'text-emerald-600' },
          { label: 'Ổn định', value: expertData.students.filter((item) => item.status === 'Ổn định').length, color: 'text-blue-600' },
          { label: 'Cần hỗ trợ', value: expertData.students.filter((item) => item.status === 'Cần hỗ trợ').length, color: 'text-amber-600' },
          { label: 'Không hoạt động', value: expertData.students.filter((item) => item.lastActive.includes('ngày')).length, color: 'text-rose-600' },
        ]" :key="stat.label" class="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><p class="text-xs font-medium text-slate-500">{{ stat.label }}</p><p class="mt-2 text-2xl font-extrabold" :class="stat.color">{{ stat.value }}</p></article>
      </div>

      <div class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div class="flex flex-col gap-3 border-b border-slate-100 p-4 sm:flex-row sm:items-center sm:justify-between sm:px-5">
          <label class="flex h-10 w-full items-center gap-2 rounded-xl border border-slate-200 px-3 text-slate-400 sm:max-w-sm">
            <AdminIcon name="search" :size="17" />
            <input v-model="search" class="min-w-0 flex-1 text-sm text-slate-700 outline-none placeholder:text-slate-400" :placeholder="section === 'vocabulary' ? 'Tìm từ vựng, chủ đề...' : 'Tìm kiếm...'" aria-label="Tìm trong danh sách" />
          </label>
          <div class="flex items-center gap-2">
            <label class="sr-only" :for="`filter-${section}`">Lọc theo trạng thái</label>
            <select :id="`filter-${section}`" v-model="statusFilter" class="h-10 min-w-36 rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-600 outline-none focus:border-blue-400">
              <option value="">Tất cả trạng thái</option>
              <option v-for="filter in filters" :key="filter" :value="filter">{{ filter }}</option>
            </select>
            <span class="hidden text-xs text-slate-400 sm:inline">{{ filteredRows.length }} mục</span>
          </div>
        </div>

        <div v-if="pageRows.length" class="overflow-x-auto">
          <table class="w-full min-w-[920px] text-left text-sm">
            <thead class="bg-slate-50 text-[11px] font-bold uppercase tracking-wide text-slate-500">
              <tr><th v-for="column in config.columns" :key="column[0]" class="whitespace-nowrap px-4 py-3">{{ column[1] }}</th><th class="px-4 py-3 text-right">Thao tác</th></tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="row in pageRows" :key="row.id" class="transition hover:bg-slate-50/70">
                <td v-for="column in config.columns" :key="column[0]" class="max-w-[230px] px-4 py-3.5 text-slate-600">
                  <template v-if="column[0] === 'name' && row.initials">
                    <span class="flex items-center gap-2.5"><span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-[10px] font-bold" :class="row.color">{{ row.initials }}</span><span class="min-w-0"><span class="block truncate font-semibold text-slate-700">{{ row.name }}</span><span class="block text-[10px] text-slate-400">{{ row.className }}</span></span></span>
                  </template>
                  <template v-else-if="column[0] === 'progress'">
                    <span class="flex min-w-24 items-center gap-2"><span class="h-1.5 flex-1 overflow-hidden rounded-full bg-slate-100"><span class="block h-full rounded-full bg-blue-500" :style="{ width: `${row.progress}%` }"></span></span><strong class="text-xs text-slate-600">{{ row.progress }}%</strong></span>
                  </template>
                  <template v-else-if="column[0] === 'completed'">{{ row.completed }}/{{ row.total }} chủ đề</template>
                  <template v-else-if="column[0] === 'status'">
                    <span class="inline-flex whitespace-nowrap rounded-full px-2.5 py-1 text-[10px] font-semibold" :class="row.status === 'Cần hỗ trợ' ? 'bg-amber-50 text-amber-700' : row.status === 'Đã xuất bản' || row.status === 'Đang triển khai' || row.status === 'Đang sử dụng' || row.status === 'Đang tiến bộ' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'">{{ row.status }}</span>
                  </template>
                  <template v-else><span class="block truncate" :class="column[0] === 'id' ? 'font-mono text-xs text-slate-400' : 'font-medium text-slate-700'">{{ row[column[0]] ?? '—' }}</span></template>
                </td>
                <td class="whitespace-nowrap px-4 py-3 text-right">
                  <div class="flex justify-end gap-1">
                    <button v-if="section === 'students' || section === 'progress'" type="button" class="rounded-lg p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600" title="Xem hồ sơ học viên" aria-label="Xem hồ sơ học viên" @click="viewStudent(row)"><AdminIcon name="eye" :size="16" /></button>
                    <button v-if="section === 'students' || section === 'progress'" type="button" class="rounded-lg p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600" title="Nhắn tin" aria-label="Nhắn tin" @click="messageStudent(row)"><AdminIcon name="message" :size="16" /></button>
                    <button v-if="section === 'students' || section === 'progress'" type="button" class="rounded-lg p-2 text-slate-400 hover:bg-amber-50 hover:text-amber-600" title="Điều chỉnh độ khó" aria-label="Điều chỉnh độ khó" @click="adjustDifficulty(row)"><AdminIcon name="filter" :size="16" /></button>
                    <button v-if="section === 'students' || section === 'progress'" type="button" class="rounded-lg p-2 text-slate-400 hover:bg-emerald-50 hover:text-emerald-600" title="Giao bài luyện tập" aria-label="Giao bài luyện tập" @click="assignPractice(row)"><AdminIcon name="check" :size="16" /></button>
                    <template v-else>
                      <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600" title="Xem chi tiết" aria-label="Xem chi tiết" @click="selected = row"><AdminIcon name="eye" :size="16" /></button>
                      <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-blue-50 hover:text-blue-600" title="Chỉnh sửa" aria-label="Chỉnh sửa" @click="openEdit(row)"><AdminIcon name="edit" :size="16" /></button>
                      <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600" title="Xóa" aria-label="Xóa" @click="removeRecord(row)"><AdminIcon name="delete" :size="16" /></button>
                    </template>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="flex flex-col items-center px-6 py-14 text-center">
          <span class="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"><AdminIcon name="search" :size="22" /></span>
          <p class="mt-4 font-semibold text-slate-700">{{ rawRows.length ? 'Không tìm thấy kết quả phù hợp' : 'Chưa có dữ liệu' }}</p>
          <p class="mt-1 max-w-sm text-sm text-slate-400">{{ rawRows.length ? 'Thử từ khóa hoặc bộ lọc khác.' : 'Dữ liệu sẽ xuất hiện tại đây sau khi được tạo.' }}</p>
          <button v-if="config.action && !rawRows.length" type="button" class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700" @click="openCreate">{{ config.action }}</button>
        </div>

        <div v-if="filteredRows.length" class="flex flex-col items-center justify-between gap-3 border-t border-slate-100 px-4 py-3 sm:flex-row sm:px-5">
          <p class="text-xs text-slate-500">Hiển thị {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, filteredRows.length) }} trong {{ filteredRows.length }} mục</p>
          <div class="flex items-center gap-2">
            <button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="page === 1" @click="page--">Trước</button>
            <span class="text-xs text-slate-500">Trang {{ page }}/{{ pageCount }}</span>
            <button type="button" class="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="page >= pageCount" @click="page++">Sau</button>
          </div>
        </div>
      </div>
    </template>

    <section v-else-if="isMessages" class="grid h-full min-h-0 grid-rows-[minmax(170px,30%)_minmax(0,1fr)] overflow-hidden border border-slate-200 bg-white shadow-sm lg:grid-rows-1 lg:grid-cols-[280px_minmax(0,1fr)_250px]">
      <aside class="flex min-h-0 flex-col border-b border-slate-200 lg:border-b-0 lg:border-r">
        <div class="border-b border-slate-100 p-4"><h3 class="font-bold text-slate-800">Hội thoại</h3><label class="mt-3 flex h-9 items-center gap-2 rounded-lg bg-slate-100 px-3 text-slate-400"><AdminIcon name="search" :size="15" /><input v-model="messageSearch" class="min-w-0 flex-1 bg-transparent text-xs text-slate-700 outline-none" placeholder="Tìm hội thoại..." aria-label="Tìm hội thoại" /></label></div>
        <div class="min-h-0 flex-1 divide-y divide-slate-100 overflow-y-auto">
          <button v-for="conversation in conversations" :key="conversation.studentId" type="button" class="flex w-full items-center gap-3 p-3 text-left transition hover:bg-slate-50" :class="{ 'bg-blue-50/70': activeConversation?.studentId === conversation.studentId }" @click="markRead(conversation)">
            <span class="relative flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-xs font-bold" :class="conversation.color">{{ conversation.initials }}<i v-if="conversation.unread" class="absolute -right-0.5 -top-0.5 h-2.5 w-2.5 rounded-full bg-blue-600 ring-2 ring-white"></i></span>
            <span class="min-w-0 flex-1"><span class="flex items-center justify-between gap-2"><strong class="truncate text-xs text-slate-700">{{ conversation.name }}</strong><small class="shrink-0 text-[10px] text-slate-400">{{ conversation.time }}</small></span><span class="mt-1 block truncate text-[11px] text-slate-400">{{ conversation.preview }}</span></span>
          </button>
          <p v-if="!conversations.length" class="p-5 text-center text-xs text-slate-400">Không có hội thoại phù hợp.</p>
        </div>
      </aside>

      <div v-if="activeConversation" class="flex min-h-0 min-w-0 flex-col">
        <div class="flex items-center gap-3 border-b border-slate-100 px-4 py-3">
          <span class="flex h-9 w-9 items-center justify-center rounded-full text-xs font-bold" :class="activeConversation.color">{{ activeConversation.initials }}</span>
          <div class="min-w-0"><p class="truncate text-sm font-bold text-slate-800">{{ activeConversation.name }}</p><p class="text-[11px] text-slate-400">{{ activeConversation.studentId }}</p></div>
          <span class="ml-auto rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-semibold text-emerald-700">Được phân công</span>
        </div>
        <div ref="messageList" class="min-h-0 flex-1 space-y-4 overflow-y-auto bg-slate-50/60 p-4 sm:p-6">
          <p class="text-center text-[11px] text-slate-400">Cuộc trò chuyện · Tin nhắn demo trong phiên hiện tại</p>
          <div v-for="message in activeConversation.messages" :key="message.id" class="flex" :class="message.from === 'expert' ? 'justify-end' : 'justify-start'">
            <div class="max-w-[85%]">
              <div class="rounded-2xl px-4 py-2.5 text-sm leading-6" :class="message.from === 'expert' ? 'rounded-br-md bg-blue-600 text-white' : 'rounded-bl-md border border-slate-200 bg-white text-slate-700'">{{ message.text }}</div>
              <p class="mt-1 px-1 text-[10px] text-slate-400" :class="message.from === 'expert' ? 'text-right' : ''">{{ message.time }}</p>
            </div>
          </div>
        </div>
        <form class="flex items-center gap-2 border-t border-slate-100 p-3 sm:p-4" @submit.prevent="sendMessage">
          <button type="button" class="hidden rounded-lg p-2 text-slate-400 sm:block" title="Đính kèm sẽ khả dụng khi có API lưu trữ" aria-label="Đính kèm chưa khả dụng" @click="notifyExpert('Gửi tệp cần dịch vụ lưu trữ backend; tính năng chưa được kết nối.', 'error')"><AdminIcon name="attach" :size="18" /></button>
          <input v-model="messageDraft" class="h-11 min-w-0 flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 text-sm outline-none transition focus:border-blue-400 focus:bg-white" placeholder="Nhập tin nhắn..." aria-label="Nội dung tin nhắn" />
          <button type="submit" class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-blue-600 text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-40" :disabled="!messageDraft.trim()" aria-label="Gửi tin nhắn"><AdminIcon name="send" :size="17" /></button>
        </form>
        <p class="px-4 pb-3 text-center text-[10px] text-slate-400">Tin nhắn demo chỉ tồn tại trong phiên hiện tại · Chưa kết nối WebSocket</p>
      </div>
      <div v-else class="flex min-h-[460px] items-center justify-center p-8 text-sm text-slate-400">Chọn hội thoại để bắt đầu trao đổi.</div>

      <aside v-if="activeConversation" class="hidden border-l border-slate-200 p-5 lg:block">
        <h3 class="text-sm font-bold text-slate-800">Thông tin học viên</h3>
        <div class="mt-6 flex flex-col items-center text-center"><span class="flex h-16 w-16 items-center justify-center rounded-full text-lg font-bold" :class="activeConversation.color">{{ activeConversation.initials }}</span><p class="mt-3 font-bold text-slate-800">{{ activeConversation.name }}</p><p class="mt-1 text-xs text-slate-400">{{ activeConversation.studentId }}</p></div>
        <div class="mt-6 space-y-4 border-t border-slate-100 pt-4">
          <div><p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">Lộ trình đang học</p><p class="mt-1 text-xs font-semibold leading-5 text-slate-700">{{ activeConversation.path }}</p></div>
          <div><div class="flex justify-between text-xs"><span class="text-slate-500">Tiến độ</span><strong class="text-slate-700">{{ activeConversation.progress }}%</strong></div><div class="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-blue-500" :style="{ width: `${activeConversation.progress}%` }"></div></div></div>
        </div>
        <RouterLink :to="{ name: 'ExpertStudents' }" class="mt-6 flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-3 py-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"><AdminIcon name="profile" :size="15" />Danh sách học viên</RouterLink>
        <RouterLink :to="{ name: 'ExpertProgress' }" class="mt-2 flex items-center justify-center gap-2 rounded-xl border border-slate-200 px-3 py-2.5 text-xs font-semibold text-slate-600 hover:bg-slate-50"><AdminIcon name="chart" :size="15" />Xem tiến độ học tập</RouterLink>
      </aside>
    </section>

    <section v-else-if="isProfile" class="grid min-h-full gap-5 xl:h-full xl:min-h-0 xl:grid-cols-[minmax(0,1fr)_320px]">
      <form class="flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7" @submit.prevent="saveProfile">
        <h3 class="font-bold text-slate-800">Thông tin chuyên môn</h3><p class="mt-1 text-sm text-slate-400">Cập nhật hồ sơ hiển thị cho học viên được phân công.</p>
        <div class="mt-6 grid gap-4 sm:grid-cols-2">
          <label class="space-y-1.5 text-xs font-semibold text-slate-600">Họ và tên<input v-model="profile.name" required class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400" /></label>
          <label class="space-y-1.5 text-xs font-semibold text-slate-600">Email<input v-model="profile.email" type="email" required class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400" /></label>
          <label class="space-y-1.5 text-xs font-semibold text-slate-600">Số điện thoại<input v-model="profile.phone" type="tel" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400" /></label>
          <label class="space-y-1.5 text-xs font-semibold text-slate-600">Chuyên môn<input v-model="profile.specialization" required class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400" /></label>
          <label class="space-y-1.5 text-xs font-semibold text-slate-600 sm:col-span-2">Giới thiệu<textarea v-model="profile.bio" rows="4" class="w-full rounded-xl border border-slate-200 p-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400"></textarea></label>
        </div>
        <button type="submit" class="mt-auto self-start rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">Lưu hồ sơ</button>
      </form>
      <article class="h-full rounded-2xl border border-slate-200 bg-white p-6 text-center shadow-sm">
        <div class="mx-auto flex h-20 w-20 items-center justify-center overflow-hidden rounded-full bg-blue-100 text-xl font-bold text-blue-700">
          <img v-if="profileImage" :src="profileImage" alt="Ảnh đại diện giảng viên" class="h-full w-full object-cover" />
          <span v-else>TN</span>
        </div>
        <div class="mt-3 flex justify-center gap-2">
          <label class="cursor-pointer rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700">
            {{ profileImage ? 'Đổi ảnh' : 'Tải ảnh lên' }}
            <input type="file" accept="image/*" class="sr-only" aria-label="Tải ảnh đại diện lên" @change="updateProfileImage" />
          </label>
          <button v-if="profileImage" type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-rose-600 hover:bg-rose-50" @click="removeProfileImage">Xóa ảnh</button>
        </div>
        <p class="mt-2 text-[11px] text-slate-400">Ảnh định dạng hình ảnh, tối đa 2 MB. Được lưu trên trình duyệt này.</p>
        <h3 class="mt-4 font-bold text-slate-800">{{ profile.name }}</h3><p class="mt-1 text-xs text-slate-500">Giảng viên · KidSpeak</p>
        <div class="mt-5 space-y-2 border-t border-slate-100 pt-4 text-left text-xs text-slate-500"><p>{{ profile.email }}</p><p>{{ profile.specialization }}</p><p>{{ expertData.students.length }} học viên được phân công</p></div>
        <p class="mt-4 rounded-xl bg-blue-50 p-3 text-left text-xs leading-5 text-blue-700">Giao diện demo không xác minh danh tính. Quyền truy cập dữ liệu phải được backend kiểm tra.</p>
      </article>
    </section>

    <section v-else-if="isSettings" class="max-w-3xl space-y-5">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
        <h3 class="font-bold text-slate-800">Thông báo</h3><p class="mt-1 text-sm text-slate-400">Chọn loại cập nhật bạn muốn nhận.</p>
        <label class="mt-6 flex items-center justify-between gap-4 border-b border-slate-100 pb-4"><span><strong class="block text-sm text-slate-700">Thông báo qua email</strong><small class="mt-1 block text-xs text-slate-400">Nhận tin nhắn và cập nhật học viên.</small></span><input v-model="expertData.settings.emailNotifications" type="checkbox" class="h-4 w-4 accent-blue-600" /></label>
        <label class="mt-4 flex items-center justify-between gap-4"><span><strong class="block text-sm text-slate-700">Báo cáo hàng tuần</strong><small class="mt-1 block text-xs text-slate-400">Tổng hợp hoạt động của học viên được phân công.</small></span><input v-model="expertData.settings.weeklyReport" type="checkbox" class="h-4 w-4 accent-blue-600" /></label>
      </article>
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
        <h3 class="font-bold text-slate-800">Quyền riêng tư</h3><p class="mt-1 text-sm text-slate-400">Giới hạn người có thể xem hồ sơ giảng viên.</p>
        <label class="mt-5 block text-xs font-semibold text-slate-600">Phạm vi hiển thị<select v-model="expertData.settings.profileVisibility" class="mt-2 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400"><option>Học viên được phân công</option><option>Chỉ bản thân tôi</option></select></label>
        <button type="button" class="mt-5 rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700" @click="saveSettings">Lưu cài đặt</button>
      </article>
      <p class="rounded-xl border border-amber-200 bg-amber-50 p-4 text-xs leading-5 text-amber-800">Các tùy chọn trên chỉ được lưu trong phiên demo. Quyền truy cập phải được xác thực và kiểm tra ở backend.</p>
    </section>

    <div v-if="modalOpen && config?.fields" class="fixed inset-0 z-[60] flex items-center justify-center overflow-y-auto bg-slate-950/45 p-4" @click.self="modalOpen = false">
      <form class="my-auto max-h-[min(90dvh,900px)] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white shadow-2xl" @submit.prevent="saveRecord">
        <div class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-100 bg-white px-5 py-4 sm:px-6"><div><h3 class="font-bold text-slate-800">{{ editing ? 'Chỉnh sửa' : config.action }}</h3><p class="mt-1 text-xs text-slate-400">Thay đổi chỉ áp dụng với dữ liệu demo trong phiên hiện tại.</p></div><button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Đóng" @click="modalOpen = false"><AdminIcon name="close" /></button></div>
        <div class="grid gap-4 p-5 sm:grid-cols-2 sm:p-6">
          <label v-for="field in config.fields" :key="field.key" class="space-y-1.5 text-xs font-semibold text-slate-600" :class="{ 'sm:col-span-2': field.type === 'textarea' }">
            {{ field.label }}<span v-if="field.required" class="text-rose-500"> *</span>
            <textarea v-if="field.type === 'textarea'" v-model="form[field.key]" rows="3" class="w-full rounded-xl border border-slate-200 p-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400"></textarea>
            <select v-else-if="field.type === 'select'" v-model="form[field.key]" class="h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400"><option v-for="option in field.options" :key="option" :value="option">{{ option }}</option></select>
            <input v-else v-model="form[field.key]" :type="field.type || 'text'" :required="field.required" class="h-11 w-full rounded-xl border border-slate-200 px-3 text-sm font-normal text-slate-700 outline-none focus:border-blue-400" />
          </label>
          <div v-if="section === 'vocabulary'" class="sm:col-span-2">
            <div class="rounded-xl border border-blue-100 bg-blue-50/60 p-4">
              <div class="flex items-start gap-3"><span class="rounded-lg bg-white p-2 text-blue-600"><AdminIcon name="microphone" :size="18" /></span><div class="min-w-0 flex-1"><p class="text-sm font-bold text-slate-700">Âm thanh mẫu</p><p class="mt-1 text-xs leading-5 text-slate-500">Google Text-to-Speech chưa được kết nối. Không có âm thanh giả được tạo trong giao diện.</p></div></div>
              <div class="mt-3 flex flex-wrap gap-2"><button type="button" class="rounded-lg bg-blue-600 px-3 py-2 text-xs font-semibold text-white hover:bg-blue-700" @click="ttsNotice">Tạo âm thanh bằng Google TTS</button><button type="button" class="rounded-lg border border-slate-200 bg-white px-3 py-2 text-xs font-semibold text-slate-600" @click="notifyExpert('Tải tệp âm thanh cần backend lưu trữ; tính năng chưa được kết nối.', 'error')">Chọn file âm thanh</button></div>
            </div>
          </div>
          <div v-if="section === 'resources'" class="sm:col-span-2"><p class="rounded-xl border border-dashed border-slate-300 p-4 text-xs leading-5 text-slate-500">Tệp chỉ có thể được tải lên khi tích hợp dịch vụ lưu trữ backend. Trường “Tên tệp / định dạng” hiện lưu thông tin mô tả, không tải tệp lên máy chủ.</p></div>
        </div>
        <div class="flex justify-end gap-2 border-t border-slate-100 px-5 py-4 sm:px-6"><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="modalOpen = false">Hủy</button><button type="submit" class="rounded-xl bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">{{ editing ? 'Lưu thay đổi' : 'Tạo mới' }}</button></div>
      </form>
    </div>

    <div v-if="selected" class="fixed inset-0 z-[60] flex items-center justify-center overflow-y-auto bg-slate-950/45 p-4" @click.self="selected = null">
      <section class="my-auto max-h-[90dvh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white shadow-2xl">
        <div class="flex items-start justify-between border-b border-slate-100 p-5 sm:p-6"><div><p class="text-xs font-semibold text-blue-600">{{ selected.id }}</p><h3 class="mt-1 text-xl font-bold text-slate-800">{{ selected.name || selected.title || selected.word }}</h3><p v-if="selected.path" class="mt-1 text-sm text-slate-500">{{ selected.path }}</p></div><button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100" aria-label="Đóng" @click="selected = null"><AdminIcon name="close" /></button></div>
        <template v-if="selected.progress !== undefined">
          <div class="flex gap-2 overflow-x-auto border-b border-slate-100 px-4 pt-3 sm:px-6"><button v-for="tab in detailTabs" :key="tab" type="button" class="whitespace-nowrap border-b-2 px-2 py-2 text-xs font-semibold" :class="selectedTab === tab ? 'border-blue-600 text-blue-700' : 'border-transparent text-slate-500'" @click="selectedTab = tab">{{ tab }}</button></div>
          <div class="space-y-4 p-5 sm:p-6">
            <template v-if="selectedTab === 'Tổng quan'">
              <div class="grid gap-3 sm:grid-cols-3"><div class="rounded-xl bg-slate-50 p-4"><p class="text-xs text-slate-400">Tiến độ</p><p class="mt-1 text-xl font-bold text-slate-800">{{ selected.progress }}%</p></div><div class="rounded-xl bg-slate-50 p-4"><p class="text-xs text-slate-400">Điểm luyện tập</p><p class="mt-1 text-xl font-bold text-slate-800">{{ selected.score }}/100</p></div><div class="rounded-xl bg-slate-50 p-4"><p class="text-xs text-slate-400">Phát âm</p><p class="mt-1 text-xl font-bold text-slate-800">{{ selected.pronunciation }}/100</p></div></div>
              <p class="text-sm text-slate-600">Đã hoàn thành {{ selected.completed }} trên {{ selected.total }} chủ đề · Lần học gần nhất: {{ selected.lastActive }}.</p>
            </template>
            <template v-else-if="selectedTab === 'Lịch sử luyện tập'"><div class="rounded-xl border border-slate-200 p-4"><p class="text-sm font-semibold text-slate-700">Hoạt động gần đây</p><p class="mt-2 text-sm text-slate-500">{{ selected.lastActive }} · {{ selected.path }} · Điểm {{ selected.score }}/100</p><p class="mt-2 text-xs text-slate-400">Lịch sử chi tiết sẽ hiển thị sau khi backend cung cấp dữ liệu luyện tập.</p></div></template>
            <template v-else-if="selectedTab === 'Phân tích phát âm'"><div class="rounded-xl border border-slate-200 p-4"><p class="text-sm font-semibold text-slate-700">Kết quả phát âm hiện tại: {{ selected.pronunciation }}/100</p><div class="mt-3 h-2 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-blue-500" :style="{ width: `${selected.pronunciation}%` }"></div></div><p class="mt-3 text-xs text-slate-400">Phân tích từng âm cần tích hợp dịch vụ chấm phát âm ở backend.</p></div></template>
            <template v-else><label class="block text-xs font-semibold text-slate-600">Ghi chú giảng viên<textarea rows="3" class="mt-2 w-full rounded-xl border border-slate-200 p-3 text-sm font-normal outline-none focus:border-blue-400" placeholder="Nhập ghi chú trong phiên làm việc..."></textarea></label></template>
          </div>
          <div class="flex flex-wrap justify-end gap-2 border-t border-slate-100 p-4"><button type="button" class="rounded-xl border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600" @click="messageStudent(selected)">Nhắn tin</button><button type="button" class="rounded-xl border border-blue-200 bg-blue-50 px-3 py-2 text-xs font-semibold text-blue-700" @click="assignPractice(selected)">Giao bài luyện</button><button type="button" class="rounded-xl bg-blue-600 px-3 py-2 text-xs font-semibold text-white" @click="adjustDifficulty(selected)">Điều chỉnh độ khó</button></div>
        </template>
        <div v-else class="grid gap-4 p-5 sm:grid-cols-2 sm:p-6"><div v-for="column in config?.columns || []" :key="column[0]" class="rounded-xl bg-slate-50 p-3"><p class="text-[10px] font-semibold uppercase text-slate-400">{{ column[1] }}</p><p class="mt-1 break-words text-sm text-slate-700">{{ selected[column[0]] ?? '—' }}</p></div></div>
      </section>
    </div>
  </section>
</template>
