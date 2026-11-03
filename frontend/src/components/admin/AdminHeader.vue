<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AdminIcon from './AdminIcon.vue'

defineProps({ title: { type: String, required: true } })
const emit = defineEmits(['toggle-menu'])
const route = useRoute()
const breadcrumb = computed(() => route.meta.title || 'Tổng quan')
</script>

<template>
  <header class="sticky top-0 z-20 flex min-h-[76px] items-center justify-between gap-4 border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-7 lg:px-9">
    <div class="flex min-w-0 items-center gap-3">
      <button type="button" class="rounded-xl border border-slate-200 p-2 text-slate-600 lg:hidden" aria-label="Mở menu" @click="emit('toggle-menu')"><AdminIcon name="menu" /></button>
      <div class="min-w-0">
        <div class="hidden items-center gap-2 text-xs text-slate-400 sm:flex"><span>Quản trị</span><AdminIcon name="arrow" :size="13" /><span class="truncate text-slate-500">{{ breadcrumb }}</span></div>
        <h1 class="truncate text-lg font-bold text-slate-800 sm:mt-1 sm:text-xl">{{ title }}</h1>
      </div>
    </div>
    <div class="flex shrink-0 items-center gap-3">
      <span class="hidden text-right sm:block"><span class="block text-sm font-semibold text-slate-700">Admin KidSpeak</span><span class="block text-xs text-slate-400">Quản trị viên</span></span>
      <div class="flex h-10 w-10 items-center justify-center rounded-full bg-amber-100 text-sm font-bold text-amber-800">AD</div>
    </div>
  </header>
</template>
