<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const root = ref(null)
const isVisible = ref(false)
let observer

onMounted(() => {
  if (!('IntersectionObserver' in window)) {
    isVisible.value = true
    return
  }

  observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.disconnect()
      }
    },
    { threshold: 0.12 },
  )

  if (root.value) observer.observe(root.value)
})

onUnmounted(() => observer?.disconnect())
</script>

<template>
  <div ref="root" class="scroll-reveal" :class="{ 'scroll-reveal--visible': isVisible }">
    <slot />
  </div>
</template>

<style scoped>
.scroll-reveal {
  opacity: 0;
  transform: translateY(1rem);
  transition:
    opacity 500ms ease,
    transform 500ms ease;
}

.scroll-reveal--visible {
  opacity: 1;
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .scroll-reveal,
  .scroll-reveal--visible {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
