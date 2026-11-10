<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import PracticeNavigation from '../../components/pronunciation/PracticeNavigation.vue'
import PracticeStatistics from '../../components/pronunciation/PracticeStatistics.vue'
import PronunciationFeedback from '../../components/pronunciation/PronunciationFeedback.vue'
import PronunciationGuidePanel from '../../components/pronunciation/PronunciationGuidePanel.vue'
import PronunciationResultPanel from '../../components/pronunciation/PronunciationResultPanel.vue'
import RecordingPanel from '../../components/pronunciation/RecordingPanel.vue'
import VocabularyInfo from '../../components/pronunciation/VocabularyInfo.vue'
import { useAudioRecorder } from '../../composable/useAudioRecorder'
import { getTopicProgress, saveCurrentWord } from '../../services/studentProgressService'
import { createIllustrativePronunciationResult, getPracticeStatistics } from '../../services/studentPronunciationService'
import { getStudentTopicBySlug } from '../../services/studentTopicService'

const route = useRoute()
const router = useRouter()
const topic = ref(null)
const word = ref(null)
const result = ref(null)
const practiceStats = ref({ attempts: 0, bestScore: null, latestScore: null, completed: false, history: [] })
const loading = ref(true)
const errorMessage = ref('')
const resultError = ref('')
const {
  isRequesting,
  isRecording,
  isPlaying,
  duration,
  hasRecording,
  errorMessage: recordingError,
  startRecording,
  stopRecording,
  playRecording,
  reset: resetRecording,
} = useAudioRecorder()

const currentIndex = computed(() => topic.value?.words.findIndex((item) => item.id === word.value?.id) ?? -1)
const nextWord = computed(() => topic.value?.words[currentIndex.value + 1] || null)
const previousWord = computed(() => topic.value?.words[currentIndex.value - 1] || null)
const progressPercent = computed(() => {
  if (!topic.value) return 0
  const total = topic.value.words.length
  const completed = getTopicProgress(topic.value.slug, total).completed
  return total ? Math.round((completed / total) * 100) : 0
})

async function loadWord() {
  loading.value = true
  errorMessage.value = ''
  resultError.value = ''
  result.value = null
  window.speechSynthesis?.cancel()
  resetRecording()
  try {
    topic.value = await getStudentTopicBySlug(route.params.topicSlug)
    if (!topic.value) {
      word.value = null
      errorMessage.value = 'Không tìm thấy chủ đề hoặc chủ đề chưa được xuất bản.'
      return
    }
    word.value = topic.value.words.find((item) => item.id === route.params.wordId) || null
    if (!word.value) {
      errorMessage.value = 'Không tìm thấy từ vựng trong chủ đề này.'
      return
    }
    saveCurrentWord(topic.value.slug, word.value.id, topic.value.words.length)
    practiceStats.value = getPracticeStatistics(topic.value.slug, word.value.id)
  } catch (error) {
    console.error('Không thể tải bài luyện phát âm.', error)
    word.value = null
    errorMessage.value = 'Chưa tải được bài luyện. Con thử lại nhé!'
  } finally {
    loading.value = false
  }
}

async function confirmRecording() {
  if (!topic.value || !word.value || !hasRecording.value || isRecording.value || isRequesting.value) return
  resultError.value = ''
  try {
    result.value = await createIllustrativePronunciationResult({
      topicSlug: topic.value.slug,
      wordId: word.value.id,
      hasRecording: hasRecording.value,
      totalWords: topic.value.words.length,
    })
    practiceStats.value = getPracticeStatistics(topic.value.slug, word.value.id)
  } catch (error) {
    console.error('Không thể tạo kết quả minh họa.', error)
    resultError.value = error.message || 'Không thể lưu kết quả minh họa. Hãy thử lại nhé!'
  }
}

function practiceAgain() {
  result.value = null
  resultError.value = ''
  resetRecording()
}

function goToWord(target) {
  if (!target || !topic.value) return
  try {
    saveCurrentWord(topic.value.slug, target.id, topic.value.words.length)
    router.push({ name: 'StudentPronunciationPractice', params: { topicSlug: topic.value.slug, wordId: target.id } })
  } catch (error) {
    console.error('Không thể lưu vị trí học.', error)
    resultError.value = 'Chưa lưu được vị trí học. Con thử lại nhé!'
  }
}

watch(() => [route.params.topicSlug, route.params.wordId], loadWord)
onMounted(loadWord)
onUnmounted(() => window.speechSynthesis?.cancel())
</script>

