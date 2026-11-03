<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminHeader from '../components/admin/AdminHeader.vue'
import AdminIcon from '../components/admin/AdminIcon.vue'
import AdminSidebar from '../components/admin/AdminSidebar.vue'
import { toastMessage } from '../data/adminMockData'

const route = useRoute()
const mobileOpen = ref(false)
const title = computed(() => route.meta.title || 'Tổng quan')

onMounted(() => document.documentElement.setAttribute('data-theme', 'admin'))
onUnmounted(() => document.documentElement.removeAttribute('data-theme'))
</script>

<template>
  <div class="grid h-dvh overflow-hidden bg-slate-50 text-slate-700 lg:grid-cols-[20%_80%]">
    <AdminSidebar :mobile-open="mobileOpen" @close="mobileOpen = false" @navigate="mobileOpen = false" />
    <main class="flex min-w-0 flex-col overflow-hidden">
      <AdminHeader :title="title" @toggle-menu="mobileOpen = !mobileOpen" />
      <div class="min-h-0 flex-1 overflow-y-auto">
        <RouterView />
      </div>
    </main>
    <Transition enter-active-class="transition duration-200" enter-from-class="translate-y-2 opacity-0" leave-active-class="transition duration-150" leave-to-class="translate-y-2 opacity-0">
      <div v-if="toastMessage" role="status" class="fixed bottom-5 right-5 z-[60] flex max-w-[calc(100vw-2.5rem)] items-center gap-3 rounded-xl bg-slate-900 px-4 py-3 text-sm font-medium text-white shadow-xl">
        <span class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500"><AdminIcon name="check" :size="15" /></span>
        {{ toastMessage }}
      </div>
    </Transition>
  </div>
</template>
