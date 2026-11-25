<script setup>
import { onMounted, onUnmounted } from 'vue'
import ToastContainer from './components/common/toast/ToastContainer.vue'
import { toast } from './composable/useToast'

function showForbidden(event) {
  toast.error('Không có quyền', event.detail?.message || 'Bạn không có quyền thực hiện thao tác này.')
}

onMounted(() => window.addEventListener('kidspeak:api-forbidden', showForbidden))
onUnmounted(() => window.removeEventListener('kidspeak:api-forbidden', showForbidden))
</script>

<template>
  <RouterView />
  <ToastContainer />
</template>