<template>
  <section class="mx-auto max-w-[1050px] space-y-5 p-4 sm:p-6 xl:p-8">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <nav class="flex min-w-0 items-center gap-2 text-xs font-semibold text-slate-400" aria-label="Breadcrumb">
        <RouterLink :to="{ name: 'StudentTopics' }" class="shrink-0 hover:text-sky-700">Chủ đề học tập</RouterLink>
        <AdminIcon name="arrow" :size="13" />
        <RouterLink v-if="topic" :to="{ name: 'StudentTopicDetail', params: { topicSlug: topic.slug } }" class="truncate hover:text-sky-700">{{ topic.title }} · Danh sách từ</RouterLink>
        <span v-else class="text-slate-600">Luyện phát âm</span>
      </nav>
      <span v-if="topic && currentIndex >= 0" class="shrink-0 text-xs font-bold text-slate-500">Từ {{ currentIndex + 1 }}/{{ topic.words.length }}</span>
    </div>

    <div v-if="topic && word && !loading" class="rounded-2xl border border-amber-100 bg-white p-4 shadow-sm">
      <div class="flex items-center justify-between gap-3 text-xs"><span class="font-extrabold text-kids-text">Tiến trình chủ đề</span><span class="font-bold text-slate-500">{{ progressPercent }}% · {{ practiceStats.attempts }} lượt đã xác nhận với từ này</span></div>
      <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="progressPercent" aria-valuemin="0" aria-valuemax="100" aria-label="Tiến trình chủ đề"><div class="h-full rounded-full bg-gradient-to-r from-kids-primary to-kids-secondary transition-all" :style="{ width: `${progressPercent}%` }"></div></div>
    </div>

    <div v-if="loading" class="space-y-4" role="status" aria-live="polite">
      <span class="sr-only">Đang tải bài luyện phát âm...</span>
      <div class="h-72 animate-pulse rounded-3xl bg-white shadow-sm"></div><div class="h-52 animate-pulse rounded-3xl bg-white shadow-sm"></div>
    </div>
    <div v-else-if="errorMessage" class="rounded-3xl border border-rose-100 bg-white p-8 text-center shadow-sm" role="alert">
      <h2 class="text-xl font-extrabold text-kids-text">Chưa mở được bài luyện</h2><p class="mt-2 text-sm text-slate-500">{{ errorMessage }}</p>
      <RouterLink :to="{ name: 'StudentTopics' }" class="mt-5 inline-flex rounded-xl bg-kids-primary px-4 py-2.5 text-sm font-bold text-kids-text">Quay lại chủ đề</RouterLink>
    </div>

    <template v-else-if="topic && word">
      <header class="flex flex-wrap items-end justify-between gap-3">
        <div><p class="text-xs font-extrabold uppercase tracking-wider text-kids-cta">Cùng luyện từng từ</p><h1 class="mt-1 text-2xl font-extrabold text-kids-text sm:text-3xl">Luyện phát âm</h1></div>
        <span class="rounded-full bg-sky-50 px-3 py-1.5 text-[11px] font-bold text-sky-800">{{ topic.title }}</span>
      </header>

      <VocabularyInfo :word="word" :topic-title="topic.title" />
      <PronunciationGuidePanel :word="word" />
      <RecordingPanel
        :is-requesting="isRequesting"
        :is-recording="isRecording"
        :is-playing="isPlaying"
        :has-recording="hasRecording"
        :confirmed="Boolean(result)"
        :duration="duration"
        :error-message="recordingError"
        @start="startRecording"
        @stop="stopRecording"
        @play="playRecording"
        @retake="practiceAgain"
        @confirm="confirmRecording"
      />
      <p v-if="resultError" class="rounded-xl bg-rose-50 px-4 py-3 text-xs text-rose-700" role="alert">{{ resultError }}</p>

      <PronunciationResultPanel v-if="result" :result="result" />
      <section v-else class="rounded-3xl border border-dashed border-sky-200 bg-sky-50/60 p-5 text-center" aria-labelledby="result-placeholder-heading">
        <p class="text-xs font-extrabold uppercase tracking-wider text-sky-800">Danh mục 4</p>
        <h2 id="result-placeholder-heading" class="mt-1 font-extrabold text-kids-text">Kết quả chấm điểm</h2>
        <p class="mt-2 text-xs leading-5 text-slate-500">Sau khi con ghi âm và xác nhận, kết quả minh họa sẽ hiện ở đây. Không có AI phân tích âm thanh.</p>
      </section>

      <PronunciationFeedback v-if="result" :result="result" />
      <section v-else class="rounded-3xl border border-dashed border-amber-200 bg-amber-50/50 p-5 text-center" aria-labelledby="feedback-placeholder-heading">
        <p class="text-xs font-extrabold uppercase tracking-wider text-amber-900">Danh mục 5</p>
        <h2 id="feedback-placeholder-heading" class="mt-1 font-extrabold text-kids-text">Nhận xét và sửa lỗi</h2>
        <p class="mt-2 text-xs leading-5 text-slate-500">Nhận xét minh họa chỉ xuất hiện sau khi con xác nhận bản ghi.</p>
      </section>

      <PracticeStatistics :stats="practiceStats" />
      <PracticeNavigation
        :topic-slug="topic.slug"
        :previous-word="previousWord"
        :next-word="nextWord"
        :confirmed="Boolean(result)"
        @previous="goToWord(previousWord)"
        @next="goToWord(nextWord)"
        @retry="practiceAgain"
      />
      <p class="pb-2 text-center text-[10px] text-slate-400">Tệp ghi âm được giữ tạm trong trình duyệt và sẽ bị xóa khi rời trang. Kết quả và thống kê là dữ liệu mô phỏng.</p>
    </template>
  </section>
</template>
