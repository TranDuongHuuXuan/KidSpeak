<script setup>
import { useRouter } from 'vue-router'
import AdminIcon from './AdminIcon.vue'
import logo from '../../assets/logo_project.png'

defineProps({ mobileOpen: { type: Boolean, default: false } })
const emit = defineEmits(['navigate', 'close'])
const router = useRouter()

const links = [
  { name: 'AdminDashboard', label: 'Tổng quan', icon: 'dashboard' },
  { name: 'AdminUsers', label: 'Người dùng', icon: 'users' },
  { name: 'AdminRoles', label: 'Phân quyền', icon: 'roles' },
  { name: 'AdminVerification', label: 'Xác thực giáo viên', icon: 'verify' },
  { name: 'AdminLessons', label: 'Kiểm duyệt bài học', icon: 'lessons' },
  { name: 'AdminNotifications', label: 'Thông báo', icon: 'bell' },
  { name: 'AdminSettings', label: 'Cấu hình hệ thống', icon: 'settings' },
]

function logout() {
  emit('navigate')
  router.push({ name: 'Login' })
}
</script>

<template>
  <div v-if="mobileOpen" class="fixed inset-0 z-30 bg-slate-950/40 lg:hidden" @click="emit('close')"></div>
  <aside class="fixed inset-y-0 left-0 z-40 flex w-[min(84vw,320px)] -translate-x-full flex-col border-r border-slate-200 bg-white transition-transform duration-200 lg:static lg:z-auto lg:w-full lg:translate-x-0" :class="{ '!translate-x-0': mobileOpen }">
    <div class="flex items-center gap-3 border-b border-slate-100 px-5 py-5">
      <img :src="logo" alt="KidSpeak" class="h-11 w-11 rounded-xl object-contain" />
      <div class="min-w-0">
        <p class="truncate text-base font-extrabold text-slate-800">KidSpeak Admin</p>
        <p class="text-xs text-slate-500">Không gian quản trị</p>
      </div>
      <button type="button" class="ml-auto rounded-lg p-2 text-slate-500 hover:bg-slate-100 lg:hidden" aria-label="Đóng menu" @click="emit('close')"><AdminIcon name="close" /></button>
    </div>

    <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-5" aria-label="Điều hướng quản trị">
      <p class="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">Quản trị hệ thống</p>
      <RouterLink
        v-for="link in links"
        :key="link.name"
        :to="{ name: link.name }"
        class="group flex items-center gap-3 rounded-xl px-3 py-3 text-sm font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
        active-class="!bg-amber-50 !text-slate-900 shadow-sm"
        @click="emit('navigate')"
      >
        <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 text-slate-500 transition group-hover:bg-white group-hover:text-admin-cta"><AdminIcon :name="link.icon" :size="19" /></span>
        <span class="flex-1">{{ link.label }}</span>
        <AdminIcon v-if="$route.name === link.name" name="arrow" :size="16" />
      </RouterLink>
    </nav>

    <div class="border-t border-slate-100 p-4">
      <div class="flex items-center gap-3 rounded-xl bg-slate-50 p-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-full bg-amber-100 text-sm font-bold text-amber-800">AD</div>
        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-bold text-slate-800">Admin KidSpeak</p>
          <p class="truncate text-xs text-slate-500">admin@kidspeak.vn</p>
        </div>
        <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-white hover:text-red-600" title="Đăng xuất" aria-label="Đăng xuất" @click="logout"><AdminIcon name="logout" :size="18" /></button>
      </div>
    </div>
  </aside>
</template>
