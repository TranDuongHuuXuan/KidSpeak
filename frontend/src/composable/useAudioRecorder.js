import { computed, onUnmounted, ref } from 'vue'

function getRecordingError(error) {
  if (error?.name === 'NotAllowedError' || error?.name === 'PermissionDeniedError') {
    return 'Bạn chưa cấp quyền microphone. Hãy cho phép truy cập micro trong trình duyệt rồi thử lại nhé.'
  }
  if (error?.name === 'NotFoundError' || error?.name === 'DevicesNotFoundError') {
    return 'Không tìm thấy microphone. Hãy kết nối hoặc bật micro trên thiết bị.'
  }
  if (error?.name === 'NotReadableError' || error?.name === 'TrackStartError') {
    return 'Microphone đang bận hoặc không thể sử dụng. Hãy đóng ứng dụng khác đang dùng micro rồi thử lại.'
  }
  if (error?.name === 'SecurityError') {
    return 'Trình duyệt không cho phép ghi âm trên kết nối này. Hãy dùng localhost hoặc HTTPS.'
  }
  return 'Không thể bắt đầu ghi âm. Hãy kiểm tra quyền truy cập và thử lại.'
}

export function useAudioRecorder() {
  const isRequesting = ref(false)
  const isRecording = ref(false)
  const isPlaying = ref(false)
  const duration = ref(0)
  const audioBlob = ref(null)
  const audioUrl = ref('')
  const errorMessage = ref('')
  const hasRecording = computed(() => Boolean(audioBlob.value && audioUrl.value))

  let mediaStream = null
  let recorder = null
  let playback = null
  let timer = null
  let recordingStartedAt = 0
  let discardOnStop = false
  let chunks = []
  let startRequestId = 0

  function clearTimer() {
    if (timer) {
      window.clearInterval(timer)
      timer = null
    }
  }

  function releaseStream() {
    mediaStream?.getTracks().forEach((track) => track.stop())
    mediaStream = null
  }

  function revokeRecordingUrl() {
    if (audioUrl.value) {
      URL.revokeObjectURL(audioUrl.value)
      audioUrl.value = ''
    }
  }

  function stopPlayback() {
    if (!playback) return
    playback.pause()
    playback.removeAttribute('src')
    playback.load()
    playback = null
    isPlaying.value = false
  }

  async function startRecording() {
    errorMessage.value = ''

    if (isRecording.value || isRequesting.value) return
    if (typeof MediaRecorder === 'undefined') {
      errorMessage.value = 'Trình duyệt này chưa hỗ trợ ghi âm. Hãy thử phiên bản Chrome, Edge hoặc Firefox mới hơn.'
      return
    }
    if (!navigator.mediaDevices?.getUserMedia) {
      errorMessage.value = 'Không thể truy cập microphone. Hãy mở trang qua localhost hoặc HTTPS.'
      return
    }

    reset()
    const requestId = ++startRequestId
    isRequesting.value = true

    try {
      const requestedStream = await navigator.mediaDevices.getUserMedia({ audio: true })
      if (requestId !== startRequestId) {
        requestedStream.getTracks().forEach((track) => track.stop())
        return
      }

      mediaStream = requestedStream
      recorder = new MediaRecorder(mediaStream)
      chunks = []
      discardOnStop = false

      recorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) chunks.push(event.data)
      })

      recorder.addEventListener('stop', () => {
        clearTimer()
        isRecording.value = false

        if (!discardOnStop && chunks.length > 0) {
          audioBlob.value = new Blob(chunks, {
            type: recorder?.mimeType || chunks[0].type || 'audio/webm',
          })
          audioUrl.value = URL.createObjectURL(audioBlob.value)
        }

        chunks = []
        recorder = null
        discardOnStop = false
        releaseStream()
      }, { once: true })

      recorder.addEventListener('error', () => {
        errorMessage.value = 'Đã xảy ra lỗi khi ghi âm. Hãy thử lại nhé.'
        clearTimer()
        isRequesting.value = false
        isRecording.value = false
        releaseStream()
        recorder = null
        chunks = []
      }, { once: true })

      recorder.start()
      isRequesting.value = false
      isRecording.value = true
      recordingStartedAt = Date.now()
      duration.value = 0
      timer = window.setInterval(() => {
        duration.value = Math.floor((Date.now() - recordingStartedAt) / 1000)
      }, 250)
    } catch (error) {
      if (requestId !== startRequestId) return
      clearTimer()
      isRequesting.value = false
      isRecording.value = false
      releaseStream()
      recorder = null
      errorMessage.value = getRecordingError(error)
    }
  }

  function stopRecording() {
    if (!recorder || recorder.state === 'inactive') return
    clearTimer()
    duration.value = Math.floor((Date.now() - recordingStartedAt) / 1000)
    try {
      recorder.stop()
    } catch {
      isRecording.value = false
      releaseStream()
      errorMessage.value = 'Không thể hoàn tất bản ghi. Hãy thử ghi âm lại nhé.'
    }
  }

  async function playRecording() {
    if (!audioUrl.value || isRecording.value) return
    errorMessage.value = ''
    stopPlayback()

    playback = new Audio(audioUrl.value)
    playback.addEventListener('ended', () => {
      isPlaying.value = false
      playback = null
    }, { once: true })
    playback.addEventListener('error', () => {
      isPlaying.value = false
      playback = null
      errorMessage.value = 'Không thể phát bản ghi này. Hãy ghi âm lại nhé.'
    }, { once: true })

    try {
      isPlaying.value = true
      await playback.play()
    } catch {
      isPlaying.value = false
      playback = null
      errorMessage.value = 'Không thể phát bản ghi này. Hãy thử lại nhé.'
    }
  }

  function reset() {
    startRequestId += 1
    isRequesting.value = false
    if (recorder && recorder.state !== 'inactive') {
      discardOnStop = true
      stopRecording()
    } else {
      releaseStream()
    }
    clearTimer()
    stopPlayback()
    revokeRecordingUrl()
    audioBlob.value = null
    duration.value = 0
    errorMessage.value = ''
    chunks = []
  }

  onUnmounted(() => {
    startRequestId += 1
    isRequesting.value = false
    if (recorder && recorder.state !== 'inactive') {
      discardOnStop = true
      stopRecording()
    }
    clearTimer()
    stopPlayback()
    releaseStream()
    revokeRecordingUrl()
  })

  return {
    isRequesting,
    isRecording,
    isPlaying,
    duration,
    audioUrl,
    hasRecording,
    errorMessage,
    startRecording,
    stopRecording,
    playRecording,
    reset,
  }
}
