<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import ExpertHeader from '../components/expert/ExpertHeader.vue'
import ExpertSidebar from '../components/expert/ExpertSidebar.vue'

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
  </div>
</template>
