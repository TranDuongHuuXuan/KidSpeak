<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { expertData } from '../../data/expertMockData'

const router = useRouter()
const needsHelp = computed(() => expertData.students.filter((student) => student.status === 'Cần hỗ trợ'))
const stats = computed(() => [
  { label: 'Chủ đề quản lý', value: expertData.topics.length, note: 'Tất cả trạng thái', icon: 'lessons', iconClass: 'bg-violet-50 text-violet-600' },
  { label: 'Từ vựng', value: expertData.vocabulary.length, note: 'Trong các chủ đề của bạn', icon: 'book', iconClass: 'bg-sky-50 text-sky-600' },
  { label: 'Học viên phụ trách', value: expertData.students.length, note: 'Được phân công', icon: 'users', iconClass: 'bg-blue-50 text-blue-600' },
  { label: 'Đang học', value: expertData.students.filter((student) => student.progress > 0).length, note: 'Có hoạt động học tập', icon: 'chart', iconClass: 'bg-emerald-50 text-emerald-600' },
  { label: 'Cần hỗ trợ', value: needsHelp.value.length, note: 'Ưu tiên theo dõi', icon: 'bell', iconClass: 'bg-amber-50 text-amber-600' },
  { label: 'Lộ trình triển khai', value: expertData.paths.filter((path) => path.status === 'Đang triển khai').length, note: 'Đang áp dụng cho học viên', icon: 'route', iconClass: 'bg-rose-50 text-rose-600' },
])

const quickActions = [
  { label: 'Tạo chủ đề mới', description: 'Soạn nội dung học tập', icon: 'plus', route: 'ExpertTopics', query: { create: '1' } },
  { label: 'Thêm từ vựng', description: 'Bổ sung từ mới vào chủ đề', icon: 'book', route: 'ExpertVocabulary', query: { create: '1' } },
  { label: 'Xây dựng lộ trình', description: 'Sắp xếp các chủ đề học', icon: 'route', route: 'ExpertPaths', query: { create: '1' } },
  { label: 'Xem tiến độ học viên', description: 'Theo dõi kết quả gần đây', icon: 'chart', route: 'ExpertProgress' },
]

function openRoute(name, query) {
  router.push({ name, query })
}
</script>

