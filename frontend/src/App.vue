<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const forbiddenMessage = ref('')
let forbiddenTimer

function showForbidden(event) {
  forbiddenMessage.value = event.detail?.message || 'Bạn không có quyền thực hiện thao tác này.'
  clearTimeout(forbiddenTimer)
  forbiddenTimer = setTimeout(() => {
    forbiddenMessage.value = ''
  }, 4000)
}

onMounted(() => window.addEventListener('kidspeak:api-forbidden', showForbidden))
onUnmounted(() => {
  window.removeEventListener('kidspeak:api-forbidden', showForbidden)
  clearTimeout(forbiddenTimer)
})
</script>

<template>
  <RouterView />
  <div v-if="forbiddenMessage" role="alert" class="fixed bottom-5 right-5 z-[100] max-w-sm rounded-xl bg-rose-700 px-4 py-3 text-sm font-semibold text-white shadow-xl">
    {{ forbiddenMessage }}
  </div>
</template>
