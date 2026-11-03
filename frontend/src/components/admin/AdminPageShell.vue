<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>

<template>
  <section class="space-y-6 p-4 sm:p-7 lg:p-9">
    <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
      <div>
        <p class="text-sm font-semibold text-admin-cta">KidSpeak Admin</p>
        <h2 class="mt-1 text-2xl font-extrabold tracking-tight text-slate-800 sm:text-3xl">{{ title }}</h2>
        <p v-if="description" class="mt-2 max-w-3xl text-sm leading-6 text-slate-500">{{ description }}</p>
      </div>
      <div v-if="$slots.actions" class="flex shrink-0 flex-wrap gap-2"><slot name="actions" /></div>
    </div>
    <slot />
  </section>
</template>
