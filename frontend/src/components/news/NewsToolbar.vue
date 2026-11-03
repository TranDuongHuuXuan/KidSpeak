<script setup>
import { Search, X } from '@lucide/vue'

defineProps({
  categories: { type: Array, required: true },
  activeCategory: { type: String, required: true },
  search: { type: String, required: true },
})

const emit = defineEmits(['update:activeCategory', 'update:search'])
</script>

<template>
  <section class="mx-auto max-w-screen-xl px-5 pt-10 sm:px-8 sm:pt-14">
    <div class="flex flex-col gap-5">
      <div class="-mx-1 flex gap-2 overflow-x-auto px-1 pb-2" role="tablist" aria-label="Lọc bài viết theo danh mục">
        <button
          v-for="category in categories"
          :key="category"
          type="button"
          role="tab"
          :aria-selected="activeCategory === category"
          class="shrink-0 rounded-full border px-4 py-2.5 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/30"
          :class="activeCategory === category ? 'border-kids-text bg-kids-text text-white shadow-sm' : 'border-kids-text/10 bg-white text-kids-text/70 hover:border-kids-secondary hover:bg-kids-secondary/10'"
          @click="emit('update:activeCategory', category)"
        >{{ category }}</button>
      </div>
      <label class="relative block w-full sm:max-w-sm">
        <Search :size="19" class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-kids-text/45" />
        <input
          :value="search"
          type="search"
          placeholder="Tìm theo tiêu đề bài viết..."
          class="h-12 w-full rounded-xl border border-kids-text/15 bg-white pl-11 pr-11 text-sm text-kids-text outline-none transition placeholder:text-kids-text/40 focus:border-kids-secondary focus:ring-4 focus:ring-kids-secondary/15"
          @input="emit('update:search', $event.target.value)"
        />
        <button v-if="search" type="button" class="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-lg text-kids-text/50 hover:bg-kids-bg hover:text-kids-text" aria-label="Xóa nội dung tìm kiếm" @click="emit('update:search', '')"><X :size="17" /></button>
      </label>
    </div>
  </section>
</template>
