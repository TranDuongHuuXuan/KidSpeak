<script setup>
import { useRouter } from 'vue-router'
import AdminIcon from '../admin/AdminIcon.vue'
import logo from '../../assets/logo_project.png'
import { studentProfile } from '../../data/studentMockData'
import { studentAccountService } from '../../services/studentAccountService'

try {
  studentAccountService.getProfile()
} catch (error) {
  console.error('Không thể tải thông tin học sinh cho sidebar.', error)
}

defineProps({
  mobileOpen: { type: Boolean, default: false },
  collapsed: { type: Boolean, default: false },
})

const emit = defineEmits(['navigate', 'close', 'toggle-collapse'])
const router = useRouter()

const groups = [
  {
    title: 'Học tập',
    links: [
      { name: 'StudentDashboard', label: 'Tổng quan', icon: 'dashboard' },
      { name: 'StudentTopics', label: 'Chủ đề học tập', icon: 'book' },
      { name: 'StudentPronunciation', label: 'Luyện phát âm', icon: 'microphone' },
    ],
  },
  {
    title: 'Cá nhân',
    links: [
      { name: 'StudentResults', label: 'Kết quả học tập', icon: 'chart' },
      { name: 'StudentAchievements', label: 'Thành tích', icon: 'trophy' },
      { name: 'StudentMessages', label: 'Tin nhắn', icon: 'message' },
      { name: 'StudentProfile', label: 'Hồ sơ cá nhân', icon: 'profile' },
    ],
  },
]

function logout() {
  emit('navigate')
  router.push({ name: 'Login' })
}
</script>

<template>
  <div v-if="mobileOpen" class="fixed inset-0 z-30 bg-slate-950/40 lg:hidden" @click="emit('close')"></div>
  <aside
    class="fixed inset-y-0 left-0 z-40 flex w-[min(84vw,320px)] -translate-x-full flex-col border-r border-amber-100 bg-white transition-all duration-200 lg:static lg:z-auto lg:translate-x-0"
    :class="[mobileOpen && '!translate-x-0', collapsed ? 'lg:w-[84px]' : 'lg:w-[272px]']"
  >
    <div class="flex min-h-[76px] items-center gap-3 border-b border-amber-100 px-4">
      <img :src="logo" alt="KidSpeak" class="h-10 w-10 shrink-0 rounded-xl object-contain" />
      <div v-if="!collapsed" class="min-w-0">
        <p class="truncate text-sm font-extrabold text-kids-text">KidSpeak</p>
        <p class="text-xs font-medium text-slate-500">Không gian học sinh</p>
      </div>
      <button type="button" class="ml-auto rounded-lg p-2 text-slate-500 hover:bg-amber-50 lg:hidden" aria-label="Đóng menu" @click="emit('close')">
        <AdminIcon name="close" />
      </button>
      <button v-if="!collapsed" type="button" class="ml-auto hidden rounded-lg p-2 text-slate-500 hover:bg-amber-50 lg:block" aria-label="Thu gọn menu" title="Thu gọn menu" @click="emit('toggle-collapse')">
        <AdminIcon name="collapse" />
      </button>
    </div>

    <div v-if="collapsed" class="hidden self-center py-2 lg:block">
      <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-amber-50" aria-label="Mở rộng menu" title="Mở rộng menu" @click="emit('toggle-collapse')">
        <AdminIcon name="expand" />
      </button>
    </div>

    <nav class="flex-1 space-y-6 overflow-y-auto px-3 py-5" aria-label="Điều hướng học sinh">
      <section v-for="group in groups" :key="group.title">
        <p v-if="!collapsed" class="px-3 pb-2 text-[10px] font-extrabold uppercase tracking-[0.14em] text-slate-400">{{ group.title }}</p>
        <div class="space-y-1">
          <RouterLink
            v-for="link in group.links"
            :key="link.name"
            :to="{ name: link.name }"
            class="group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold text-slate-600 transition duration-200 hover:bg-amber-50 hover:text-kids-text"
            active-class="!bg-amber-100/70 !text-kids-text shadow-sm"
            :title="collapsed ? link.label : undefined"
            @click="emit('navigate')"
          >
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-50 text-slate-500 transition group-hover:bg-white group-hover:text-kids-cta group-[.router-link-active]:bg-kids-primary/30 group-[.router-link-active]:text-amber-800">
              <AdminIcon :name="link.icon" :size="18" />
            </span>
            <span v-if="!collapsed" class="min-w-0 flex-1 truncate">{{ link.label }}</span>
            <AdminIcon v-if="!collapsed && $route.name === link.name" name="arrow" :size="15" />
          </RouterLink>
        </div>
      </section>
    </nav>

    <div class="border-t border-amber-100 p-3">
      <div class="flex items-center gap-3 rounded-xl bg-kids-bg p-2.5" :class="{ 'justify-center': collapsed }">
        <span class="flex h-10 w-10 shrink-0 items-center justify-center overflow-hidden rounded-full bg-kids-secondary/25 text-xs font-extrabold text-sky-800">
          <img v-if="studentProfile.avatar" :src="studentProfile.avatar" :alt="`Ảnh đại diện ${studentProfile.name}`" class="h-full w-full object-cover" />
          <span v-else>{{ studentProfile.initials }}</span>
        </span>
        <div v-if="!collapsed" class="min-w-0 flex-1">
          <p class="truncate text-xs font-bold text-kids-text">{{ studentProfile.name }}</p>
          <p class="truncate text-[11px] text-slate-500">{{ studentProfile.role }}</p>
        </div>
        <button v-if="!collapsed" type="button" class="rounded-lg p-2 text-slate-500 transition hover:bg-white hover:text-rose-600" title="Đăng xuất" aria-label="Đăng xuất" @click="logout">
          <AdminIcon name="logout" :size="17" />
        </button>
      </div>
    </div>
  </aside>
</template>
