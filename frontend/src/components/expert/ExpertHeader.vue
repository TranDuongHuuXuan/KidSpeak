<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminIcon from '../admin/AdminIcon.vue'
import { expertData } from '../../data/expertMockData'

defineProps({ title: { type: String, required: true } })
const emit = defineEmits(['toggle-menu'])
const route = useRoute()
const router = useRouter()
const search = ref('')
const notificationsOpen = ref(false)
const breadcrumb = computed(() => route.meta.title || 'Tổng quan')
const unreadCount = computed(() => expertData.conversations.reduce((total, item) => total + item.unread, 0))

function submitSearch() {
  const query = search.value.trim()
  if (!query) return
  router.push({ name: 'ExpertStudents', query: { q: query } })
  search.value = ''
}
</script>

<template>
  <header class="sticky top-0 z-20 flex min-h-[76px] items-center justify-between gap-3 border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-7 lg:px-8">
    <div class="flex min-w-0 items-center gap-3">
      <button type="button" class="rounded-xl border border-slate-200 p-2 text-slate-600 lg:hidden" aria-label="Mở menu" @click="emit('toggle-menu')"><AdminIcon name="menu" /></button>
      <div class="min-w-0">
        <div class="hidden items-center gap-2 text-xs text-slate-400 sm:flex"><span>Giảng viên</span><AdminIcon name="arrow" :size="13" /><span class="truncate text-slate-500">{{ breadcrumb }}</span></div>
        <h1 class="truncate text-lg font-bold text-slate-800 sm:mt-1 sm:text-xl">{{ title }}</h1>
      </div>
    </div>
    <form class="hidden w-full max-w-[320px] md:block" role="search" @submit.prevent="submitSearch">
      <label class="flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-slate-50 px-3 text-slate-400 focus-within:border-blue-400 focus-within:bg-white">
        <AdminIcon name="search" :size="17" />
        <input v-model="search" class="min-w-0 flex-1 bg-transparent text-sm text-slate-700 outline-none placeholder:text-slate-400" placeholder="Tìm học viên..." aria-label="Tìm học viên" />
        <kbd class="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px]">↵</kbd>
      </label>
    </form>
    <div class="flex shrink-0 items-center gap-2 sm:gap-3">
      <div class="relative">
        <button type="button" class="relative rounded-xl p-2.5 text-slate-500 transition hover:bg-slate-100" aria-label="Thông báo" :aria-expanded="notificationsOpen" @click="notificationsOpen = !notificationsOpen">
          <AdminIcon name="bell" :size="19" />
          <span v-if="unreadCount" class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white"></span>
        </button>
        <div v-if="notificationsOpen" class="absolute right-0 top-full z-30 mt-3 w-[min(88vw,340px)] rounded-2xl border border-slate-200 bg-white p-4 shadow-xl">
          <div class="flex items-center justify-between"><p class="font-bold text-slate-800">Thông báo</p><span class="text-xs text-slate-400">{{ unreadCount }} tin chưa đọc</span></div>
          <div class="mt-3 space-y-3">
            <div v-for="activity in expertData.activities.slice(0, 3)" :key="activity.id" class="flex gap-3 border-t border-slate-100 pt-3">
              <span class="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-blue-500"></span>
              <div><p class="text-xs font-semibold text-slate-700">{{ activity.title }}</p><p class="mt-1 text-[11px] text-slate-400">{{ activity.time }}</p></div>
            </div>
          </div>
          <RouterLink :to="{ name: 'ExpertMessages' }" class="mt-3 block text-center text-xs font-semibold text-blue-600" @click="notificationsOpen = false">Mở hộp thư</RouterLink>
        </div>
      </div>
      <div class="hidden text-right sm:block"><p class="text-sm font-semibold text-slate-700">Trần Thị Ngọc</p><p class="text-xs text-slate-400">Giảng viên</p></div>
      <div class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">TN</div>
      <RouterLink :to="{ name: 'Login' }" class="hidden rounded-xl p-2 text-slate-400 transition hover:bg-rose-50 hover:text-rose-600 sm:block" title="Đăng xuất" aria-label="Đăng xuất"><AdminIcon name="logout" :size="18" /></RouterLink>
    </div>
  </header>
</template>
