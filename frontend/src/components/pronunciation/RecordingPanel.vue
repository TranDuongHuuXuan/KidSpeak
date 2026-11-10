<script setup>
import { computed } from 'vue'
import AdminIcon from '../admin/AdminIcon.vue'

const props = defineProps({
  isRequesting: { type: Boolean, default: false },
  isRecording: { type: Boolean, default: false },
  isPlaying: { type: Boolean, default: false },
  hasRecording: { type: Boolean, default: false },
  confirmed: { type: Boolean, default: false },
  duration: { type: Number, default: 0 },
  errorMessage: { type: String, default: '' },
})

const emit = defineEmits(['start', 'stop', 'play', 'retake', 'confirm'])
const stateLabel = computed(() => {
  if (props.confirmed) return 'Đã xác nhận · kết quả minh họa'
  if (props.isRequesting) return 'Đang yêu cầu quyền microphone'
  if (props.isRecording) return 'Đang ghi âm'
  if (props.isPlaying) return 'Đang phát lại'
  if (props.hasRecording) return 'Đã ghi âm · chưa xác nhận'
  return 'Chưa ghi âm'
})

function formatDuration(seconds) {
  return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`
}
</script>

<template>
  <section class="rounded-3xl border border-orange-100 bg-white p-5 shadow-sm sm:p-6" aria-labelledby="recording-panel-heading">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div><p class="text-xs font-extrabold uppercase tracking-wider text-kids-cta">Danh mục 3</p><h2 id="recording-panel-heading" class="mt-1 text-lg font-extrabold text-kids-text">Ghi âm giọng nói</h2></div>
      <span class="inline-flex items-center gap-2 rounded-full bg-kids-bg px-3 py-1.5 text-[11px] font-bold text-slate-600" role="status" aria-live="polite">
        <span class="h-2 w-2 rounded-full" :class="isRecording ? 'animate-pulse bg-rose-500' : confirmed ? 'bg-emerald-500' : 'bg-slate-300'"></span>{{ stateLabel }}
      </span>
    </div>
    <p class="mt-2 text-xs leading-5 text-slate-500">Bản ghi được xử lý trong trình duyệt này; không tải lên hoặc gửi tới máy chủ.</p>

    <div v-if="isRecording" class="mt-5 flex h-14 items-center justify-center gap-1.5" role="img" aria-label="Đang ghi âm">
      <span v-for="bar in 21" :key="bar" class="w-1.5 animate-pulse rounded-full bg-rose-400" :style="{ height: `${12 + ((bar * 17) % 34)}px`, animationDelay: `${bar * 35}ms` }"></span>
    </div>
    <div v-if="isRecording || hasRecording" class="mt-3 text-center font-mono text-lg font-bold tabular-nums" :class="isRecording ? 'text-rose-600' : 'text-slate-500'" aria-live="off">{{ formatDuration(duration) }}</div>

    <div class="mt-4 flex flex-col gap-3 sm:flex-row">
      <button v-if="!isRecording" type="button" class="inline-flex min-h-14 flex-1 items-center justify-center gap-2 rounded-2xl bg-kids-cta px-4 text-sm font-extrabold text-white shadow-sm transition hover:bg-orange-600 disabled:cursor-not-allowed disabled:opacity-50" :disabled="isRequesting || confirmed" :aria-busy="isRequesting" @click="emit('start')">
        <AdminIcon name="microphone" :size="19" />{{ isRequesting ? 'Đang kết nối microphone...' : hasRecording ? 'Ghi âm lại' : 'Bắt đầu ghi âm' }}
      </button>
      <button v-else type="button" class="inline-flex min-h-14 flex-1 items-center justify-center gap-2 rounded-2xl bg-rose-600 px-4 text-sm font-extrabold text-white transition hover:bg-rose-700" @click="emit('stop')"><span class="h-4 w-4 rounded-sm bg-white"></span>Dừng ghi âm</button>
      <button v-if="hasRecording && !isRecording" type="button" class="inline-flex min-h-14 items-center justify-center gap-2 rounded-2xl border border-slate-200 px-4 text-sm font-bold text-slate-700 transition hover:bg-slate-50 disabled:opacity-50" :disabled="isPlaying" @click="emit('play')"><AdminIcon name="play" :size="17" />{{ isPlaying ? 'Đang phát...' : 'Nghe lại bản ghi' }}</button>
      <button v-if="hasRecording && !isRecording && !confirmed" type="button" class="inline-flex min-h-14 items-center justify-center gap-2 rounded-2xl border border-slate-200 px-4 text-sm font-bold text-slate-700 transition hover:bg-slate-50" @click="emit('retake')"><AdminIcon name="close" :size="16" />Ghi âm lại</button>
    </div>
    <p v-if="errorMessage" class="mt-3 rounded-xl bg-rose-50 px-4 py-3 text-xs leading-5 text-rose-700" role="alert">{{ errorMessage }}</p>
    <p v-if="hasRecording && !confirmed" class="mt-3 rounded-xl bg-emerald-50 px-4 py-3 text-xs leading-5 text-emerald-800">Bản ghi đã sẵn sàng trên thiết bị. Nghe lại trước khi xác nhận nhé.</p>
    <p v-if="confirmed" class="mt-3 rounded-xl bg-emerald-50 px-4 py-3 text-xs leading-5 text-emerald-800" role="status">Con đã xác nhận bản ghi. Chỉ dữ liệu kết quả minh họa được lưu; tệp âm thanh không được gửi đi.</p>
    <button type="button" class="mt-4 min-h-12 w-full rounded-xl bg-kids-secondary/30 px-4 text-sm font-extrabold text-kids-text transition hover:bg-kids-secondary/50 disabled:cursor-not-allowed disabled:opacity-45" :disabled="!hasRecording || isRecording || isRequesting || confirmed" @click="emit('confirm')">Xác nhận bản ghi và xem kết quả minh họa</button>
  </section>
</template>
