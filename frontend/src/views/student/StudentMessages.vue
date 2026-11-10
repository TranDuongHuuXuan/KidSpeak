<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { studentMessagingService } from '../../services/studentMessagingService'

const conversations = ref([])
const activeId = ref('')
const filter = ref('all')
const query = ref('')
const draft = ref('')
const messageList = ref(null)
const loading = ref(true)
const errorMessage = ref('')

const activeConversation = computed(() => conversations.value.find((item) => item.id === activeId.value) || null)
const filteredConversations = computed(() => {
  const search = query.value.trim().toLocaleLowerCase('vi')
  return conversations.value.filter((conversation) => {
    const matchesStatus = filter.value === 'all'
      || (filter.value === 'unread' ? conversation.unread > 0 : conversation.unread === 0)
    const latest = conversation.messages.at(-1)?.text || ''
    const matchesQuery = !search || `${conversation.name} ${latest} ${conversation.messages.map((message) => message.text).join(' ')}`
      .toLocaleLowerCase('vi')
      .includes(search)
    return matchesStatus && matchesQuery
  })
})

const groupedMessages = computed(() => {
  if (!activeConversation.value) return []
  const groups = []
  for (const message of activeConversation.value.messages) {
    const date = new Date(message.sentAt)
    const day = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    let group = groups.at(-1)
    if (!group || group.day !== day) {
      group = { day, label: formatDayLabel(date), messages: [] }
      groups.push(group)
    }
    group.messages.push(message)
  }
  return groups
})

const unreadTotal = computed(() => conversations.value.reduce((sum, item) => sum + item.unread, 0))

