<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import StudentTopicCard from '../../components/student/StudentTopicCard.vue'
import { getNextUncompletedWord, getTopicProgress, startTopic, toggleTopicFlag } from '../../services/studentProgressService'
import { getStudentLearningPaths, getStudentTopics } from '../../services/studentTopicService'

const route = useRoute()
const router = useRouter()
const isPronunciationPage = computed(() => route.name === 'StudentPronunciation')
const topics = ref([])
const paths = ref([])
const loading = ref(true)
const errorMessage = ref('')
const search = ref('')
const level = ref('')
const status = ref('')
const favoritesOnly = ref(false)
const starredOnly = ref(false)
const sort = ref('recommended')
const page = ref(1)
const pageSize = ref(6)

const filteredTopics = computed(() => topics.value)
const pageCount = computed(() => Math.max(1, Math.ceil(filteredTopics.value.length / pageSize.value)))
const visibleTopics = computed(() => filteredTopics.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value))
const inProgressTopics = computed(() => topics.value.filter((topic) => topic.progress.status === 'in-progress'))

async function loadData() {
  loading.value = true
  errorMessage.value = ''
  try {
    const options = {
      query: search.value,
      level: level.value,
      status: status.value,
      favoritesOnly: favoritesOnly.value,
      starredOnly: starredOnly.value,
      sort: isPronunciationPage.value ? 'recent' : sort.value,
    }
    const [filtered, allTopics, learningPaths] = await Promise.all([
      getStudentTopics(options),
      getStudentTopics({ sort: isPronunciationPage.value ? 'recent' : 'recommended' }),
      isPronunciationPage.value ? Promise.resolve([]) : getStudentLearningPaths(),
    ])
    topics.value = filtered
    paths.value = learningPaths
    allPublishedTopics.value = allTopics
    page.value = Math.min(page.value, Math.max(1, Math.ceil(filtered.length / pageSize.value)))
  } catch (error) {
    console.error('Không thể tải chủ đề học tập.', error)
    errorMessage.value = 'Chưa tải được chủ đề. Con thử tải lại nhé!'
  } finally {
    loading.value = false
  }
}

const allPublishedTopics = ref([])
const activeTopics = computed(() => allPublishedTopics.value.filter((topic) => topic.progress.status === 'in-progress'))

function openTopic(topic) {
  try {
    const progress = getTopicProgress(topic.slug, topic.words.length)
    const nextWord = getNextUncompletedWord(topic, progress)
    startTopic(topic.slug, nextWord?.id, topic.words.length)
    router.push({ name: 'StudentTopicDetail', params: { topicSlug: topic.slug } })
  } catch (error) {
    console.error('Không thể lưu tiến độ chủ đề.', error)
    errorMessage.value = 'Chưa lưu được tiến độ. Con thử lại nhé!'
  }
}

function continueTopic(topic) {
  openTopic(topic)
}

async function toggleFlag(slug, flag) {
  try {
    toggleTopicFlag(slug, flag)
    await loadData()
  } catch (error) {
    console.error('Không thể cập nhật lựa chọn chủ đề.', error)
    errorMessage.value = 'Chưa cập nhật được lựa chọn. Con thử lại nhé!'
  }
}

function openPath(path) {
  const topic = allPublishedTopics.value.find((item) => item.slug === path.nextTopicSlug)
  if (topic) openTopic(topic)
}

watch([search, level, status, favoritesOnly, starredOnly, sort], () => {
  page.value = 1
  loadData()
})
watch(pageSize, () => { page.value = 1 })
watch(isPronunciationPage, (pronunciationMode) => {
  page.value = 1
  const nextSort = pronunciationMode ? 'recent' : 'recommended'
  if (sort.value === nextSort) loadData()
  else sort.value = nextSort
})
watch(() => route.query.q, (query) => {
  search.value = typeof query === 'string' ? query : ''
})

onMounted(() => {
  search.value = typeof route.query.q === 'string' ? route.query.q : ''
  loadData()
})
</script>

