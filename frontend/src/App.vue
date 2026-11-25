<script setup>
import { onMounted, onUnmounted } from 'vue'
import ToastContainer from './components/common/toast/ToastContainer.vue'
import { toast } from './composable/useToast'

function showForbidden(event) {
  toast.error('Không có quyền', event.detail?.message || 'Bạn không có quyền thực hiện thao tác này.')
}

function showAccountDisabled(event) {
  toast.error('Tài khoản đã bị khóa', event.detail?.message || 'Tài khoản của quý khách đã bị khóa! Vui lòng liên hệ bộ phận hỗ trợ để được giải quyết.')
}

onMounted(() => window.addEventListener('kidspeak:api-forbidden', showForbidden))
onMounted(() => window.addEventListener('kidspeak:account-disabled', showAccountDisabled))
onUnmounted(() => {
  window.removeEventListener('kidspeak:api-forbidden', showForbidden)
  window.removeEventListener('kidspeak:account-disabled', showAccountDisabled)
})
</script>

<template>
  <RouterView />
  <ToastContainer />
</template>
