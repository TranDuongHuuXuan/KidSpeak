<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from '../components/admin/AdminIcon.vue'
import ExpertHeader from '../components/expert/ExpertHeader.vue'
import ExpertSidebar from '../components/expert/ExpertSidebar.vue'
import { expertToast } from '../data/expertMockData'

const route = useRoute()
const mobileOpen = ref(false)
const collapsed = ref(false)
const title = computed(() => route.meta.title || 'Tổng quan')

onMounted(() => document.documentElement.setAttribute('data-theme', 'expert'))
onUnmounted(() => document.documentElement.removeAttribute('data-theme'))
</script>

<template>
  <div class="flex h-dvh overflow-hidden bg-slate-50 text-slate-700">
    <ExpertSidebar
      :mobile-open="mobileOpen"
      :collapsed="collapsed"
      @close="mobileOpen = false"
      @navigate="mobileOpen = false"
      @toggle-collapse="collapsed = !collapsed"
    />
    <main class="flex min-w-0 flex-1 flex-col overflow-hidden">
      <ExpertHeader :title="title" @toggle-menu="mobileOpen = !mobileOpen" />
      <div class="min-h-0 flex-1 overflow-y-auto">
        <RouterView />
      </div>
    </main>
    <Transition enter-active-class="transition duration-200" enter-from-class="translate-y-2 opacity-0" leave-active-class="transition duration-150" leave-to-class="translate-y-2 opacity-0">
      <div v-if="expertToast.message" role="status" class="fixed bottom-5 right-5 z-[70] flex max-w-[calc(100vw-2.5rem)] items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-white shadow-xl" :class="expertToast.tone === 'error' ? 'bg-rose-700' : 'bg-slate-900'">
        <span class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500"><AdminIcon :name="expertToast.tone === 'error' ? 'close' : 'check'" :size="15" /></span>
        {{ expertToast.message }}
      </div>
    </Transition>
  </div>
</template>
