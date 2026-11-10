<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import { studentProfile } from '../../data/studentMockData'
import { fetchStudentDashboard } from '../../services/studentService'

const router = useRouter()
const dashboard = ref(null)
const loading = ref(true)
const errorMessage = ref('')

async function loadDashboard() {
  loading.value = true
  errorMessage.value = ''
  try {
    dashboard.value = await fetchStudentDashboard()
  } catch (error) {
    console.error('Không thể tải dữ liệu dashboard học sinh.', error)
    errorMessage.value = 'Chưa tải được thông tin học tập. Con thử lại nhé!'
  } finally {
    loading.value = false
  }
}

function openTopic(topicId) {
  router.push({ name: 'StudentTopicDetail', params: { topicSlug: topicId } })
}

onMounted(loadDashboard)
</script>

<template>
  <section class="mx-auto max-w-[1500px] space-y-6 p-4 sm:p-6 xl:p-8">
    <div v-if="loading" class="space-y-5" role="status" aria-live="polite">
      <span class="sr-only">Đang tải bảng tổng quan học tập...</span>
      <div class="h-52 animate-pulse rounded-[28px] bg-amber-100/70"></div>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <div v-for="item in 4" :key="item" class="h-32 animate-pulse rounded-2xl bg-white shadow-sm"></div>
      </div>
      <div class="h-64 animate-pulse rounded-2xl bg-white shadow-sm"></div>
    </div>

    <div v-else-if="errorMessage" class="rounded-3xl border border-rose-100 bg-white p-8 text-center shadow-sm" role="alert">
      <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-rose-50 text-rose-600"><AdminIcon name="close" :size="25" /></span>
      <h2 class="mt-4 text-xl font-extrabold text-kids-text">Ôi, có chút trục trặc rồi!</h2>
      <p class="mt-2 text-sm text-slate-500">{{ errorMessage }}</p>
      <button type="button" class="mt-5 rounded-xl bg-kids-cta px-5 py-2.5 text-sm font-bold text-white transition hover:bg-orange-600" @click="loadDashboard">Thử tải lại</button>
    </div>

    <template v-else-if="dashboard">
      <section class="relative isolate overflow-hidden rounded-[28px] bg-gradient-to-br from-amber-100 via-amber-50 to-sky-50 px-5 py-7 sm:px-8 sm:py-9 lg:px-10" aria-labelledby="student-greeting">
        <div class="pointer-events-none absolute -right-10 -top-20 -z-10 h-64 w-64 rounded-full bg-white/50"></div>
        <div class="pointer-events-none absolute bottom-[-110px] right-40 -z-10 h-56 w-56 rounded-full bg-sky-100/60"></div>
        <div class="grid items-center gap-5 md:grid-cols-[minmax(0,1fr)_230px] lg:grid-cols-[minmax(0,1fr)_280px]">
          <div class="max-w-2xl">
            <p class="inline-flex items-center gap-2 rounded-full bg-white/80 px-3 py-1.5 text-xs font-bold text-amber-800 shadow-sm">
              <AdminIcon name="sparkles" :size="15" /> {{ studentProfile.grade }} · Sẵn sàng khám phá
            </p>
            <h2 id="student-greeting" class="mt-4 text-2xl font-extrabold leading-tight text-kids-text sm:text-3xl lg:text-4xl">Xin chào, {{ studentProfile.name.split(' ').slice(-1)[0] }}! <span aria-hidden="true">👋</span></h2>
            <p class="mt-3 max-w-xl text-sm leading-6 text-slate-600 sm:text-base">Hôm nay chúng ta cùng học thêm những từ mới nhé! Mỗi ngày một chút, con sẽ nói thật tự tin.</p>
            <RouterLink :to="{ name: 'StudentPronunciation' }" class="mt-5 inline-flex items-center gap-2 rounded-xl bg-kids-cta px-5 py-3 text-sm font-extrabold text-white shadow-md shadow-orange-200 transition hover:-translate-y-0.5 hover:bg-orange-600">
              <AdminIcon name="play" :size="17" /> Bắt đầu học
            </RouterLink>
          </div>

          <div class="relative mx-auto hidden h-44 w-52 items-center justify-center md:flex lg:h-52 lg:w-60" aria-label="Bạn Spark cổ vũ con học tập">
            <span class="absolute right-5 top-2 text-3xl text-kids-primary" aria-hidden="true">✦</span>
            <span class="absolute left-5 top-10 text-xl text-sky-400" aria-hidden="true">✦</span>
            <span class="absolute bottom-1 right-7 text-xl text-kids-cta" aria-hidden="true">✦</span>
            <svg viewBox="0 0 220 190" class="h-full w-full drop-shadow-lg" role="img" aria-label="Mascot Spark đang vẫy tay">
              <ellipse cx="108" cy="170" rx="66" ry="12" fill="#263238" opacity=".1" />
              <path d="M56 77c-16-17-35-9-33 10 2 15 16 24 33 21m108-31c16-17 35-9 33 10-2 15-16 24-33 21" fill="#4fc3f7" stroke="#263238" stroke-width="5" stroke-linecap="round" />
              <path d="M65 45 52 21l31 12m72 12 13-24-31 12" fill="#ffc107" stroke="#263238" stroke-width="5" stroke-linejoin="round" />
              <path d="M50 90c0-38 26-65 61-65s61 27 61 65-27 70-61 70-61-32-61-70Z" fill="#ffc107" stroke="#263238" stroke-width="5" />
              <circle cx="87" cy="87" r="7" fill="#263238" /><circle cx="135" cy="87" r="7" fill="#263238" />
              <circle cx="89" cy="84" r="2.5" fill="#fff" /><circle cx="137" cy="84" r="2.5" fill="#fff" />
              <ellipse cx="69" cy="106" rx="10" ry="6" fill="#ff7043" opacity=".55" /><ellipse cx="154" cy="106" rx="10" ry="6" fill="#ff7043" opacity=".55" />
              <path d="M91 111c9 12 23 12 32 0" fill="none" stroke="#263238" stroke-width="5" stroke-linecap="round" />
              <path d="m88 152-8 17m53-17 8 17" stroke="#263238" stroke-width="6" stroke-linecap="round" />
              <path d="m109 8 4 10 11 2-8 7 2 11-9-6-10 6 3-11-8-7 11-2z" fill="#fff" stroke="#263238" stroke-width="3" stroke-linejoin="round" />
            </svg>
          </div>
        </div>
      </section>

      <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4" aria-label="Thống kê học tập">
        <article v-for="stat in dashboard.stats" :key="stat.label" class="rounded-2xl border border-amber-100/80 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">
          <div class="flex items-start justify-between gap-3">
            <div><p class="text-xs font-semibold text-slate-500 sm:text-sm">{{ stat.label }}</p><p class="mt-3 text-3xl font-extrabold tracking-tight text-kids-text">{{ stat.value }}<span v-if="stat.suffix" class="ml-1 text-sm font-bold text-slate-400">{{ stat.suffix }}</span></p></div>
            <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl" :class="stat.iconClass"><AdminIcon :name="stat.icon" :size="21" /></span>
          </div>
          <p class="mt-3 text-xs text-slate-400">{{ stat.note }}</p>
        </article>
      </section>

      <section class="grid gap-5 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)]">
        <article class="overflow-hidden rounded-2xl border border-amber-100 bg-white shadow-sm">
          <div class="flex flex-wrap items-start justify-between gap-3 px-5 pt-5 sm:px-6 sm:pt-6">
            <div><p class="text-xs font-bold uppercase tracking-wider text-kids-cta">Học tiếp nào!</p><h3 class="mt-1 text-lg font-extrabold text-kids-text">Con đang học dở</h3></div>
            <span class="rounded-full bg-amber-50 px-3 py-1.5 text-xs font-bold text-amber-800">{{ dashboard.continueLearning.completed }}/{{ dashboard.continueLearning.total }} bài</span>
          </div>
          <div v-if="dashboard.continueLearning" class="grid gap-4 p-5 sm:grid-cols-[minmax(140px,0.75fr)_minmax(0,1.25fr)] sm:px-6 sm:pb-6">
            <img :src="dashboard.continueLearning.image" :alt="dashboard.continueLearning.title" class="h-40 w-full rounded-2xl object-cover sm:h-full sm:min-h-[180px]" />
            <div class="flex flex-col justify-center">
              <h4 class="text-xl font-extrabold text-kids-text">{{ dashboard.continueLearning.title }}</h4>
              <p class="mt-2 text-sm leading-6 text-slate-500">{{ dashboard.continueLearning.description }}</p>
              <div class="mt-5 flex items-center justify-between text-xs font-semibold text-slate-500">
                <span>Tiến độ của con</span><span>{{ dashboard.continueLearning.progress }}%</span>
              </div>
              <div class="mt-2 h-2.5 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="dashboard.continueLearning.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${dashboard.continueLearning.title}`">
                <div class="h-full rounded-full bg-gradient-to-r from-kids-primary to-kids-cta transition-all" :style="{ width: `${dashboard.continueLearning.progress}%` }"></div>
              </div>
              <button type="button" class="mt-5 inline-flex w-fit items-center gap-2 rounded-xl bg-kids-primary px-4 py-2.5 text-sm font-extrabold text-kids-text transition hover:bg-amber-400" @click="openTopic(dashboard.continueLearning.topicId)">
                Tiếp tục học <AdminIcon name="arrow" :size="16" />
              </button>
            </div>
          </div>
          <div v-else class="p-8 text-center text-sm text-slate-500">Chưa có bài học đang học. Con chọn một chủ đề để bắt đầu nhé!</div>
        </article>

        <article class="rounded-2xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6">
          <div class="flex items-start justify-between gap-3">
            <div><p class="text-xs font-bold uppercase tracking-wider text-sky-600">Cố lên nhé!</p><h3 class="mt-1 text-lg font-extrabold text-kids-text">Mục tiêu tuần này</h3></div>
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-sky-600"><AdminIcon name="target" :size="20" /></span>
          </div>
          <div class="mt-5 flex items-center gap-4">
            <div class="relative flex h-24 w-24 shrink-0 items-center justify-center rounded-full" :style="{ background: 'conic-gradient(#4fc3f7 0% 70%, #eaf6fb 70% 100%)' }">
              <div class="flex h-[72px] w-[72px] flex-col items-center justify-center rounded-full bg-white"><span class="text-xl font-extrabold text-kids-text">7/10</span><span class="text-[9px] text-slate-400">bài học</span></div>
            </div>
            <div><p class="text-sm font-bold text-kids-text">Con sắp đạt mục tiêu rồi!</p><p class="mt-1 text-xs leading-5 text-slate-500">Học thêm 3 bài nữa để nhận huy hiệu tuần này.</p><div class="mt-3 flex items-center gap-1 text-kids-primary"><AdminIcon v-for="item in 3" :key="item" name="star" :size="16" /></div></div>
          </div>
        </article>
      </section>

      <section aria-labelledby="student-topics-title">
        <div class="mb-4 flex flex-wrap items-end justify-between gap-3">
          <div><p class="text-xs font-bold uppercase tracking-wider text-emerald-600">Cùng khám phá</p><h3 id="student-topics-title" class="mt-1 text-xl font-extrabold text-kids-text">Chủ đề học tập nổi bật</h3></div>
          <RouterLink :to="{ name: 'StudentTopics' }" class="text-sm font-bold text-sky-700 transition hover:text-sky-900">Xem tất cả <span aria-hidden="true">→</span></RouterLink>
        </div>
        <div v-if="dashboard.topics.length" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="topic in dashboard.topics" :key="topic.id" class="overflow-hidden rounded-2xl border border-amber-100 bg-white shadow-sm transition duration-200 hover:-translate-y-1 hover:shadow-md">
            <div class="relative h-36 overflow-hidden bg-kids-bg">
              <img :src="topic.image" :alt="topic.title" class="h-full w-full object-cover transition duration-300 hover:scale-105" loading="lazy" />
              <span class="absolute left-3 top-3 rounded-full bg-white/95 px-2.5 py-1 text-[11px] font-bold text-slate-600 shadow-sm">{{ topic.level }}</span>
            </div>
            <div class="p-4">
              <div class="flex items-start justify-between gap-2"><h4 class="font-extrabold text-kids-text">{{ topic.title }}</h4><span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg" :class="topic.color"><AdminIcon :name="topic.icon" :size="16" /></span></div>
              <p class="mt-2 text-xs text-slate-500">{{ topic.words }} từ vựng <span aria-hidden="true">·</span> {{ topic.progress ? `Đã học ${topic.progress}%` : 'Chưa bắt đầu' }}</p>
              <div class="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="topic.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${topic.title}`">
                <div class="h-full rounded-full bg-kids-secondary" :style="{ width: `${topic.progress}%` }"></div>
              </div>
              <button type="button" class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl border border-amber-200 py-2.5 text-xs font-bold text-kids-text transition hover:border-kids-primary hover:bg-amber-50" @click="openTopic(topic.id)">
                Xem chi tiết <AdminIcon name="arrow" :size="14" />
              </button>
            </div>
          </article>
        </div>
        <div v-else class="rounded-2xl border border-dashed border-amber-200 bg-white p-8 text-center text-sm text-slate-500">Chưa có chủ đề học tập. Con quay lại sau nhé!</div>
      </section>

      <section class="grid gap-5 xl:grid-cols-[minmax(0,1.15fr)_minmax(300px,0.85fr)]">
        <article class="overflow-hidden rounded-2xl border border-amber-100 bg-white shadow-sm">
          <div class="flex items-center justify-between gap-3 border-b border-slate-100 px-5 py-4 sm:px-6">
            <div><h3 class="font-extrabold text-kids-text">Hoạt động gần đây</h3><p class="mt-1 text-xs text-slate-400">Những từ con vừa luyện tập</p></div>
            <RouterLink :to="{ name: 'StudentResults' }" class="text-xs font-bold text-sky-700 hover:text-sky-900">Xem kết quả</RouterLink>
          </div>
          <div v-if="dashboard.activities.length" class="divide-y divide-slate-100">
            <div v-for="activity in dashboard.activities" :key="activity.id" class="flex flex-wrap items-center justify-between gap-3 px-5 py-4 sm:px-6">
              <div class="flex min-w-0 items-center gap-3">
                <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-50 text-sky-700"><AdminIcon name="microphone" :size="18" /></span>
                <div class="min-w-0"><p class="font-bold text-kids-text">{{ activity.title }}</p><p class="mt-1 truncate text-xs text-slate-400">{{ activity.topic }} · {{ activity.time }}</p></div>
              </div>
              <div class="flex items-center gap-3"><span class="text-sm font-extrabold text-emerald-700">{{ activity.score }} điểm</span><span class="rounded-full bg-emerald-50 px-2.5 py-1 text-[10px] font-bold text-emerald-700">{{ activity.status }}</span></div>
            </div>
          </div>
          <div v-else class="p-8 text-center text-sm text-slate-500">Con chưa có hoạt động nào. Cùng luyện một từ nhé!</div>
        </article>

        <article class="rounded-2xl border border-amber-100 bg-white p-5 shadow-sm sm:p-6">
          <div class="flex items-center justify-between gap-3"><div><h3 class="font-extrabold text-kids-text">Huy hiệu của con</h3><p class="mt-1 text-xs text-slate-400">Mỗi nỗ lực đều đáng khen!</p></div><AdminIcon name="trophy" :size="21" class="text-amber-500" /></div>
          <div v-if="dashboard.achievements.length" class="mt-4 grid grid-cols-2 gap-3">
            <div v-for="achievement in dashboard.achievements" :key="achievement.id" class="flex items-center gap-2.5 rounded-xl bg-kids-bg p-3">
              <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl" :class="achievement.color"><AdminIcon :name="achievement.icon" :size="18" /></span>
              <div class="min-w-0"><p class="truncate text-xs font-extrabold text-kids-text">{{ achievement.title }}</p><p class="mt-1 line-clamp-2 text-[10px] leading-4 text-slate-500">{{ achievement.detail }}</p></div>
            </div>
          </div>
          <div v-else class="mt-4 rounded-xl bg-kids-bg p-5 text-center text-sm text-slate-500">Huy hiệu đầu tiên đang chờ con chinh phục!</div>
          <RouterLink :to="{ name: 'StudentAchievements' }" class="mt-4 block text-center text-xs font-bold text-sky-700 hover:text-sky-900">Xem bộ sưu tập huy hiệu →</RouterLink>
        </article>
      </section>

      <p class="pb-2 text-center text-[11px] text-slate-400">Dữ liệu minh họa · Chưa kết nối máy chủ</p>
    </template>
  </section>
</template>
