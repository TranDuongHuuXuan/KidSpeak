<script setup>
import { computed } from 'vue'
import AdminBadge from '../../components/admin/AdminBadge.vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, formatDate } from '../../data/adminMockData'

const teacherCount = computed(() => adminData.users.filter((user) => user.role === 'Teacher').length)
const studentCount = computed(() => adminData.users.filter((user) => user.role === 'Student').length)
const pendingLessons = computed(() => adminData.lessons.filter((lesson) => lesson.status === 'Pending').length)
const pendingAccounts = computed(() => adminData.users.filter((user) => user.status === 'Pending').length)
const roleTotal = computed(() => adminData.users.length || 1)
const roleStats = computed(() => [
  { label: 'Học viên', count: studentCount.value, color: 'bg-blue-500' },
  { label: 'Giáo viên', count: teacherCount.value, color: 'bg-amber-500' },
  { label: 'Quản trị', count: 1, color: 'bg-violet-500' },
])
const activityItems = computed(() => [
  ...adminData.teacherRequests.slice(0, 2).map((request) => ({ id: `teacher-${request.id}`, title: `${request.name} gửi yêu cầu giáo viên`, date: request.sentAt, icon: 'users', status: request.status })),
  ...adminData.lessons.slice(0, 2).map((lesson) => ({ id: `lesson-${lesson.id}`, title: `Bài học “${lesson.title}” được gửi`, date: lesson.submittedAt, icon: 'lessons', status: lesson.status })),
].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 5))

const stats = computed(() => [
  { label: 'Tổng người dùng', value: adminData.users.length, icon: 'users', iconClass: 'bg-blue-50 text-blue-600', note: 'Tài khoản trên hệ thống' },
  { label: 'Giáo viên', value: teacherCount.value, icon: 'roles', iconClass: 'bg-violet-50 text-violet-600', note: 'Đã được cấp quyền' },
  { label: 'Học viên', value: studentCount.value, icon: 'dashboard', iconClass: 'bg-amber-50 text-amber-700', note: 'Đang tham gia học tập' },
  { label: 'Bài học', value: adminData.lessons.length, icon: 'lessons', iconClass: 'bg-cyan-50 text-cyan-700', note: 'Tổng nội dung bài học' },
  { label: 'Chờ duyệt', value: pendingLessons.value, icon: 'verify', iconClass: 'bg-orange-50 text-orange-600', note: 'Bài học cần kiểm duyệt' },
  { label: 'Chờ xác thực', value: pendingAccounts.value, icon: 'bell', iconClass: 'bg-rose-50 text-rose-600', note: 'Tài khoản cần xử lý' },
])
</script>

