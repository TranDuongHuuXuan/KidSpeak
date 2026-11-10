<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import StudentResultChart from '../../components/student/StudentResultChart.vue'
import {
  comparisonBarOption,
  pronunciationBarOption,
  progressLineOption,
  practiceWeekdayOption,
  topicDistributionOption,
} from '../../data/studentResultsChartOptions'
import { getStudentResultsChartData } from '../../services/studentResultsChartService'
import { getStudentResults } from '../../services/studentResultsService'

const router = useRouter()
const report = ref(null)
const loading = ref(true)
const errorMessage = ref('')
const topicStatus = ref('all')
const historyQuery = ref('')
const historyRange = ref('all')
const historyStatus = ref('all')
const historyPage = ref(1)
const wordQuery = ref('')
const wordPart = ref('all')
const wordSort = ref('score')
const wordPage = ref(1)
const chartRange = ref(7)
const expandedHistory = ref('')
const pageSize = 6

const summaryCards = computed(() => {
  if (!report.value) return []
  const stats = report.value.stats
  return [
    { label: 'Chủ đề đã tham gia', value: stats.participatedTopics, icon: 'book', color: 'bg-sky-50 text-sky-700', note: `Trong ${stats.totalTopics} chủ đề` },
    { label: 'Chủ đề hoàn thành', value: stats.completedTopics, icon: 'circleCheck', color: 'bg-emerald-50 text-emerald-700', note: 'Đã học hết các từ' },
    { label: 'Từ vựng đã học', value: stats.learnedWords, icon: 'education', color: 'bg-amber-50 text-amber-700', note: 'Từ đã hoàn thành' },
    { label: 'Từ đã luyện phát âm', value: stats.practicedWords, icon: 'microphone', color: 'bg-orange-50 text-orange-700', note: 'Tính theo từ riêng biệt' },
    { label: 'Tiến độ học trung bình', value: stats.averageLearning === null ? '—' : `${stats.averageLearning}%`, icon: 'chart', color: 'bg-violet-50 text-violet-700', note: 'Trung bình các chủ đề đã bắt đầu' },
    { label: 'Điểm phát âm trung bình', value: stats.averagePronunciation === null ? '—' : `${stats.averagePronunciation}/100`, icon: 'sparkles', color: 'bg-rose-50 text-rose-700', note: 'Từ các lượt minh họa đã xác nhận' },
  ]
})

const filteredTopics = computed(() => {
  if (!report.value) return []
  return report.value.topics.filter((topic) => topicStatus.value === 'all' || topic.progress.status === topicStatus.value)
})

const filteredHistory = computed(() => {
  if (!report.value) return []
  const query = historyQuery.value.trim().toLocaleLowerCase('vi')
  const cutoff = getCutoff(historyRange.value)
  return report.value.history.filter((item) => {
    const matchesQuery = !query || item.topicTitle.toLocaleLowerCase('vi').includes(query)
    const matchesDate = !cutoff || item.date >= cutoff
    const matchesStatus = historyStatus.value === 'all' || item.status === historyStatus.value
    return matchesQuery && matchesDate && matchesStatus
  })
})

const historyPageCount = computed(() => Math.max(1, Math.ceil(filteredHistory.value.length / pageSize)))
const pagedHistory = computed(() => filteredHistory.value.slice((historyPage.value - 1) * pageSize, historyPage.value * pageSize))

const filteredWords = computed(() => {
  if (!report.value) return []
  const query = wordQuery.value.trim().toLocaleLowerCase('vi')
  const words = report.value.needsPractice.filter((item) => {
    const matchesQuery = !query || `${item.word} ${item.topicTitle}`.toLocaleLowerCase('vi').includes(query)
    const matchesPart = wordPart.value === 'all'
      || item.improvementParts.some((part) => part.key === wordPart.value)
    return matchesQuery && matchesPart
  })
  return words.sort(wordSort.value === 'recent'
    ? (a, b) => new Date(b.practicedAt) - new Date(a.practicedAt)
    : (a, b) => a.score - b.score)
})

const wordPageCount = computed(() => Math.max(1, Math.ceil(filteredWords.value.length / pageSize)))
const pagedWords = computed(() => filteredWords.value.slice((wordPage.value - 1) * pageSize, wordPage.value * pageSize))

