<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import AdminHeader from '../components/admin/AdminHeader.vue'
import AdminSidebar from '../components/admin/AdminSidebar.vue'

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
  </div>
</template>
