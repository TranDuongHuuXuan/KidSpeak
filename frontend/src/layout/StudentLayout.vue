<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from '../components/admin/AdminIcon.vue'
import StudentHeader from '../components/student/StudentHeader.vue'
import StudentSidebar from '../components/student/StudentSidebar.vue'
import { consumeFlashToast } from '../services/flashToast'

const route = useRoute()
const mobileOpen = ref(false)
const collapsed = ref(false)
const successToast = ref('')
let successToastTimer
const title = computed(() => route.meta.title || 'Tổng quan')

onMounted(() => {
  document.documentElement.setAttribute('data-theme', 'student')
  successToast.value = consumeFlashToast() || ''
  if (successToast.value) {
    successToastTimer = setTimeout(() => {
      successToast.value = ''
    }, 4000)
  }
})

onUnmounted(() => {
  document.documentElement.removeAttribute('data-theme')
  clearTimeout(successToastTimer)
})
</script>

<template>
  <div class="flex h-dvh overflow-hidden bg-kids-bg font-sans text-kids-text" style="--font-sans: 'Be Vietnam Pro', Arial, sans-serif">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-2 opacity-0"
    >
      <div
        v-if="successToast"
        class="fixed right-4 top-4 z-50 flex max-w-sm items-start gap-3 rounded-2xl border border-feedback-success/30 bg-kids-surface p-4 text-kids-text shadow-xl sm:right-6 sm:top-6"
        role="status"
        aria-live="polite"
      >
        <span class="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-feedback-success/15 text-feedback-success" aria-hidden="true">✓</span>
        <p class="flex-1 text-sm font-semibold">{{ successToast }}</p>
        <button
          type="button"
          class="rounded-lg px-1 text-lg leading-none text-kids-text/60 hover:text-kids-text"
          aria-label="Đóng thông báo"
          @click="successToast = ''"
        >&times;</button>
      </div>
    </Transition>
    <StudentSidebar
      :mobile-open="mobileOpen"
      :collapsed="collapsed"
      @close="mobileOpen = false"
      @navigate="mobileOpen = false"
      @toggle-collapse="collapsed = !collapsed"
    />
    <main class="flex min-w-0 flex-1 flex-col overflow-hidden">
      <StudentHeader :title="title" @toggle-menu="mobileOpen = !mobileOpen" />
      <div class="min-h-0 flex-1 overflow-y-auto">
        <RouterView />
      </div>
    </main>
  </div>
</template>