<template>
  <section class="space-y-6 p-4 sm:p-7 lg:p-8">
    <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p class="text-sm font-semibold text-blue-600">Không gian giảng viên</p>
        <h2 class="mt-1 text-2xl font-extrabold tracking-tight text-slate-800 sm:text-3xl">Chào cô Ngọc 👋</h2>
        <p class="mt-2 text-sm leading-6 text-slate-500">Đây là tình hình học tập của các học viên bạn đang phụ trách.</p>
      </div>
      <div class="flex items-center gap-2 text-xs text-slate-500"><span class="h-2 w-2 rounded-full bg-emerald-500"></span>Dữ liệu minh họa · Chưa kết nối API</div>
    </div>

    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      <article v-for="stat in stats" :key="stat.label" class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div class="flex items-start justify-between gap-3">
          <div><p class="text-sm font-medium text-slate-500">{{ stat.label }}</p><p class="mt-3 text-3xl font-extrabold text-slate-800">{{ stat.value }}</p></div>
          <span class="flex h-11 w-11 items-center justify-center rounded-xl" :class="stat.iconClass"><AdminIcon :name="stat.icon" /></span>
        </div>
        <p class="mt-3 text-xs text-slate-400">{{ stat.note }}</p>
      </article>
    </div>

    <div class="grid gap-5 xl:grid-cols-[minmax(0,1.45fr)_minmax(280px,0.75fr)]">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div><h3 class="font-bold text-slate-800">Tiến độ học tập</h3><p class="mt-1 text-xs text-slate-400">Tỷ lệ hoàn thành trung bình theo tuần</p></div>
          <span class="rounded-lg bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700">6 tuần gần nhất</span>
        </div>
        <div class="mt-6 overflow-hidden">
          <svg viewBox="0 0 640 230" role="img" aria-label="Biểu đồ tiến độ học tập theo tuần" class="h-56 w-full overflow-visible">
            <defs><linearGradient id="expert-progress-area" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#2563eb" stop-opacity=".2" /><stop offset="100%" stop-color="#2563eb" stop-opacity="0" /></linearGradient></defs>
            <g stroke="#e2e8f0" stroke-dasharray="4 5"><path d="M40 25H620M40 75H620M40 125H620M40 175H620" /></g>
            <path d="M40 160 C85 149 105 145 155 139 S225 120 270 126 S335 91 385 105 S450 76 500 82 S565 42 620 38 V190 H40Z" fill="url(#expert-progress-area)" />
            <path d="M40 160 C85 149 105 145 155 139 S225 120 270 126 S335 91 385 105 S450 76 500 82 S565 42 620 38" fill="none" stroke="#2563eb" stroke-width="3" stroke-linecap="round" />
            <g fill="#fff" stroke="#2563eb" stroke-width="3"><circle cx="40" cy="160" r="4" /><circle cx="155" cy="139" r="4" /><circle cx="270" cy="126" r="4" /><circle cx="385" cy="105" r="4" /><circle cx="500" cy="82" r="4" /><circle cx="620" cy="38" r="4" /></g>
            <g fill="#94a3b8" font-size="11"><text x="34" y="215">Tuần 1</text><text x="147" y="215">Tuần 2</text><text x="262" y="215">Tuần 3</text><text x="376" y="215">Tuần 4</text><text x="487" y="215">Tuần 5</text><text x="592" y="215">Tuần 6</text></g>
          </svg>
        </div>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex items-start justify-between"><div><h3 class="font-bold text-slate-800">Kết quả luyện tập</h3><p class="mt-1 text-xs text-slate-400">Điểm trung bình học viên</p></div><AdminIcon name="chart" class="text-blue-600" /></div>
        <div class="mt-7 flex items-center justify-center">
          <div class="relative flex h-40 w-40 items-center justify-center rounded-full" :style="{ background: `conic-gradient(#2563eb 0% 78%, #e2e8f0 78% 100%)` }">
            <div class="flex h-32 w-32 flex-col items-center justify-center rounded-full bg-white"><span class="text-3xl font-extrabold text-slate-800">78%</span><span class="text-xs text-slate-400">điểm trung bình</span></div>
          </div>
        </div>
        <div class="mt-6 space-y-3">
          <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2 text-slate-500"><i class="h-2.5 w-2.5 rounded-full bg-blue-600"></i>Phát âm</span><strong class="text-slate-700">72 điểm</strong></div>
          <div class="flex items-center justify-between text-sm"><span class="flex items-center gap-2 text-slate-500"><i class="h-2.5 w-2.5 rounded-full bg-slate-200"></i>Từ vựng</span><strong class="text-slate-700">84 điểm</strong></div>
        </div>
      </article>
    </div>

    <div class="grid gap-5 xl:grid-cols-[minmax(0,1.2fr)_minmax(300px,0.8fr)]">
      <article class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 px-5 py-4 sm:px-6">
          <div><h3 class="font-bold text-slate-800">Học viên cần hỗ trợ</h3><p class="mt-1 text-xs text-slate-400">Theo dõi các trường hợp cần ưu tiên</p></div>
          <RouterLink :to="{ name: 'ExpertProgress', query: { status: 'Cần hỗ trợ' } }" class="text-xs font-semibold text-blue-600 hover:text-blue-700">Xem tất cả</RouterLink>
        </div>
        <div v-if="needsHelp.length" class="divide-y divide-slate-100">
          <div v-for="student in needsHelp" :key="student.id" class="flex flex-wrap items-center justify-between gap-3 px-5 py-4 sm:px-6">
            <div class="flex min-w-0 items-center gap-3"><span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-xs font-bold" :class="student.color">{{ student.initials }}</span><div class="min-w-0"><p class="truncate text-sm font-semibold text-slate-700">{{ student.name }}</p><p class="mt-0.5 truncate text-xs text-slate-400">{{ student.path }} · {{ student.lastActive }}</p></div></div>
            <div class="flex items-center gap-3"><span class="hidden text-right sm:block"><strong class="block text-sm text-slate-700">{{ student.progress }}%</strong><span class="text-[11px] text-slate-400">tiến độ</span></span><RouterLink :to="{ name: 'ExpertMessages', query: { student: student.id } }" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 hover:border-blue-200 hover:text-blue-700">Nhắn tin</RouterLink></div>
          </div>
        </div>
        <div v-else class="px-6 py-10 text-center text-sm text-slate-500">Chưa có học viên cần hỗ trợ.</div>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div><h3 class="font-bold text-slate-800">Thao tác nhanh</h3><p class="mt-1 text-xs text-slate-400">Bắt đầu công việc thường dùng</p></div>
        <div class="mt-4 grid gap-2">
          <button v-for="action in quickActions" :key="action.label" type="button" class="flex items-center gap-3 rounded-xl border border-slate-100 p-3 text-left transition hover:border-blue-200 hover:bg-blue-50/50" @click="openRoute(action.route, action.query)">
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600"><AdminIcon :name="action.icon" :size="18" /></span>
            <span class="min-w-0 flex-1"><strong class="block text-sm text-slate-700">{{ action.label }}</strong><small class="mt-0.5 block text-xs text-slate-400">{{ action.description }}</small></span>
            <AdminIcon name="arrow" :size="16" class="text-slate-400" />
          </button>
        </div>
      </article>
    </div>

    <div class="grid gap-5 xl:grid-cols-2">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex items-center justify-between gap-3"><div><h3 class="font-bold text-slate-800">Hoạt động gần đây</h3><p class="mt-1 text-xs text-slate-400">Cập nhật trong không gian giảng viên</p></div><AdminIcon name="clock" class="text-slate-400" /></div>
        <div class="mt-5 space-y-4">
          <div v-for="activity in expertData.activities" :key="activity.id" class="flex gap-3">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl" :class="activity.tone"><AdminIcon :name="activity.type === 'student' ? 'users' : activity.type === 'message' ? 'message' : activity.type === 'path' ? 'route' : 'lessons'" :size="17" /></span>
            <div class="min-w-0 flex-1"><p class="text-sm font-semibold text-slate-700">{{ activity.title }}</p><p class="mt-0.5 text-xs text-slate-400">{{ activity.detail }}</p></div><span class="shrink-0 text-[11px] text-slate-400">{{ activity.time }}</span>
          </div>
        </div>
      </article>
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="flex items-center justify-between gap-3"><div><h3 class="font-bold text-slate-800">Chủ đề mới cập nhật</h3><p class="mt-1 text-xs text-slate-400">Nội dung do bạn quản lý</p></div><RouterLink :to="{ name: 'ExpertTopics' }" class="text-xs font-semibold text-blue-600">Quản lý</RouterLink></div>
        <div class="mt-4 space-y-3">
          <div v-for="topic in expertData.topics.slice(0, 3)" :key="topic.id" class="flex items-center gap-3 rounded-xl bg-slate-50 p-3">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white text-blue-600"><AdminIcon name="lessons" :size="17" /></span>
            <div class="min-w-0 flex-1"><p class="truncate text-sm font-semibold text-slate-700">{{ topic.title }}</p><p class="mt-0.5 text-xs text-slate-400">{{ topic.words }} từ vựng · {{ topic.level }}</p></div>
            <span class="rounded-full bg-white px-2.5 py-1 text-[10px] font-semibold text-slate-500">{{ topic.status }}</span>
          </div>
        </div>
        <RouterLink :to="{ name: 'ExpertMessages' }" class="mt-4 flex items-center justify-between rounded-xl border border-blue-100 bg-blue-50/70 px-4 py-3 text-sm font-semibold text-blue-700 hover:bg-blue-50">
          <span class="flex items-center gap-2"><AdminIcon name="message" :size="17" />{{ expertData.conversations.reduce((total, item) => total + item.unread, 0) }} tin nhắn chưa đọc</span><AdminIcon name="arrow" :size="16" />
        </RouterLink>
      </article>
    </div>
  </section>
</template>