const chartData = computed(() => report.value
  ? getStudentResultsChartData(report.value, chartRange.value)
  : null)
const progressChartOption = computed(() => chartData.value ? progressLineOption(chartData.value) : {})
const topicChartOption = computed(() => chartData.value ? topicDistributionOption(chartData.value) : {})
const componentChartOption = computed(() => chartData.value ? pronunciationBarOption(chartData.value) : {})
const practiceChartOption = computed(() => chartData.value ? practiceWeekdayOption(chartData.value) : {})
const comparisonChartOption = computed(() => chartData.value ? comparisonBarOption(chartData.value) : {})

const progressPercent = computed(() => {
  const stats = report.value?.stats
  return stats?.totalTopics ? Math.round((stats.completedTopics / stats.totalTopics) * 100) : 0
})

watch([historyQuery, historyRange, historyStatus], () => { historyPage.value = 1 })
watch([wordQuery, wordPart, wordSort], () => { wordPage.value = 1 })
watch(filteredHistory, () => {
  if (historyPage.value > historyPageCount.value) historyPage.value = historyPageCount.value
})
watch(filteredWords, () => {
  if (wordPage.value > wordPageCount.value) wordPage.value = wordPageCount.value
})

function getCutoff(range) {
  if (range === 'all') return ''
  const date = new Date()
  date.setHours(0, 0, 0, 0)
  date.setDate(date.getDate() - Number(range) + 1)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function formatDate(date) {
  return new Date(`${date}T00:00:00`).toLocaleDateString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

function statusClass(status) {
  if (status === 'completed') return 'bg-emerald-50 text-emerald-700'
  if (status === 'in-progress') return 'bg-sky-50 text-sky-700'
  return 'bg-slate-100 text-slate-500'
}

function startPractice(item) {
  router.push({
    name: 'StudentPronunciationPractice',
    params: { topicSlug: item.topicSlug, wordId: item.wordId },
  })
}

async function loadReport() {
  loading.value = true
  errorMessage.value = ''
  try {
    report.value = await getStudentResults()
  } catch (error) {
    console.error('Không thể tải kết quả học tập.', error)
    errorMessage.value = 'Chưa thể đọc dữ liệu học tập trên thiết bị này. Hãy thử tải lại trang.'
  } finally {
    loading.value = false
  }
}

onMounted(loadReport)
</script>

<template>
  <section class="mx-auto max-w-[1440px] space-y-6 p-4 sm:p-6 xl:p-8">
    <header class="flex flex-wrap items-end justify-between gap-4">
      <div>
        <p class="text-xs font-extrabold uppercase tracking-[0.16em] text-kids-cta">Con đang tiến bộ mỗi ngày</p>
        <h1 class="mt-1 text-2xl font-extrabold text-kids-text sm:text-3xl">Kết quả học tập</h1>
        <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500">Cùng nhìn lại những chủ đề con đã khám phá và các lượt luyện phát âm đã xác nhận.</p>
      </div>
      <RouterLink :to="{ name: 'StudentTopics' }" class="inline-flex min-h-11 items-center gap-2 rounded-xl bg-kids-primary px-4 text-sm font-extrabold text-kids-text transition hover:bg-amber-400">
        <AdminIcon name="book" :size="17" /> Tiếp tục học <AdminIcon name="arrow" :size="15" />
      </RouterLink>
    </header>

    <div class="rounded-2xl border border-sky-100 bg-sky-50 px-4 py-3 text-xs leading-5 text-sky-900">
      <strong>Dữ liệu minh họa:</strong> điểm phát âm trong bản demo được tạo sau khi con chủ động xác nhận bản ghi; đây không phải kết quả phân tích AI. Thành tích chỉ được mở khóa khi đạt điều kiện hiển thị.
    </div>

    <div v-if="loading" class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" role="status" aria-live="polite">
      <span class="sr-only">Đang tổng hợp kết quả học tập...</span>
      <div v-for="item in 6" :key="item" class="h-32 animate-pulse rounded-2xl bg-white shadow-sm"></div>
    </div>
    <div v-else-if="errorMessage" class="rounded-3xl border border-rose-100 bg-white p-8 text-center shadow-sm" role="alert">
      <h2 class="text-lg font-extrabold text-kids-text">Chưa tải được kết quả</h2>
      <p class="mt-2 text-sm text-slate-500">{{ errorMessage }}</p>
      <button type="button" class="mt-4 rounded-xl bg-kids-primary px-4 py-2.5 text-sm font-bold text-kids-text" @click="loadReport">Thử lại</button>
    </div>
    <template v-else-if="report">
      <section aria-labelledby="results-overview-heading">
        <div class="mb-3 flex items-center gap-2">
          <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-100 text-amber-800"><AdminIcon name="chart" :size="18" /></span>
          <h2 id="results-overview-heading" class="text-lg font-extrabold text-kids-text">Tổng quan kết quả</h2>
        </div>
        <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="card in summaryCards" :key="card.label" class="rounded-2xl border border-amber-100 bg-white p-4 shadow-sm">
            <div class="flex items-start justify-between gap-3">
              <div><p class="text-xs font-semibold text-slate-500">{{ card.label }}</p><p class="mt-2 text-3xl font-extrabold text-kids-text">{{ card.value }}</p></div>
              <span class="flex h-11 w-11 items-center justify-center rounded-xl" :class="card.color"><AdminIcon :name="card.icon" :size="21" /></span>
            </div>
            <p class="mt-2 text-[11px] text-slate-400">{{ card.note }}</p>
          </article>
        </div>
      </section>

      <section class="space-y-4" aria-label="Biểu đồ kết quả học tập">
        <article class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="learning-progress-chart-heading">
          <div class="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Biểu đồ 1</p>
              <h2 id="learning-progress-chart-heading" class="mt-1 text-lg font-extrabold text-kids-text">Tiến bộ học tập theo thời gian</h2>
              <p class="mt-1 text-xs text-slate-500">Tỷ lệ hoàn thành chủ đề được ghi nhận theo ngày, tuần hoặc tháng.</p>
            </div>
            <label class="flex items-center gap-2 text-xs font-bold text-slate-600">Khoảng thời gian
              <select v-model.number="chartRange" class="rounded-lg border border-slate-200 bg-white px-3 py-2 outline-none focus:border-sky-400"><option :value="7">7 ngày gần nhất</option><option :value="30">30 ngày gần nhất</option><option :value="90">3 tháng gần nhất</option></select>
            </label>
          </div>
          <div v-if="chartData.learningHasData" class="mt-3">
            <StudentResultChart :option="progressChartOption" label="Biểu đồ đường tiến độ hoàn thành chủ đề theo thời gian" :height="340" />
            <p class="mt-1 text-[10px] text-slate-400">Trục dọc là phần trăm từ đã hoàn thành trong chủ đề, không phải điểm kiểm tra.</p>
          </div>
          <p v-else class="mt-4 rounded-2xl bg-slate-50 p-6 text-center text-sm leading-6 text-slate-500">Chưa có mốc tiến độ theo thời gian. Mốc đầu tiên sẽ được ghi nhận khi con bắt đầu một chủ đề; lịch sử cũ không được suy đoán hoặc tạo lại.</p>
        </article>

        <div class="grid items-stretch gap-4 xl:grid-cols-2">
          <article class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="topic-distribution-chart-heading">
            <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Biểu đồ 2</p>
            <h2 id="topic-distribution-chart-heading" class="mt-1 text-lg font-extrabold text-kids-text">Phân bố tiến độ chủ đề</h2>
            <p class="mt-1 text-xs text-slate-500">Trạng thái hiện tại của {{ chartData.totalTopics }} chủ đề.</p>
            <StudentResultChart :option="topicChartOption" label="Biểu đồ donut phân bố chủ đề hoàn thành, đang học và chưa bắt đầu" :height="300" />
            <div class="grid grid-cols-3 gap-2 text-center text-[10px]">
              <p><strong class="text-emerald-700">{{ chartData.distribution[0].value }}</strong> hoàn thành</p>
              <p><strong class="text-sky-700">{{ chartData.distribution[1].value }}</strong> đang học</p>
              <p><strong class="text-slate-500">{{ chartData.distribution[2].value }}</strong> chưa bắt đầu</p>
            </div>
          </article>

          <article class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="pronunciation-chart-heading">
            <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Biểu đồ 3</p>
            <h2 id="pronunciation-chart-heading" class="mt-1 text-lg font-extrabold text-kids-text">Phân tích khả năng phát âm</h2>
            <p class="mt-1 text-xs text-slate-500">Điểm trung bình âm đầu, phần vần và thanh điệu trong {{ chartRange === 90 ? '3 tháng' : `${chartRange} ngày` }} gần nhất.</p>
            <StudentResultChart v-if="chartData.componentsHaveData" :option="componentChartOption" label="Biểu đồ cột điểm trung bình âm đầu, phần vần và thanh điệu" :height="260" />
            <p v-else class="mt-4 flex h-[260px] items-center justify-center rounded-2xl bg-slate-50 p-5 text-center text-sm text-slate-500">Chưa có điểm thành phần trong khoảng thời gian này.</p>
            <p v-if="chartData.bestComponent" class="rounded-xl bg-sky-50 p-3 text-xs leading-5 text-sky-900">
              Điểm cao nhất: <strong>{{ chartData.bestComponent.label }} ({{ chartData.bestComponent.score }}/100)</strong>.
              <template v-if="chartData.lowestComponent"> Nên luyện thêm: <strong>{{ chartData.lowestComponent.label }} ({{ chartData.lowestComponent.score }}/100)</strong>.</template>
            </p>
            <p v-else class="rounded-xl bg-slate-50 p-3 text-xs leading-5 text-slate-500">Chỉ nhận xét khi có dữ liệu chấm thành phần; hiện chưa có kết luận nào.</p>
          </article>
        </div>

        <div class="grid items-stretch gap-4 xl:grid-cols-2">
          <article class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="practice-weekday-chart-heading">
            <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Biểu đồ 4</p>
            <h2 id="practice-weekday-chart-heading" class="mt-1 text-lg font-extrabold text-kids-text">Số lượt luyện phát âm</h2>
            <p class="mt-1 text-xs text-slate-500">Phân bố theo ngày trong tuần, trong {{ chartRange === 90 ? '3 tháng' : `${chartRange} ngày` }} đã chọn.</p>
            <StudentResultChart v-if="chartData.hasPracticeData" :option="practiceChartOption" label="Biểu đồ cột số lượt luyện phát âm theo ngày trong tuần" :height="300" />
            <p v-else class="mt-4 flex h-[300px] items-center justify-center rounded-2xl bg-slate-50 p-5 text-center text-sm text-slate-500">Chưa có lượt luyện được xác nhận trong khoảng thời gian này.</p>
          </article>

          <article class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="learning-pronunciation-comparison-heading">
            <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Biểu đồ 5</p>
            <h2 id="learning-pronunciation-comparison-heading" class="mt-1 text-lg font-extrabold text-kids-text">So sánh tiến độ học và phát âm</h2>
            <p class="mt-1 text-xs text-slate-500">So sánh tỷ lệ hoàn thành chủ đề với điểm phát âm theo cùng khoảng thời gian.</p>
            <div class="mt-2 flex flex-wrap gap-4 text-[10px] text-slate-600">
              <span class="inline-flex items-center gap-2"><i class="h-2.5 w-2.5 rounded-sm bg-kids-primary"></i> Tiến độ học tập (%)</span>
              <span class="inline-flex items-center gap-2"><i class="h-2.5 w-2.5 rounded-sm bg-violet-500"></i> Điểm luyện phát âm</span>
            </div>
            <StudentResultChart v-if="chartData.hasComparisonData" :option="comparisonChartOption" label="Biểu đồ cột nhóm so sánh tiến độ học tập và điểm phát âm" :height="276" />
            <p v-else class="mt-4 flex h-[276px] items-center justify-center rounded-2xl bg-slate-50 p-5 text-center text-sm text-slate-500">Chưa có dữ liệu lịch sử để so sánh trong khoảng thời gian này.</p>
            <p class="text-[10px] leading-5 text-slate-400">Mỗi chuỗi chỉ hiện khi có dữ liệu thật đã lưu; không có điểm học tập lịch sử thì cột tương ứng để trống.</p>
          </article>
        </div>
      </section>

      <section class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="topic-progress-heading">
        <div class="flex flex-wrap items-end justify-between gap-3">
          <div>
            <p class="text-xs font-extrabold uppercase tracking-wider text-sky-700">Hành trình của con</p>
            <h2 id="topic-progress-heading" class="mt-1 text-lg font-extrabold text-kids-text">Tiến độ học tập</h2>
            <p class="mt-1 text-xs text-slate-500">{{ report.stats.completedTopics }} hoàn thành · {{ report.stats.inProgressTopics }} đang học · {{ report.stats.notStartedTopics }} chưa bắt đầu</p>
          </div>
          <label class="flex items-center gap-2 text-xs font-bold text-slate-600">Lọc chủ đề
            <select v-model="topicStatus" class="rounded-lg border border-slate-200 bg-white px-3 py-2 outline-none focus:border-sky-400">
              <option value="all">Tất cả</option><option value="in-progress">Đang học</option><option value="completed">Hoàn thành</option><option value="not-started">Chưa bắt đầu</option>
            </select>
          </label>
        </div>
        <div class="mt-5 grid gap-5 lg:grid-cols-[250px_1fr]">
          <div class="rounded-2xl bg-kids-bg p-4">
            <div class="flex items-center justify-between text-xs font-bold text-slate-600"><span>Hoàn thành chủ đề</span><span>{{ progressPercent }}%</span></div>
            <div class="mt-3 h-3 overflow-hidden rounded-full bg-white" role="progressbar" :aria-valuenow="progressPercent" aria-valuemin="0" aria-valuemax="100" aria-label="Tỷ lệ chủ đề hoàn thành"><div class="h-full rounded-full bg-gradient-to-r from-kids-primary to-kids-secondary transition-all" :style="{ width: `${progressPercent}%` }"></div></div>
            <p class="mt-3 text-xs leading-5 text-slate-500">Con đã hoàn thành {{ report.stats.completedTopics }} trên {{ report.stats.totalTopics }} chủ đề.</p>
            <div class="mt-4 grid grid-cols-3 gap-2 text-center">
              <div><p class="text-lg font-extrabold text-emerald-700">{{ report.stats.completedTopics }}</p><p class="text-[9px] text-slate-500">Xong</p></div>
              <div><p class="text-lg font-extrabold text-sky-700">{{ report.stats.inProgressTopics }}</p><p class="text-[9px] text-slate-500">Đang học</p></div>
              <div><p class="text-lg font-extrabold text-slate-500">{{ report.stats.notStartedTopics }}</p><p class="text-[9px] text-slate-500">Chưa học</p></div>
            </div>
          </div>
          <div v-if="filteredTopics.length" class="grid gap-3 md:grid-cols-2">
            <article v-for="topic in filteredTopics" :key="topic.slug" class="flex gap-3 rounded-2xl border border-slate-100 p-3">
              <img :src="topic.image" :alt="topic.imageAlt" class="h-16 w-16 shrink-0 rounded-xl object-cover" loading="lazy" />
              <div class="min-w-0 flex-1">
                <div class="flex flex-wrap items-start justify-between gap-2"><h3 class="text-sm font-extrabold text-kids-text">{{ topic.title }}</h3><span class="rounded-full px-2 py-1 text-[9px] font-bold" :class="statusClass(topic.progress.status)">{{ topic.statusLabel }}</span></div>
                <p class="mt-1 text-[11px] text-slate-500">{{ topic.level }} · {{ topic.studiedWords }}/{{ topic.wordCount }} từ đã học</p>
                <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="topic.progress.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${topic.title}`"><div class="h-full rounded-full bg-sky-400" :style="{ width: `${topic.progress.progress}%` }"></div></div>
              </div>
            </article>
          </div>
          <p v-else class="rounded-2xl bg-slate-50 p-6 text-center text-sm text-slate-500">Không có chủ đề trong trạng thái này.</p>
        </div>
      </section>

      <section class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="pronunciation-results-heading">
        <div class="flex items-center gap-2">
          <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-orange-50 text-orange-700"><AdminIcon name="microphone" :size="18" /></span>
          <div><h2 id="pronunciation-results-heading" class="text-lg font-extrabold text-kids-text">Kết quả luyện phát âm</h2><p class="text-[11px] text-slate-500">Tách riêng số lượt luyện và số từ đã luyện.</p></div>
        </div>
        <div class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="item in [
            { label: 'Tổng lượt ghi âm đã xác nhận', value: report.stats.practiceAttempts, icon: 'microphone' },
            { label: 'Số từ đã luyện', value: report.stats.practicedWords, icon: 'book' },
            { label: 'Điểm trung bình', value: report.stats.averagePronunciation === null ? '—' : `${report.stats.averagePronunciation}/100`, icon: 'chart' },
            { label: 'Điểm cao nhất', value: report.stats.highestScore === null ? '—' : `${report.stats.highestScore}/100`, icon: 'trophy' },
            { label: 'Từ đạt mục tiêu (từ 80 điểm)', value: report.stats.goalWords, icon: 'target' },
            { label: 'Từ cần luyện thêm', value: report.stats.wordsToImprove, icon: 'sparkles' },
          ]" :key="item.label" class="flex items-center gap-3 rounded-2xl bg-slate-50 p-4">
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-white text-sky-700 shadow-sm"><AdminIcon :name="item.icon" :size="19" /></span>
            <div><p class="text-[11px] font-semibold text-slate-500">{{ item.label }}</p><p class="mt-1 text-2xl font-extrabold text-kids-text">{{ item.value }}</p></div>
          </article>
        </div>
      </section>

      <section class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="learning-history-heading">
        <div class="flex flex-wrap items-end justify-between gap-3">
          <div><h2 id="learning-history-heading" class="text-lg font-extrabold text-kids-text">Lịch sử học tập</h2><p class="mt-1 text-xs text-slate-500">Gom các lượt xác nhận theo ngày và chủ đề; số từ được đếm riêng biệt trong nhóm.</p></div>
          <span class="text-xs font-bold text-slate-500">{{ filteredHistory.length }} buổi</span>
        </div>
        <div class="mt-4 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">
          <label class="relative"><span class="sr-only">Tìm theo chủ đề</span><AdminIcon name="search" :size="16" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input v-model="historyQuery" class="min-h-10 w-full rounded-xl border border-slate-200 pl-9 pr-3 text-xs outline-none focus:border-sky-400" placeholder="Tìm tên chủ đề" /></label>
          <select v-model="historyRange" aria-label="Lọc lịch sử theo thời gian" class="min-h-10 rounded-xl border border-slate-200 px-3 text-xs outline-none focus:border-sky-400"><option value="all">Mọi thời gian</option><option value="7">7 ngày gần nhất</option><option value="30">30 ngày gần nhất</option><option value="90">3 tháng gần nhất</option></select>
          <select v-model="historyStatus" aria-label="Lọc lịch sử theo trạng thái" class="min-h-10 rounded-xl border border-slate-200 px-3 text-xs outline-none focus:border-sky-400"><option value="all">Mọi trạng thái</option><option value="in-progress">Đang học</option><option value="completed">Hoàn thành</option><option value="not-started">Chưa bắt đầu</option></select>
        </div>
        <div v-if="pagedHistory.length" class="mt-4 space-y-2">
          <article v-for="item in pagedHistory" :key="item.id" class="rounded-2xl border border-slate-100">
            <div class="grid items-center gap-2 p-3 sm:grid-cols-[1fr_auto_auto_auto]">
              <div><p class="text-xs font-extrabold text-kids-text">{{ item.topicTitle }}</p><p class="mt-1 text-[10px] text-slate-500">{{ formatDate(item.date) }} · {{ item.topicLevel }}</p></div>
              <p class="text-[11px] text-slate-600">{{ item.learnedWords }} từ học · {{ item.practicedWords }} từ luyện</p>
              <span class="text-xs font-extrabold text-kids-text">{{ item.averageScore }}/100 <small class="font-medium text-slate-400">minh họa</small></span>
              <div class="flex items-center gap-2"><span class="rounded-full px-2 py-1 text-[9px] font-bold" :class="statusClass(item.status)">{{ item.statusLabel }}</span><button type="button" class="rounded-lg p-2 text-sky-700 hover:bg-sky-50" :aria-expanded="expandedHistory === item.id" :aria-label="`${expandedHistory === item.id ? 'Ẩn' : 'Xem'} chi tiết ${item.topicTitle}`" @click="expandedHistory = expandedHistory === item.id ? '' : item.id"><AdminIcon :name="expandedHistory === item.id ? 'chevronDown' : 'arrow'" :size="16" /></button></div>
            </div>
            <div v-if="expandedHistory === item.id" class="border-t border-slate-100 bg-slate-50 px-4 py-3 text-[11px] text-slate-600">
              <p>{{ item.attempts }} lượt xác nhận, {{ item.wordIds.length }} từ riêng biệt. Điểm nhóm là trung bình các lượt trong ngày.</p>
              <p class="mt-1">Từ đã luyện: {{ item.wordIds.map((id) => report.attempts.find((attempt) => attempt.topicSlug === item.topicSlug && attempt.wordId === id)?.word).filter(Boolean).join(', ') || 'Chưa có chi tiết' }}.</p>
            </div>
          </article>
        </div>
        <p v-else class="mt-4 rounded-2xl bg-slate-50 p-6 text-center text-sm text-slate-500">Chưa tìm thấy lịch sử phù hợp với bộ lọc.</p>
        <div v-if="historyPageCount > 1" class="mt-4 flex items-center justify-center gap-3">
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold disabled:opacity-40" :disabled="historyPage <= 1" @click="historyPage--">Trước</button>
          <span class="text-xs text-slate-500">Trang {{ historyPage }}/{{ historyPageCount }}</span>
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold disabled:opacity-40" :disabled="historyPage >= historyPageCount" @click="historyPage++">Sau</button>
        </div>
      </section>

      <section class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="improve-words-heading">
        <div class="flex flex-wrap items-end justify-between gap-3">
          <div><h2 id="improve-words-heading" class="text-lg font-extrabold text-kids-text">Từ vựng cần luyện thêm</h2><p class="mt-1 text-xs text-slate-500">Chỉ liệt kê từ có điểm tổng thể dưới 80 hoặc điểm thành phần dưới 75.</p></div>
          <span class="rounded-full bg-amber-50 px-3 py-1.5 text-[11px] font-bold text-amber-800">{{ report.needsPractice.length }} từ</span>
        </div>
        <div class="mt-4 grid gap-2 sm:grid-cols-3">
          <label class="relative"><span class="sr-only">Tìm từ vựng</span><AdminIcon name="search" :size="16" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input v-model="wordQuery" class="min-h-10 w-full rounded-xl border border-slate-200 pl-9 pr-3 text-xs outline-none focus:border-sky-400" placeholder="Tìm từ hoặc chủ đề" /></label>
          <select v-model="wordPart" aria-label="Lọc theo thành phần phát âm" class="min-h-10 rounded-xl border border-slate-200 px-3 text-xs outline-none focus:border-sky-400"><option value="all">Mọi thành phần</option><option value="initial">Âm đầu</option><option value="final">Phần vần</option><option value="tone">Thanh điệu</option></select>
          <select v-model="wordSort" aria-label="Sắp xếp từ cần luyện" class="min-h-10 rounded-xl border border-slate-200 px-3 text-xs outline-none focus:border-sky-400"><option value="score">Điểm thấp đến cao</option><option value="recent">Luyện gần đây</option></select>
        </div>
        <div v-if="pagedWords.length" class="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          <article v-for="item in pagedWords" :key="item.id" class="flex gap-3 rounded-2xl border border-slate-100 p-3">
            <img :src="item.image" :alt="item.imageAlt" class="h-20 w-20 shrink-0 rounded-xl object-cover" loading="lazy" />
            <div class="min-w-0 flex-1">
              <div class="flex items-start justify-between gap-2"><div><h3 class="text-base font-extrabold text-kids-text">{{ item.word }}</h3><p class="text-[10px] text-slate-500">{{ item.phonetic || 'Chưa có phiên âm' }} · {{ item.topicTitle }}</p></div><span class="rounded-lg bg-amber-50 px-2 py-1 text-xs font-extrabold text-amber-800">{{ item.score }}/100</span></div>
              <p class="mt-2 text-[10px] leading-4 text-slate-600">{{ item.improvementLabel }} · {{ item.attempts }} lượt luyện</p>
              <button type="button" class="mt-2 inline-flex min-h-9 items-center gap-1.5 rounded-lg bg-kids-primary px-3 text-[11px] font-extrabold text-kids-text hover:bg-amber-400" @click="startPractice(item)">Luyện tập lại <AdminIcon name="arrow" :size="13" /></button>
            </div>
          </article>
        </div>
        <p v-else class="mt-4 rounded-2xl bg-emerald-50 p-6 text-center text-sm leading-6 text-emerald-800">{{ report.needsPractice.length ? 'Không có từ phù hợp với bộ lọc hiện tại.' : 'Tuyệt vời! Chưa có từ nào cần luyện thêm theo các ngưỡng điểm minh họa.' }}</p>
        <div v-if="wordPageCount > 1" class="mt-4 flex items-center justify-center gap-3">
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold disabled:opacity-40" :disabled="wordPage <= 1" @click="wordPage--">Trước</button>
          <span class="text-xs text-slate-500">Trang {{ wordPage }}/{{ wordPageCount }}</span>
          <button type="button" class="rounded-lg border border-slate-200 px-3 py-2 text-xs font-bold disabled:opacity-40" :disabled="wordPage >= wordPageCount" @click="wordPage++">Sau</button>
        </div>
      </section>

      <section class="rounded-3xl border border-amber-100 bg-white p-4 shadow-sm sm:p-6" aria-labelledby="achievements-heading">
        <div class="flex flex-wrap items-end justify-between gap-3">
          <div><h2 id="achievements-heading" class="text-lg font-extrabold text-kids-text">Thành tích và huy hiệu</h2><p class="mt-1 text-xs text-slate-500">Huy hiệu được mở khóa dựa trên tiến độ đang lưu trên thiết bị.</p></div>
          <div class="flex gap-4 text-center"><div><p class="text-lg font-extrabold text-kids-text">{{ report.stats.studyStreak }}</p><p class="text-[9px] text-slate-500">Ngày liên tục</p></div><div><p class="text-lg font-extrabold text-kids-text">{{ report.stats.studySessions }}</p><p class="text-[9px] text-slate-500">Buổi học</p></div><div><p class="text-lg font-extrabold text-kids-text">{{ report.stats.learnedWords }}</p><p class="text-[9px] text-slate-500">Từ đã học</p></div></div>
        </div>
        <div class="mt-4 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <article v-for="badge in report.badges" :key="badge.id" class="flex gap-3 rounded-2xl border p-4" :class="badge.earned ? 'border-amber-200 bg-amber-50/60' : 'border-slate-100 bg-slate-50/70'">
            <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl" :class="badge.earned ? 'bg-kids-primary/50 text-amber-900' : 'bg-white text-slate-400'"><AdminIcon :name="badge.icon" :size="21" /></span>
            <div class="min-w-0"><div class="flex items-center gap-2"><h3 class="text-xs font-extrabold text-kids-text">{{ badge.name }}</h3><span class="rounded-full px-2 py-0.5 text-[9px] font-bold" :class="badge.earned ? 'bg-emerald-100 text-emerald-800' : 'bg-white text-slate-500'">{{ badge.earned ? 'Đã đạt' : 'Chưa đạt' }}</span></div><p class="mt-1 text-[10px] leading-4 text-slate-500">{{ badge.description }}</p><p class="mt-1 text-[10px] font-bold text-slate-600">Tiến độ: {{ Math.min(badge.current, badge.target) }}/{{ badge.target }}</p></div>
          </article>
        </div>
        <div class="mt-4 rounded-2xl bg-sky-50 p-4">
          <h3 class="text-xs font-extrabold text-sky-900">Mục tiêu học tập</h3>
          <div class="mt-2 grid gap-2 sm:grid-cols-2">
            <p class="flex items-center gap-2 text-[11px] text-sky-900"><AdminIcon :name="report.stats.completedTopics > 0 ? 'circleCheck' : 'target'" :size="16" />Hoàn thành chủ đề đầu tiên: {{ report.stats.completedTopics > 0 ? 'Đã hoàn thành' : 'Chưa hoàn thành' }}</p>
            <p class="flex items-center gap-2 text-[11px] text-sky-900"><AdminIcon :name="report.stats.learnedWords >= 10 ? 'circleCheck' : 'target'" :size="16" />Học 10 từ vựng: {{ Math.min(report.stats.learnedWords, 10) }}/10 từ</p>
          </div>
        </div>
      </section>
    </template>
  </section>
</template>
