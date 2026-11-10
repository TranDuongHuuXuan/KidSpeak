<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import StudentVocabularyCard from '../../components/student/StudentVocabularyCard.vue'
import { getNextUncompletedWord, getTopicProgress, startTopic, toggleTopicFlag } from '../../services/studentProgressService'
import { getStudentTopicBySlug } from '../../services/studentTopicService'

const route = useRoute()
const router = useRouter()
const topic = ref(null)
const loading = ref(true)
const errorMessage = ref('')
const updateError = ref('')
const topicProgress = computed(() => topic.value ? getTopicProgress(topic.value.slug, topic.value.words.length) : null)
const nextWord = computed(() => topic.value && topicProgress.value ? getNextUncompletedWord(topic.value, topicProgress.value) : null)

async function loadTopic() {
  loading.value = true
  errorMessage.value = ''
  try {
    topic.value = await getStudentTopicBySlug(route.params.topicSlug)
    if (!topic.value) errorMessage.value = 'Không tìm thấy chủ đề hoặc chủ đề chưa được xuất bản.'
  } catch (error) {
    console.error('Không thể tải chi tiết chủ đề.', error)
    errorMessage.value = 'Chưa tải được chủ đề. Con thử lại nhé!'
  } finally {
    loading.value = false
  }
}

function startLearning(word = nextWord.value) {
  if (!topic.value || !word) return
  try {
    startTopic(topic.value.slug, word.id, topic.value.words.length)
    router.push({ name: 'StudentPronunciationPractice', params: { topicSlug: topic.value.slug, wordId: word.id } })
  } catch (error) {
    console.error('Không thể lưu tiến độ chủ đề.', error)
    updateError.value = 'Chưa lưu được tiến độ. Con thử lại nhé!'
  }
}

function updateFlag(flag) {
  if (!topic.value) return
  try {
    toggleTopicFlag(topic.value.slug, flag)
    loadTopic()
  } catch (error) {
    console.error('Không thể cập nhật lựa chọn chủ đề.', error)
    updateError.value = 'Chưa cập nhật được lựa chọn chủ đề.'
  }
}

watch(() => route.params.topicSlug, loadTopic, { immediate: true })
</script>