function formatDayLabel(date) {
  const today = new Date()
  const yesterday = new Date()
  yesterday.setDate(today.getDate() - 1)
  if (date.toDateString() === today.toDateString()) return 'Hôm nay'
  if (date.toDateString() === yesterday.toDateString()) return 'Hôm qua'
  return date.toLocaleDateString('vi-VN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

function formatTime(value) {
  return new Date(value).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

function formatPreviewTime(value) {
  const date = new Date(value)
  return date.toDateString() === new Date().toDateString()
    ? formatTime(value)
    : date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' })
}

function latestMessage(conversation) {
  return conversation.messages.at(-1)
}

function selectConversation(conversation) {
  activeId.value = conversation.id
  try {
    studentMessagingService.markRead(conversation.id)
    conversation.unread = 0
    conversation.messages.forEach((message) => {
      if (message.from === 'other') message.status = 'read'
    })
  } catch (error) {
    console.error('Không thể cập nhật trạng thái đã đọc.', error)
    errorMessage.value = error.message
  }
}

function toggleUnread(conversation, event) {
  event.stopPropagation()
  try {
    studentMessagingService.toggleUnread(conversation.id)
    conversation.unread = conversation.unread > 0 ? 0 : 1
  } catch (error) {
    console.error('Không thể đổi trạng thái hội thoại.', error)
    errorMessage.value = error.message
  }
}

function sendMessage() {
  const content = draft.value.trim()
  const active = activeConversation.value
  if (!content || !active) return
  try {
    const { conversation, message } = studentMessagingService.send(active.id, content)
    active.messages.push(message)
    active.unread = 0
    const index = conversations.value.findIndex((item) => item.id === conversation.id)
    if (index >= 0) conversations.value.splice(index, 1)
    conversations.value.unshift(active)
    draft.value = ''
  } catch (error) {
    console.error('Không thể gửi tin nhắn mô phỏng.', error)
    errorMessage.value = error.message
  }
}

function handleInputKeydown(event) {
  if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
    event.preventDefault()
    sendMessage()
  }
}

async function loadConversations() {
  loading.value = true
  errorMessage.value = ''
  try {
    conversations.value = studentMessagingService.list()
  } catch (error) {
    console.error('Không thể tải hộp thư học sinh.', error)
    errorMessage.value = error.message || 'Không thể tải danh sách hội thoại.'
  } finally {
    loading.value = false
  }
}

watch(() => activeConversation.value?.messages.length, async () => {
  await nextTick()
  if (messageList.value) messageList.value.scrollTop = messageList.value.scrollHeight
})

onMounted(loadConversations)
</script>

<template>
  <section class="h-full min-h-0 p-3 sm:p-5 lg:p-6">
    <div class="mx-auto flex h-full min-h-[420px] max-w-[1500px] flex-col overflow-hidden rounded-3xl border border-amber-100 bg-white shadow-sm">
      <header class="flex flex-wrap items-center justify-between gap-3 border-b border-amber-100 px-4 py-3 sm:px-5">
        <div>
          <h2 class="text-lg font-extrabold text-kids-text">Tin nhắn</h2>
          <p class="mt-0.5 text-[11px] text-slate-500">Trao đổi cùng thầy cô và bạn học · {{ unreadTotal }} tin chưa đọc</p>
        </div>
        <span class="rounded-full bg-sky-50 px-3 py-1.5 text-[10px] font-bold text-sky-800">Hộp thư mô phỏng</span>
      </header>
      <p v-if="errorMessage" class="mx-4 mt-3 rounded-xl bg-rose-50 px-3 py-2 text-xs text-rose-700" role="alert">{{ errorMessage }}</p>

      <div class="grid min-h-0 flex-1 grid-rows-[minmax(0,1fr)] lg:grid-cols-[320px_minmax(0,1fr)]">
        <aside class="min-h-0 flex-col border-b border-amber-100 lg:border-b-0 lg:border-r" :class="activeId ? 'hidden lg:flex' : 'flex'">
          <div class="space-y-3 p-3 sm:p-4">
            <label class="flex h-10 items-center gap-2 rounded-xl border border-slate-200 px-3 text-slate-400 focus-within:border-sky-400">
              <AdminIcon name="search" :size="16" />
              <input v-model="query" class="min-w-0 flex-1 text-xs text-kids-text outline-none" placeholder="Tên hoặc nội dung tin nhắn" aria-label="Tìm hội thoại theo tên hoặc nội dung" />
            </label>
            <div class="grid grid-cols-3 gap-1 rounded-xl bg-slate-100 p-1" role="group" aria-label="Lọc hội thoại">
              <button v-for="option in [{ id: 'all', label: 'Tất cả' }, { id: 'unread', label: 'Chưa đọc' }, { id: 'read', label: 'Đã đọc' }]" :key="option.id" type="button" class="rounded-lg px-2 py-2 text-[10px] font-bold transition" :class="filter === option.id ? 'bg-white text-kids-text shadow-sm' : 'text-slate-500 hover:text-slate-700'" :aria-pressed="filter === option.id" @click="filter = option.id">{{ option.label }}</button>
            </div>
          </div>
          <div class="min-h-0 flex-1 divide-y divide-slate-100 overflow-y-auto">
            <div v-if="loading" class="space-y-2 p-4" role="status"><div v-for="item in 3" :key="item" class="h-16 animate-pulse rounded-xl bg-slate-100"></div><span class="sr-only">Đang tải hội thoại</span></div>
            <div v-for="conversation in filteredConversations" :key="conversation.id" class="flex items-center gap-1 border-b border-slate-100 px-2">
              <button type="button" class="flex min-w-0 flex-1 items-center gap-3 py-3 pl-1 text-left transition hover:bg-amber-50/60" :class="activeId === conversation.id ? 'bg-amber-50' : ''" :aria-current="activeId === conversation.id ? 'true' : undefined" @click="selectConversation(conversation)">
                <span class="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-full text-xs font-extrabold" :class="conversation.color">
                  {{ conversation.initials }}
                  <i class="absolute bottom-0 right-0 h-3 w-3 rounded-full border-2 border-white" :class="conversation.online ? 'bg-emerald-500' : 'bg-slate-300'" :aria-label="conversation.online ? 'Đang hoạt động' : 'Ngoại tuyến'"></i>
                </span>
                <span class="min-w-0 flex-1">
                  <span class="flex items-center justify-between gap-2"><strong class="truncate text-xs text-kids-text">{{ conversation.name }}</strong><small class="shrink-0 text-[9px] text-slate-400">{{ latestMessage(conversation) ? formatPreviewTime(latestMessage(conversation).sentAt) : '' }}</small></span>
                  <span class="mt-0.5 flex items-center justify-between gap-2"><span class="truncate text-[10px]" :class="conversation.unread ? 'font-bold text-slate-700' : 'text-slate-500'">{{ latestMessage(conversation)?.text || 'Chưa có tin nhắn' }}</span><span v-if="conversation.unread" class="flex h-5 min-w-5 items-center justify-center rounded-full bg-kids-cta px-1 text-[9px] font-extrabold text-white">{{ conversation.unread }}</span></span>
                  <span class="mt-0.5 block text-[9px] text-slate-400">{{ conversation.role }}</span>
                </span>
              </button>
              <button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-sky-700" :aria-label="conversation.unread ? `Đánh dấu đã đọc: ${conversation.name}` : `Đánh dấu chưa đọc: ${conversation.name}`" :title="conversation.unread ? 'Đánh dấu đã đọc' : 'Đánh dấu chưa đọc'" @click="toggleUnread(conversation, $event)"><AdminIcon :name="conversation.unread ? 'circleCheck' : 'message'" :size="15" /></button>
            </div>
            <div v-if="!loading && !filteredConversations.length" class="px-5 py-10 text-center">
              <span class="mx-auto flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-100 text-slate-400"><AdminIcon name="message" /></span>
              <p class="mt-3 text-xs font-bold text-slate-600">{{ conversations.length ? 'Không tìm thấy hội thoại' : 'Chưa có cuộc hội thoại' }}</p>
              <p class="mt-1 text-[10px] text-slate-400">{{ conversations.length ? 'Thử từ khóa hoặc bộ lọc khác.' : 'Tin nhắn mới sẽ xuất hiện tại đây.' }}</p>
            </div>
          </div>
        </aside>

        <section v-if="activeConversation" class="flex min-h-0 min-w-0 flex-col" aria-label="Nội dung hội thoại">
          <header class="flex min-h-[68px] items-center gap-3 border-b border-slate-100 px-3 sm:px-5">
            <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden" aria-label="Quay lại danh sách hội thoại" @click="activeId = ''"><AdminIcon name="arrow" :size="18" class="rotate-180" /></button>
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-xs font-extrabold" :class="activeConversation.color">{{ activeConversation.initials }}</span>
            <div class="min-w-0"><h3 class="truncate text-sm font-extrabold text-kids-text">{{ activeConversation.name }}</h3><p class="text-[10px]" :class="activeConversation.online ? 'text-emerald-600' : 'text-slate-400'">{{ activeConversation.online ? 'Đang hoạt động' : 'Đang ngoại tuyến' }} · {{ activeConversation.role }}</p></div>
            <span class="ml-auto hidden rounded-full bg-sky-50 px-3 py-1.5 text-[10px] font-bold text-sky-800 sm:inline-flex">Tin nhắn mô phỏng</span>
          </header>
          <div ref="messageList" class="min-h-0 flex-1 space-y-4 overflow-y-auto bg-[#FFFDF8] px-3 py-4 sm:px-6 sm:py-5" aria-live="polite">
            <div v-for="group in groupedMessages" :key="group.day" class="space-y-3">
              <div class="sticky top-0 z-[1] flex justify-center"><span class="rounded-full bg-white/90 px-3 py-1 text-[9px] font-semibold text-slate-400 shadow-sm">{{ group.label }}</span></div>
              <div v-for="message in group.messages" :key="message.id" class="flex" :class="message.from === 'me' ? 'justify-end' : 'justify-start'">
                <div class="max-w-[86%] sm:max-w-[75%]">
                  <p class="mb-1 px-1 text-[9px] text-slate-400" :class="message.from === 'me' ? 'text-right' : ''">{{ message.from === 'me' ? 'Con' : activeConversation.name }}</p>
                  <p class="whitespace-pre-wrap break-words rounded-2xl px-3.5 py-2.5 text-xs leading-5 sm:text-sm" :class="message.from === 'me' ? 'rounded-br-md bg-sky-500 text-white' : 'rounded-bl-md border border-amber-100 bg-white text-slate-700 shadow-sm'">{{ message.text }}</p>
                  <p class="mt-1 flex items-center gap-1 px-1 text-[9px] text-slate-400" :class="message.from === 'me' ? 'justify-end' : ''">{{ formatTime(message.sentAt) }}<template v-if="message.from === 'me'"> · {{ message.status === 'read' ? 'Đã đọc' : message.status === 'delivered' ? 'Đã nhận' : 'Đã gửi' }}</template></p>
                </div>
              </div>
            </div>
          </div>
          <form class="border-t border-slate-100 bg-white p-3 sm:p-4" @submit.prevent="sendMessage">
            <div class="flex items-end gap-2">
              <textarea v-model="draft" rows="1" maxlength="2000" class="max-h-32 min-h-11 min-w-0 flex-1 resize-y rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-xs leading-5 text-kids-text outline-none transition focus:border-sky-400 focus:bg-white sm:text-sm" placeholder="Nhập tin nhắn... (Enter để gửi, Shift + Enter để xuống dòng)" aria-label="Nội dung tin nhắn" @keydown="handleInputKeydown"></textarea>
              <button type="submit" class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-kids-cta text-white transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="!draft.trim()" aria-label="Gửi tin nhắn"><AdminIcon name="send" :size="17" /></button>
            </div>
            <p class="mt-2 text-center text-[9px] text-slate-400">Tin nhắn lưu trên trình duyệt này · Chưa kết nối máy chủ hoặc nhắn tin thời gian thực</p>
          </form>
        </section>
        <div v-else class="hidden min-h-0 items-center justify-center bg-[#FFFDF8] text-center lg:flex">
          <div><AdminIcon name="message" :size="32" class="mx-auto text-slate-300" /><p class="mt-3 text-sm text-slate-500">Chọn hội thoại để bắt đầu trao đổi.</p></div>
        </div>
      </div>
    </div>
  </section>
</template>
