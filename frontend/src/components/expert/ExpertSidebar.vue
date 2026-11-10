<script setup>
import { useRouter } from 'vue-router'
import AdminIcon from '../admin/AdminIcon.vue'
import logo from '../../assets/logo_project.png'

defineProps({
  mobileOpen: { type: Boolean, default: false },
  collapsed: { type: Boolean, default: false },
})

const emit = defineEmits(['navigate', 'close', 'toggle-collapse'])
const router = useRouter()

const groups = [
  { title: 'Tổng quan', links: [{ name: 'ExpertDashboard', label: 'Dashboard', icon: 'dashboard' }] },
  {
    title: 'Nội dung học tập',
    links: [
      { name: 'ExpertTopics', label: 'Chủ đề', icon: 'lessons' },
      { name: 'ExpertVocabulary', label: 'Từ vựng', icon: 'book' },
      { name: 'ExpertPaths', label: 'Lộ trình học', icon: 'route' },
    ],
  },
  {
    title: 'Học viên',
    links: [
      { name: 'ExpertProgress', label: 'Tiến độ học tập', icon: 'chart' },
      { name: 'ExpertStudents', label: 'Theo dõi học viên', icon: 'users' },
    ],
  },
  {
    title: 'Tương tác & học liệu',
    links: [
      { name: 'ExpertResources', label: 'Kho học liệu', icon: 'library' },
      { name: 'ExpertMessages', label: 'Tin nhắn', icon: 'message' },
    ],
  },
  {
    title: 'Cá nhân',
    links: [
      { name: 'ExpertProfile', label: 'Hồ sơ cá nhân', icon: 'profile' },
      { name: 'ExpertSettings', label: 'Cài đặt', icon: 'settings' },
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
    class="fixed inset-y-0 left-0 z-40 flex w-[min(84vw,320px)] -translate-x-full flex-col border-r border-slate-200 bg-white transition-all duration-200 lg:static lg:z-auto lg:translate-x-0"
    :class="[mobileOpen && '!translate-x-0', collapsed ? 'lg:w-[84px]' : 'lg:w-[272px]']"
  >
    <div class="flex min-h-[76px] items-center gap-3 border-b border-slate-100 px-4">
      <img :src="logo" alt="KidSpeak" class="h-10 w-10 shrink-0 rounded-xl object-contain" />
      <div v-if="!collapsed" class="min-w-0">
        <p class="truncate text-sm font-extrabold text-slate-800">KidSpeak Expert</p>
        <p class="text-xs text-slate-500">Không gian giảng viên</p>
      </div>
      <button type="button" class="ml-auto rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden" aria-label="Đóng menu" @click="emit('close')"><AdminIcon name="close" /></button>
      <button v-if="!collapsed" type="button" class="ml-auto hidden rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:block" aria-label="Thu gọn menu" title="Thu gọn menu" @click="emit('toggle-collapse')"><AdminIcon name="collapse" /></button>
    </div>
    <button v-if="collapsed" type="button" class="hidden self-center rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:block" aria-label="Mở rộng menu" title="Mở rộng menu" @click="emit('toggle-collapse')"><AdminIcon name="expand" /></button>

    <nav class="flex-1 space-y-5 overflow-y-auto px-3 py-5" aria-label="Điều hướng giảng viên">
      <section v-for="group in groups" :key="group.title">
        <p v-if="!collapsed" class="px-3 pb-2 text-[10px] font-bold uppercase tracking-[0.12em] text-slate-400">{{ group.title }}</p>
        <div class="space-y-1">
          <RouterLink
            v-for="link in group.links"
            :key="link.name"
            :to="{ name: link.name }"
            class="group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
            active-class="!bg-blue-50 !text-blue-700 shadow-sm"
            :title="collapsed ? link.label : undefined"
            @click="emit('navigate')"
          >
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-500 transition group-hover:bg-white group-hover:text-blue-600 group-[.router-link-active]:bg-blue-100 group-[.router-link-active]:text-blue-700">
              <AdminIcon :name="link.icon" :size="18" />
            </span>
            <span v-if="!collapsed" class="min-w-0 flex-1 truncate">{{ link.label }}</span>
            <AdminIcon v-if="!collapsed && $route.name === link.name" name="arrow" :size="15" />
          </RouterLink>
        </div>
      </section>
    </nav>

    <div class="border-t border-slate-100 p-3">
      <div class="flex items-center gap-3 rounded-xl bg-slate-50 p-2.5" :class="{ 'justify-center': collapsed }">
        <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">TN</div>
        <div v-if="!collapsed" class="min-w-0 flex-1">
          <p class="truncate text-xs font-bold text-slate-800">Trần Thị Ngọc</p>
          <p class="truncate text-[11px] text-slate-500">Giảng viên</p>
        </div>
        <button v-if="!collapsed" type="button" class="rounded-lg p-2 text-slate-500 hover:bg-white hover:text-rose-600" title="Đăng xuất" aria-label="Đăng xuất" @click="logout"><AdminIcon name="logout" :size="17" /></button>
      </div>
    </div>
  </aside>
</template>