<template>
  <section class="mx-auto max-w-[1200px] space-y-6 p-4 sm:p-6 xl:p-8">
    <div class="flex items-center gap-2 text-xs font-semibold text-slate-400">
      <RouterLink :to="{ name: 'StudentTopics' }" class="hover:text-sky-700">Chủ đề học tập</RouterLink>
      <AdminIcon name="arrow" :size="13" />
      <span class="truncate text-slate-600">{{ topic?.title || 'Chi tiết chủ đề' }}</span>
    </div>

    <div v-if="loading" class="h-72 animate-pulse rounded-3xl bg-white shadow-sm" role="status">Đang tải chủ đề...</div>
    <div v-else-if="errorMessage" class="rounded-3xl border border-rose-100 bg-white p-8 text-center shadow-sm" role="alert">
      <p class="text-lg font-extrabold text-kids-text">Chưa mở được chủ đề</p><p class="mt-2 text-sm text-slate-500">{{ errorMessage }}</p>
      <RouterLink :to="{ name: 'StudentTopics' }" class="mt-5 inline-flex rounded-xl bg-kids-primary px-4 py-2.5 text-sm font-bold text-kids-text">Quay lại danh sách</RouterLink>
    </div>

    <template v-else-if="topic && topicProgress">
      <article class="overflow-hidden rounded-3xl border border-amber-100 bg-white shadow-sm">
        <div class="grid md:grid-cols-[minmax(240px,0.8fr)_minmax(0,1.2fr)]">
          <div class="min-h-56 bg-kids-bg md:min-h-full"><img :src="topic.image" :alt="topic.imageAlt" class="h-full max-h-80 w-full object-cover md:max-h-full" /></div>
          <div class="p-5 sm:p-7 lg:p-9">
            <div class="flex flex-wrap gap-2"><span class="rounded-full bg-amber-50 px-3 py-1 text-xs font-bold text-amber-800">{{ topic.level }}</span><span class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-700">Đã xuất bản</span><span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold text-slate-600">{{ topic.id }}</span></div>
            <h2 class="mt-4 text-2xl font-extrabold text-kids-text sm:text-3xl">{{ topic.title }}</h2>
            <p class="mt-3 text-sm leading-6 text-slate-600">{{ topic.description }}</p>
            <div class="mt-5 flex flex-wrap gap-x-5 gap-y-2 text-xs font-semibold text-slate-500"><span>{{ topic.wordCount }} từ vựng</span><span>{{ topic.progress.completed }} từ đã luyện</span><span>{{ topic.progress.progress }}% tiến độ</span></div>
            <div class="mt-3 h-2.5 overflow-hidden rounded-full bg-slate-100" role="progressbar" :aria-valuenow="topic.progress.progress" aria-valuemin="0" aria-valuemax="100" :aria-label="`Tiến độ ${topic.title}`"><div class="h-full rounded-full bg-gradient-to-r from-kids-primary to-kids-cta" :style="{ width: `${topic.progress.progress}%` }"></div></div>
            <p v-if="updateError" class="mt-3 text-xs text-rose-600" role="alert">{{ updateError }}</p>
            <div class="mt-5 flex flex-wrap gap-2">
              <button type="button" class="inline-flex min-h-11 items-center gap-2 rounded-xl bg-kids-cta px-4 text-sm font-extrabold text-white transition hover:bg-orange-600 disabled:opacity-50" :disabled="!nextWord" @click="startLearning()"><AdminIcon name="play" :size="16" />{{ topic.progress.status === 'not-started' ? 'Bắt đầu học' : topic.progress.status === 'completed' ? 'Ôn tập chủ đề' : 'Tiếp tục học' }}</button>
              <button type="button" class="inline-flex min-h-11 items-center gap-2 rounded-xl border px-3 text-xs font-bold transition" :class="topic.isFavorite ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-slate-200 text-slate-600 hover:bg-rose-50'" :aria-pressed="topic.isFavorite" @click="updateFlag('favorites')"><AdminIcon name="heart" :size="16" />{{ topic.isFavorite ? 'Đã yêu thích' : 'Yêu thích' }}</button>
              <button type="button" class="inline-flex min-h-11 items-center gap-2 rounded-xl border px-3 text-xs font-bold transition" :class="topic.isStarred ? 'border-amber-200 bg-amber-50 text-amber-800' : 'border-slate-200 text-slate-600 hover:bg-amber-50'" :aria-pressed="topic.isStarred" @click="updateFlag('starred')"><AdminIcon name="star" :size="16" />{{ topic.isStarred ? 'Đã ưu tiên' : 'Đánh dấu sao' }}</button>
            </div>
          </div>
        </div>
      </article>

      <section aria-labelledby="vocabulary-heading">
        <div class="mb-4 flex flex-wrap items-end justify-between gap-3"><div><p class="text-xs font-bold uppercase tracking-wider text-sky-700">Học từng từ một</p><h3 id="vocabulary-heading" class="mt-1 text-xl font-extrabold text-kids-text">Từ vựng trong chủ đề</h3></div><span class="text-xs text-slate-400">{{ topic.words.length }} từ</span></div>
        <div v-if="topic.words.length" class="space-y-3">
          <StudentVocabularyCard v-for="(word, index) in topic.words" :key="word.id" :word="word" :number="index + 1" :completed="topicProgress.completedWordIds.includes(word.id)" :score="topicProgress.latestIllustrativeScore?.wordId === word.id ? topicProgress.latestIllustrativeScore.score : null" @practice="startLearning" />
        </div>
        <div v-else class="rounded-2xl border border-dashed border-amber-200 bg-white p-8 text-center text-sm text-slate-500">Chủ đề chưa có từ vựng. Con quay lại sau nhé!</div>
      </section>
      <p class="pb-2 text-center text-[11px] text-slate-400">Nội dung học minh họa · Chưa kết nối máy chủ hoặc chấm điểm AI</p>
    </template>
  </section>
</template>