<template>
  <AdminPageShell title="Tổng quan" description="Chào mừng trở lại! Đây là tình hình hoạt động của KidSpeak hôm nay.">
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <article v-for="stat in stats" :key="stat.label" class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div class="flex items-start justify-between gap-3">
          <div><p class="text-sm font-medium text-slate-500">{{ stat.label }}</p><p class="mt-3 text-3xl font-extrabold text-slate-800">{{ stat.value }}</p></div>
          <span class="flex h-11 w-11 items-center justify-center rounded-xl" :class="stat.iconClass"><AdminIcon :name="stat.icon" /></span>
        </div>
        <p class="mt-3 text-xs text-slate-400">{{ stat.note }}</p>
      </article>
    </div>

    <div class="grid gap-5 xl:grid-cols-[minmax(0,1.4fr)_minmax(280px,0.8fr)]">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex flex-wrap items-start justify-between gap-3"><div><h3 class="font-bold text-slate-800">Tăng trưởng người dùng</h3><p class="mt-1 text-xs text-slate-400">Số lượt đăng ký trong 6 tháng gần đây</p></div><span class="rounded-lg bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-700">6 tháng</span></div>
        <div class="mt-6 overflow-hidden">
          <svg viewBox="0 0 640 230" role="img" aria-label="Biểu đồ tăng trưởng người dùng" class="h-56 w-full overflow-visible">
            <defs><linearGradient id="users-area" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#fbbf24" stop-opacity=".28" /><stop offset="100%" stop-color="#fbbf24" stop-opacity="0" /></linearGradient></defs>
            <g stroke="#e2e8f0" stroke-dasharray="4 5"><path d="M40 25H620M40 75H620M40 125H620M40 175H620" /></g>
            <path d="M40 170 C100 158 115 147 155 150 S225 120 270 128 S335 99 385 110 S450 66 500 78 S565 45 620 35 V190 H40Z" fill="url(#users-area)" />
            <path d="M40 170 C100 158 115 147 155 150 S225 120 270 128 S335 99 385 110 S450 66 500 78 S565 45 620 35" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round" />
            <g fill="#fff" stroke="#f59e0b" stroke-width="3"><circle cx="40" cy="170" r="4" /><circle cx="155" cy="150" r="4" /><circle cx="270" cy="128" r="4" /><circle cx="385" cy="110" r="4" /><circle cx="500" cy="78" r="4" /><circle cx="620" cy="35" r="4" /></g>
            <g fill="#94a3b8" font-size="11"><text x="34" y="215">Tháng 6</text><text x="147" y="215">Tháng 7</text><text x="262" y="215">Tháng 8</text><text x="376" y="215">Tháng 9</text><text x="487" y="215">Tháng 10</text><text x="592" y="215">Tháng 11</text></g>
          </svg>
        </div>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <h3 class="font-bold text-slate-800">Phân bố người dùng</h3><p class="mt-1 text-xs text-slate-400">Theo vai trò tài khoản</p>
        <div class="mt-6 flex items-center gap-6">
          <div class="relative h-36 w-36 shrink-0 rounded-full" :style="{ background: `conic-gradient(#3b82f6 0% ${studentCount / roleTotal * 100}%, #f59e0b ${studentCount / roleTotal * 100}% ${(studentCount + teacherCount) / roleTotal * 100}%, #8b5cf6 ${(studentCount + teacherCount) / roleTotal * 100}% 100%)` }">
            <div class="absolute inset-5 flex flex-col items-center justify-center rounded-full bg-white"><span class="text-2xl font-extrabold text-slate-800">{{ adminData.users.length }}</span><span class="text-[10px] text-slate-400">tài khoản</span></div>
          </div>
          <div class="min-w-0 flex-1 space-y-3">
            <div v-for="role in roleStats" :key="role.label" class="flex items-center justify-between gap-2 text-sm"><span class="flex items-center gap-2 text-slate-500"><i class="h-2.5 w-2.5 rounded-full" :class="role.color"></i>{{ role.label }}</span><strong class="text-slate-700">{{ role.count }}</strong></div>
          </div>
        </div>
      </article>
    </div>

    <div class="grid gap-5 xl:grid-cols-2">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex items-center justify-between gap-3"><div><h3 class="font-bold text-slate-800">Bài học được tạo và duyệt</h3><p class="mt-1 text-xs text-slate-400">Tình trạng kiểm duyệt nội dung</p></div><span class="text-xs text-slate-500">{{ adminData.lessons.length }} bài học</span></div>
        <div class="mt-6 space-y-4">
          <div v-for="lesson in adminData.lessons.slice(0, 4)" :key="lesson.id" class="grid grid-cols-[minmax(95px,1fr)_2fr_auto] items-center gap-3 text-xs">
            <span class="truncate text-slate-500">{{ lesson.title }}</span>
            <div class="h-2 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full" :class="lesson.status === 'Approved' ? 'bg-emerald-500' : lesson.status === 'Pending' ? 'bg-amber-400' : 'bg-rose-400'" :style="{ width: lesson.status === 'Approved' ? '100%' : lesson.status === 'Pending' ? '58%' : '34%' }"></div></div>
            <AdminBadge :status="lesson.status" />
          </div>
        </div>
      </article>
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex items-center justify-between"><div><h3 class="font-bold text-slate-800">Hoạt động gần đây</h3><p class="mt-1 text-xs text-slate-400">Yêu cầu mới nhất trên hệ thống</p></div><AdminIcon name="bell" class="text-slate-400" /></div>
        <div class="mt-5 divide-y divide-slate-100">
          <div v-for="activity in activityItems" :key="activity.id" class="flex items-center gap-3 py-3 first:pt-0 last:pb-0">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 text-slate-500"><AdminIcon :name="activity.icon" :size="17" /></span>
            <div class="min-w-0 flex-1"><p class="truncate text-sm font-medium text-slate-700">{{ activity.title }}</p><p class="mt-1 text-xs text-slate-400">{{ formatDate(activity.date) }}</p></div><AdminBadge :status="activity.status" />
          </div>
          <p v-if="!activityItems.length" class="py-8 text-center text-sm text-slate-400">Chưa có hoạt động gần đây.</p>
        </div>
      </article>
    </div>
  </AdminPageShell>
</template>
