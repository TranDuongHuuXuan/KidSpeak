<script setup>
import AdminIcon from './AdminIcon.vue'

defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, required: true },
  size: { type: String, default: 'max-w-xl' },
})

const emit = defineEmits(['update:modelValue', 'submit'])
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4" @click.self="emit('update:modelValue', false)" @keydown.esc="emit('update:modelValue', false)">
      <section role="dialog" aria-modal="true" :aria-label="title" class="max-h-[90vh] w-full overflow-y-auto rounded-2xl bg-white shadow-2xl" :class="size">
        <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-100 bg-white px-6 py-4">
          <h2 class="text-lg font-bold text-slate-800">{{ title }}</h2>
          <button type="button" class="rounded-lg p-2 text-slate-500 hover:bg-slate-100" aria-label="Đóng" @click="emit('update:modelValue', false)">
            <AdminIcon name="close" :size="18" />
          </button>
        </header>
        <form @submit.prevent="emit('submit')">
          <div class="p-6"><slot /></div>
          <footer class="flex justify-end gap-3 border-t border-slate-100 px-6 py-4">
            <button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="emit('update:modelValue', false)">Hủy</button>
            <slot name="actions">
              <button type="submit" class="rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700">Lưu thay đổi</button>
            </slot>
          </footer>
        </form>
      </section>
    </div>
  </Teleport>
</template>