<template>
  <section class="mx-auto max-w-[1500px] space-y-8 p-4 sm:p-6 xl:p-8">
    <section class="relative isolate overflow-hidden rounded-[26px] bg-gradient-to-r from-amber-100 via-amber-50 to-sky-50 px-5 py-6 sm:px-8 sm:py-7" aria-labelledby="topics-page-title">
      <div class="pointer-events-none absolute -right-7 -top-14 -z-10 h-48 w-48 rounded-full bg-white/60"></div>
      <div class="grid items-center gap-4 md:grid-cols-[minmax(0,1fr)_170px]">
        <div>
          <p class="inline-flex items-center gap-2 rounded-full bg-white/80 px-3 py-1.5 text-xs font-bold text-amber-800"><AdminIcon :name="isPronunciationPage ? 'microphone' : 'sparkles'" :size="15" />{{ isPronunciationPage ? 'Góc luyện nói của con' : 'Góc khám phá của con' }}</p>
          <h2 id="topics-page-title" class="mt-3 text-2xl font-extrabold text-kids-text sm:text-3xl">{{ isPronunciationPage ? 'Chọn chủ đề luyện phát âm' : 'Khám phá chủ đề học tập' }}</h2>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600">{{ isPronunciationPage ? 'Chọn một chủ đề, rồi chọn từ con muốn luyện phát âm nhé!' : 'Cùng KidSpeak khám phá thế giới từ vựng và luyện phát âm mỗi ngày nhé!' }}</p>
        </div>
        <div class="hidden justify-center md:flex" aria-hidden="true"><span class="text-7xl">🧭</span></div>
      </div>
    </section>

    <div v-if="errorMessage" class="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-rose-100 bg-rose-50 p-4 text-sm text-rose-700" role="alert">
      <span>{{ errorMessage }}</span>
      <button type="button" class="font-bold underline" @click="loadData">Thử lại</button>
    </div>

    <section v-if="!isPronunciationPage" aria-labelledby="learning-paths-heading">
      <div class="mb-4"><p class="text-xs font-bold uppercase tracking-wider text-kids-cta">Bước nhỏ, tiến bộ lớn</p><h3 id="learning-paths-heading" class="mt-1 text-xl font-extrabold text-kids-text">🎯 Lộ trình học tập dành cho con</h3></div>
      <div v-if="loading" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div v-for="item in 3" :key="item" class="h-48 animate-pulse rounded-2xl bg-white shadow-sm"></div>
      </div>
      <div v-else-if="paths.length" class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <article v-for="path in paths" :key="path.id" class="rounded-2xl border border-amber-100 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
          <div class="flex items-start justify-between gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-700"><AdminIcon name="route" :size="19" /></span><span class="rounded-full bg-slate-50 px-2.5 py-1 text-[10px] font-bold text-slate-600">{{ path.level }}</span></div>
          <h4 class="mt-4 font-extrabold text-kids-text">{{ path.title }}</h4>
          <p class="mt-1 min-h-10 text-xs leading-5 text-slate-500">{{ path.description }}</p>
          <div class="mt-4 flex items-center justify-between text-xs text-slate-500"><span>{{ path.topicCount }} chủ đề</span><span>{{ path.completedTopics }}/{{ path.topicCount }} hoàn thành</span></div>
          <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="path.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${path.title}`"><div class="h-full rounded-full bg-kids-secondary" :style="{ width: `${path.progress}%` }"></div></div>
          <div class="mt-4 flex items-center justify-between gap-3"><span class="truncate text-[11px] text-slate-400">{{ path.status === 'completed' ? 'Đã hoàn thành' : `Tiếp theo: ${allPublishedTopics.find((topic) => topic.slug === path.nextTopicSlug)?.title || 'Chưa có chủ đề'}` }}</span><button type="button" class="shrink-0 rounded-xl bg-kids-primary px-3 py-2 text-xs font-extrabold text-kids-text transition hover:bg-amber-400 disabled:opacity-50" :disabled="!path.nextTopicSlug" @click="openPath(path)">{{ path.status === 'not-started' ? 'Bắt đầu' : path.status === 'completed' ? 'Ôn tập' : 'Tiếp tục' }}</button></div>
        </article>
      </div>
      <div v-else class="rounded-2xl border border-dashed border-amber-200 bg-white p-6 text-center text-sm text-slate-500">Lộ trình học tập đang được chuẩn bị. Con quay lại sau nhé!</div>
    </section>

    <section aria-labelledby="continue-learning-heading">
      <div class="mb-4 flex items-end justify-between gap-3"><div><p class="text-xs font-bold uppercase tracking-wider text-sky-700">Học tiếp nào</p><h3 id="continue-learning-heading" class="mt-1 text-xl font-extrabold text-kids-text">Chủ đề đang học dở</h3></div><span class="text-xs text-slate-400">{{ activeTopics.length }} chủ đề</span></div>
      <div v-if="loading" class="h-36 animate-pulse rounded-2xl bg-white shadow-sm"></div>
      <div v-else-if="activeTopics.length" class="grid gap-4 md:grid-cols-2">
        <article v-for="topic in activeTopics" :key="topic.slug" class="flex flex-col gap-4 rounded-2xl border border-sky-100 bg-white p-4 shadow-sm sm:flex-row sm:items-center">
          <img :src="topic.image" :alt="topic.imageAlt" class="h-36 w-full rounded-xl object-cover sm:h-28 sm:w-36" loading="lazy" />
          <div class="min-w-0 flex-1">
            <h4 class="font-extrabold text-kids-text">{{ topic.title }}</h4><p class="mt-1 line-clamp-2 text-xs leading-5 text-slate-500">{{ topic.description }}</p>
            <div class="mt-3 flex justify-between text-[11px] text-slate-500"><span>{{ topic.progress.completed }}/{{ topic.wordCount }} từ</span><span>{{ topic.progress.progress }}%</span></div>
            <div class="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-sky-400" :style="{ width: `${topic.progress.progress}%` }"></div></div>
            <p class="mt-2 text-[10px] text-slate-400">Học gần nhất: {{ topic.progress.lastStudiedAt ? new Date(topic.progress.lastStudiedAt).toLocaleString('vi-VN') : 'Vừa bắt đầu' }}</p>
            <button type="button" class="mt-3 rounded-xl bg-sky-100 px-4 py-2 text-xs font-extrabold text-sky-800 transition hover:bg-sky-200" @click="continueTopic(topic)">Tiếp tục học</button>
          </div>
        </article>
      </div>
      <div v-else-if="!loading" class="rounded-2xl border border-dashed border-sky-200 bg-white p-6 text-center">
        <p class="text-sm font-bold text-kids-text">Chưa có chủ đề học dở</p><p class="mt-1 text-xs text-slate-500">Con chọn một chủ đề bên dưới để bắt đầu hành trình nhé!</p>
      </div>
    </section>

    <section aria-labelledby="all-topics-heading">
      <div class="mb-4 flex flex-wrap items-end justify-between gap-3">
        <div><p class="text-xs font-bold uppercase tracking-wider text-emerald-700">{{ isPronunciationPage ? 'Chọn một chủ đề để bắt đầu' : 'Chọn điều con thích' }}</p><h3 id="all-topics-heading" class="mt-1 text-xl font-extrabold text-kids-text">{{ isPronunciationPage ? 'Chủ đề luyện phát âm' : 'Khám phá tất cả chủ đề' }}</h3></div>
        <span class="text-xs text-slate-500">{{ filteredTopics.length }} chủ đề</span>
      </div>
      <div class="grid gap-3 rounded-2xl border border-amber-100 bg-white p-4 shadow-sm sm:grid-cols-2 xl:grid-cols-[minmax(220px,1.5fr)_repeat(3,minmax(130px,1fr))]">
        <label class="flex min-h-11 items-center gap-2 rounded-xl border border-slate-200 px-3 text-slate-400 focus-within:border-sky-400">
          <AdminIcon name="search" :size="17" /><input v-model="search" class="min-w-0 flex-1 bg-transparent text-sm text-kids-text outline-none placeholder:text-slate-400" placeholder="Tìm tên hoặc mô tả..." aria-label="Tìm chủ đề học tập" />
          <button v-if="search" type="button" class="rounded p-1 text-slate-400 hover:text-rose-600" aria-label="Xóa tìm kiếm" @click="search = ''"><AdminIcon name="close" :size="15" /></button>
        </label>
        <label class="flex items-center gap-2 rounded-xl border border-slate-200 px-3"><span class="text-xs font-semibold text-slate-500">Cấp độ</span><select v-model="level" class="min-w-0 flex-1 bg-transparent py-2 text-xs font-semibold text-kids-text outline-none"><option value="">Tất cả</option><option value="Cơ bản">Cơ bản</option><option value="Khám phá">Khám phá</option></select></label>
        <label class="flex items-center gap-2 rounded-xl border border-slate-200 px-3"><span class="text-xs font-semibold text-slate-500">Tiến độ</span><select v-model="status" class="min-w-0 flex-1 bg-transparent py-2 text-xs font-semibold text-kids-text outline-none"><option value="">Tất cả</option><option value="not-started">Chưa học</option><option value="in-progress">Đang học</option><option value="completed">Đã hoàn thành</option></select></label>
        <label class="flex items-center gap-2 rounded-xl border border-slate-200 px-3"><span class="text-xs font-semibold text-slate-500">Sắp xếp</span><select v-model="sort" class="min-w-0 flex-1 bg-transparent py-2 text-xs font-semibold text-kids-text outline-none"><option v-if="!isPronunciationPage" value="recommended">Được đề xuất</option><option value="recent">Mới nhất</option><option value="name">Tên A-Z</option><option value="progress">Tiến độ</option></select></label>
        <div class="flex flex-wrap gap-2 sm:col-span-2 xl:col-span-full">
          <button type="button" class="inline-flex min-h-9 items-center gap-2 rounded-full border px-3 text-xs font-bold transition" :class="favoritesOnly ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-slate-200 text-slate-600 hover:bg-slate-50'" :aria-pressed="favoritesOnly" @click="favoritesOnly = !favoritesOnly"><AdminIcon name="heart" :size="15" /> Yêu thích</button>
          <button type="button" class="inline-flex min-h-9 items-center gap-2 rounded-full border px-3 text-xs font-bold transition" :class="starredOnly ? 'border-amber-200 bg-amber-50 text-amber-700' : 'border-slate-200 text-slate-600 hover:bg-slate-50'" :aria-pressed="starredOnly" @click="starredOnly = !starredOnly"><AdminIcon name="star" :size="15" /> Ưu tiên học</button>
        </div>
      </div>

      <div v-if="loading" class="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <div v-for="item in pageSize" :key="item" class="h-[390px] animate-pulse rounded-2xl bg-white shadow-sm"></div>
      </div>
      <div v-else-if="visibleTopics.length" class="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <StudentTopicCard v-for="topic in visibleTopics" :key="topic.slug" :topic="topic" :show-recommended="!isPronunciationPage" :action-label="isPronunciationPage ? 'Chọn chủ đề' : ''" @open="openTopic" @favorite="toggleFlag($event, 'favorites')" @star="toggleFlag($event, 'starred')" />
      </div>
      <div v-else-if="!errorMessage" class="mt-5 rounded-2xl border border-dashed border-amber-200 bg-white p-10 text-center">
        <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-amber-50 text-amber-700"><AdminIcon name="search" :size="23" /></span>
        <h4 class="mt-4 font-extrabold text-kids-text">Chưa tìm thấy chủ đề phù hợp</h4>
        <p class="mt-1 text-sm text-slate-500">Con thử đổi từ khóa hoặc bộ lọc nhé.</p>
        <button type="button" class="mt-4 text-sm font-bold text-sky-700 underline" @click="search = ''; level = ''; status = ''; favoritesOnly = false; starredOnly = false">Xóa bộ lọc</button>
      </div>

      <div v-if="!loading && filteredTopics.length" class="mt-6 flex flex-col items-center justify-between gap-3 sm:flex-row">
        <label class="flex items-center gap-2 text-xs text-slate-500">Hiển thị
          <select v-model.number="pageSize" class="rounded-lg border border-slate-200 bg-white px-2 py-1.5 font-bold text-kids-text"><option :value="6">6</option><option :value="9">9</option><option :value="12">12</option></select>
          chủ đề mỗi trang
        </label>
        <div class="flex items-center gap-2">
          <button type="button" class="min-h-10 rounded-xl border border-slate-200 bg-white px-3 text-xs font-bold text-slate-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="page <= 1" @click="page--">Trang trước</button>
          <span class="min-w-20 text-center text-xs font-semibold text-slate-500">Trang {{ page }} / {{ pageCount }}</span>
          <button type="button" class="min-h-10 rounded-xl border border-slate-200 bg-white px-3 text-xs font-bold text-slate-600 disabled:cursor-not-allowed disabled:opacity-40" :disabled="page >= pageCount" @click="page++">Trang sau</button>
        </div>
      </div>
    </section>
  </section>
</template>
