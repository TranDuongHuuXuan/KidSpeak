<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminIcon from '../admin/AdminIcon.vue'
import { studentMockDashboard, studentProfile } from '../../data/studentMockData'
import { studentAccountService } from '../../services/studentAccountService'

try {
  studentAccountService.getProfile()
} catch (error) {
  console.error('Không thể tải thông tin học sinh cho header.', error)
}

defineProps({ title: { type: String, required: true } })
const emit = defineEmits(['toggle-menu'])
const route = useRoute()
const router = useRouter()
const search = ref('')
const notificationsOpen = ref(false)
const accountOpen = ref(false)
const breadcrumb = computed(() => route.meta.title || 'Tổng quan')

function submitSearch() {
  const query = search.value.trim()
  if (!query) return
  router.push({ name: 'StudentTopics', query: { q: query } })
  search.value = ''
}
</script>

<template>
  <header class="sticky top-0 z-20 flex min-h-[76px] items-center justify-between gap-3 border-b border-amber-100 bg-white/95 px-4 backdrop-blur sm:px-6 lg:px-8">
    <div class="flex min-w-0 items-center gap-3">
      <button type="button" class="rounded-xl border border-amber-100 p-2 text-slate-600 lg:hidden" aria-label="Mở menu" @click="emit('toggle-menu')">
        <AdminIcon name="menu" />
      </button>
      <div class="min-w-0">
        <div class="hidden items-center gap-2 text-xs text-slate-400 sm:flex">
          <span>Học sinh</span><AdminIcon name="arrow" :size="13" /><span class="truncate text-slate-500">{{ breadcrumb }}</span>
        </div>
        <h1 class="truncate text-lg font-bold text-kids-text sm:mt-1 sm:text-xl">{{ title }}</h1>
      </div>
    </div>

    <form class="hidden w-full max-w-[300px] md:block" role="search" @submit.prevent="submitSearch">
      <label class="flex h-10 items-center gap-2 rounded-xl border border-amber-100 bg-kids-bg px-3 text-slate-400 transition focus-within:border-kids-secondary focus-within:bg-white">
        <AdminIcon name="search" :size="17" />
        <input v-model="search" class="min-w-0 flex-1 bg-transparent text-sm text-kids-text outline-none placeholder:text-slate-400" placeholder="Tìm chủ đề..." aria-label="Tìm chủ đề học tập" />
        <kbd class="rounded border border-amber-100 bg-white px-1.5 py-0.5 text-[10px]">↵</kbd>
      </label>
    </form>

    <div class="flex shrink-0 items-center gap-1.5 sm:gap-3">
      <div class="relative">
        <button type="button" class="relative rounded-xl p-2.5 text-slate-500 transition hover:bg-amber-50" aria-label="Thông báo" :aria-expanded="notificationsOpen" @click="notificationsOpen = !notificationsOpen; accountOpen = false">
          <AdminIcon name="bell" :size="19" />
          <span class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-kids-cta ring-2 ring-white"></span>
        </button>
        <div v-if="notificationsOpen" class="absolute right-0 top-full z-30 mt-3 w-[min(88vw,340px)] rounded-2xl border border-amber-100 bg-white p-4 shadow-xl">
          <div class="flex items-center justify-between">
            <p class="font-bold text-kids-text">Hoạt động mới</p>
            <span class="text-xs text-slate-400">{{ studentMockDashboard.activities.length }} cập nhật</span>
          </div>
          <div class="mt-3 space-y-3">
            <div v-for="activity in studentMockDashboard.activities.slice(0, 3)" :key="activity.id" class="flex gap-3 border-t border-slate-100 pt-3">
              <span class="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-kids-secondary"></span>
              <div><p class="text-xs font-semibold text-slate-700">{{ activity.title }}</p><p class="mt-1 text-[11px] text-slate-400">{{ activity.time }}</p></div>
            </div>
          </div>
        </div>
      </div>

      <div class="relative">
        <button type="button" class="flex items-center gap-2 rounded-xl p-1.5 transition hover:bg-amber-50" aria-label="Tài khoản học sinh" :aria-expanded="accountOpen" @click="accountOpen = !accountOpen; notificationsOpen = false">
          <span class="flex h-9 w-9 items-center justify-center overflow-hidden rounded-full bg-kids-secondary/25 text-xs font-extrabold text-sky-800">
            <img v-if="studentProfile.avatar" :src="studentProfile.avatar" :alt="`Ảnh đại diện ${studentProfile.name}`" class="h-full w-full object-cover" />
            <span v-else>{{ studentProfile.initials }}</span>
          </span>
          <span class="hidden text-left sm:block"><span class="block max-w-[132px] truncate text-xs font-bold text-kids-text">{{ studentProfile.name }}</span><span class="block text-[11px] text-slate-400">{{ studentProfile.role }}</span></span>
          <AdminIcon name="chevronDown" :size="15" class="hidden text-slate-400 sm:block" />
        </button>
        <div v-if="accountOpen" class="absolute right-0 top-full z-30 mt-2 w-48 rounded-2xl border border-amber-100 bg-white p-2 shadow-xl">
          <RouterLink :to="{ name: 'StudentProfile' }" class="flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold text-slate-600 hover:bg-amber-50" @click="accountOpen = false">
            <AdminIcon name="profile" :size="17" /> Hồ sơ cá nhân
          </RouterLink>
          <RouterLink :to="{ name: 'Login' }" class="flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold text-rose-600 hover:bg-rose-50" @click="accountOpen = false">
            <AdminIcon name="logout" :size="17" /> Đăng xuất
          </RouterLink>
        </div>
      </div>
    </div>
  </header>
</template>
