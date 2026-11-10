<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from '../components/admin/AdminIcon.vue'
import StudentHeader from '../components/student/StudentHeader.vue'
import StudentSidebar from '../components/student/StudentSidebar.vue'

const route = useRoute()
const mobileOpen = ref(false)
const collapsed = ref(false)
const title = computed(() => route.meta.title || 'Tổng quan')

onMounted(() => document.documentElement.setAttribute('data-theme', 'student'))
onUnmounted(() => document.documentElement.removeAttribute('data-theme'))
</script>

<template>
  <div class="flex h-dvh overflow-hidden bg-kids-bg font-sans text-kids-text" style="--font-sans: 'Be Vietnam Pro', Arial, sans-serif">
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
