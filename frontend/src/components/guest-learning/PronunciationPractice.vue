<script setup>
import { computed, ref, watch } from 'vue'
import { useAudioRecorder } from '../../composable/useAudioRecorder'
import PronunciationGuide from './PronunciationGuide.vue'
import PronunciationResult from './PronunciationResult.vue'
import TopicHeader from './TopicHeader.vue'
import WordNavigation from './WordNavigation.vue'

const props = defineProps({
  topic: {
    type: Object,
    required: true,
  },
})

const currentIndex = ref(0)
const result = ref(null)
const practicedIds = ref(new Set())
const currentWord = computed(() => props.topic.words[currentIndex.value])
const practicedCount = computed(() => practicedIds.value.size)
const {
  isRequesting,
  isRecording,
  isPlaying,
  duration,
  hasRecording,
  errorMessage,
  startRecording,
  stopRecording,
  playRecording,
  reset: resetRecording,
} = useAudioRecorder()

watch(currentWord, () => {
  result.value = null
  resetRecording()
})

function formatDuration(seconds) {
  return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`
}

function evaluateRecording() {
  if (!hasRecording.value) return
  result.value = currentWord.value.mockScore
  practicedIds.value = new Set(practicedIds.value).add(currentWord.value.id)
}

function retryWord() {
  result.value = null
  resetRecording()
}

function nextWord() {
  currentIndex.value = (currentIndex.value + 1) % props.topic.words.length
}
</script>

<template>
  <div class="bg-kids-bg px-4 py-6 sm:px-8 sm:py-8 lg:px-12">
    <div class="mx-auto max-w-screen-2xl">
      <TopicHeader
        :topic="topic"
        :current-index="currentIndex"
        :total-words="topic.words.length"
        :practiced-count="practicedCount"
      />

      <div class="mt-6 grid items-start gap-5 lg:grid-cols-[minmax(0,1.15fr)_minmax(340px,0.85fr)]">
        <section class="rounded-3xl border border-kids-text/10 bg-white p-5 shadow-sm sm:p-7" aria-labelledby="practice-word">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <p class="text-xs font-bold uppercase tracking-[0.12em] text-kids-secondary">Bé thử đọc từ này</p>
            <span class="rounded-full px-3 py-1 text-xs font-bold" :class="isRecording ? 'bg-feedback-error/10 text-feedback-error' : 'bg-kids-bg text-kids-text/65'">
              <span v-if="isRecording" class="mr-1 inline-block h-2 w-2 animate-pulse rounded-full bg-feedback-error" aria-hidden="true"></span>
              {{ isRecording ? 'Đang ghi âm' : hasRecording ? 'Đã có bản ghi' : 'Sẵn sàng luyện tập' }}
            </span>
          </div>

          <div class="mt-5 grid items-center gap-5 sm:grid-cols-[0.9fr_1.1fr]">
            <div class="flex h-48 items-center justify-center rounded-2xl p-4 sm:h-56" :class="topic.colorClass">
              <img :src="currentWord.image" :alt="currentWord.imageAlt" class="h-full w-full object-contain" />
            </div>
            <div class="text-center sm:text-left">
              <p class="text-sm font-semibold text-kids-text/60">Từ vựng {{ String(currentIndex + 1).padStart(2, '0') }}</p>
              <h2 id="practice-word" class="mt-2 text-5xl font-extrabold capitalize text-kids-text sm:text-6xl">{{ currentWord.word }}</h2>
              <p class="mt-2 text-xs leading-5 text-kids-text/55">
                Hình minh họa thuộc chủ đề {{ topic.title }}, không phải ảnh cụ thể của từ này.
              </p>
              <button
                type="button"
                disabled
                class="mt-4 inline-flex min-h-11 cursor-not-allowed items-center gap-2 rounded-xl border border-kids-text/10 px-4 text-sm font-semibold text-kids-text/55"
                aria-label="Âm thanh mẫu đang được cập nhật"
                title="Chưa có file âm thanh mẫu"
              >
                <svg viewBox="0 0 20 20" class="h-5 w-5 fill-none stroke-current" stroke-width="1.7" aria-hidden="true">
                  <path d="M3 8v4h3l4 3V5L6 8H3Zm10-1a4 4 0 0 1 0 6m2-8a7 7 0 0 1 0 10" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                Âm thanh mẫu đang cập nhật
              </button>
            </div>
          </div>

          <div class="mt-6 rounded-2xl bg-kids-bg/70 p-4">
            <div class="flex items-center justify-between gap-3">
              <div>
                <p class="text-sm font-bold text-kids-text">Bé đọc từ “{{ currentWord.word }}”</p>
                <p class="mt-1 text-xs text-kids-text/60">
                  {{ isRecording ? 'Hãy đọc tự nhiên. Nhấn dừng khi bé đã đọc xong.' : 'Nhấn nút lớn để bắt đầu khi bé đã sẵn sàng.' }}
                </p>
              </div>
              <span v-if="isRecording" class="font-mono text-lg font-bold tabular-nums text-feedback-error" aria-live="off">
                {{ formatDuration(duration) }}
              </span>
              <span v-else-if="hasRecording" class="font-mono text-sm font-bold tabular-nums text-kids-text/65">
                {{ formatDuration(duration) }}
              </span>
            </div>

            <div class="mt-4 flex flex-wrap gap-3">
              <button
                v-if="!isRecording"
                type="button"
                class="inline-flex min-h-14 flex-1 items-center justify-center gap-2 rounded-2xl bg-kids-cta px-5 text-base font-extrabold text-white shadow-sm transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-cta/30 disabled:cursor-not-allowed disabled:opacity-70"
                :disabled="isRequesting"
                :aria-busy="isRequesting"
                @click="startRecording"
              >
                <svg v-if="!isRequesting" viewBox="0 0 20 20" class="h-6 w-6 fill-current" aria-hidden="true">
                  <path d="M10 13a3 3 0 0 0 3-3V5a3 3 0 1 0-6 0v5a3 3 0 0 0 3 3Zm5-3a1 1 0 1 1 2 0 7 7 0 0 1-6 6.93V19h3a1 1 0 1 1 0 2H6a1 1 0 1 1 0-2h3v-2.07A7 7 0 0 1 3 10a1 1 0 1 1 2 0 5 5 0 0 0 10 0Z" transform="translate(0 -1)" />
                </svg>
                {{ isRequesting ? 'Đang kết nối microphone...' : 'Bắt đầu ghi âm' }}
              </button>
              <button
                v-else
                type="button"
                class="inline-flex min-h-14 flex-1 items-center justify-center gap-2 rounded-2xl bg-feedback-error px-5 text-base font-extrabold text-white shadow-sm transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-feedback-error/30"
                @click="stopRecording"
              >
                <span class="h-4 w-4 rounded-sm bg-white" aria-hidden="true"></span>
                Dừng ghi âm
              </button>

              <button
                v-if="hasRecording && !isRecording"
                type="button"
                class="inline-flex min-h-14 items-center justify-center gap-2 rounded-2xl border border-kids-text/15 bg-white px-5 text-sm font-bold text-kids-text transition hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/30"
                @click="playRecording"
              >
                {{ isPlaying ? 'Đang phát...' : 'Nghe lại' }}
              </button>
              <button
                v-if="hasRecording && !isRecording"
                type="button"
                class="inline-flex min-h-14 items-center justify-center rounded-2xl border border-kids-text/15 bg-white px-5 text-sm font-bold text-kids-text transition hover:bg-kids-bg focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/30"
                @click="retryWord"
              >
                Ghi âm lại
              </button>
            </div>

            <p v-if="errorMessage" class="mt-3 rounded-xl bg-feedback-error/10 px-4 py-3 text-sm leading-6 text-feedback-error" role="alert">
              {{ errorMessage }}
            </p>

            <button
              type="button"
              class="mt-4 min-h-12 w-full rounded-xl bg-kids-secondary px-5 text-sm font-extrabold text-kids-text transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40 disabled:cursor-not-allowed disabled:opacity-45"
              :disabled="!hasRecording || isRecording || isRequesting"
              @click="evaluateRecording"
            >
              Chấm điểm mô phỏng
            </button>
          </div>
        </section>

        <PronunciationGuide :word="currentWord" />
      </div>

      <div class="mt-5">
        <PronunciationResult
          v-if="result !== null"
          :score="result"
          :word="currentWord.word"
          @retry="retryWord"
          @next="nextWord"
        />
      </div>

      <div class="mt-5">
        <WordNavigation
          :words="topic.words"
          :current-index="currentIndex"
          :practiced-ids="[...practicedIds]"
          @select="currentIndex = $event"
          @previous="currentIndex = Math.max(0, currentIndex - 1)"
          @next="currentIndex = Math.min(topic.words.length - 1, currentIndex + 1)"
        />
      </div>
    </div>
  </div>
</template>
