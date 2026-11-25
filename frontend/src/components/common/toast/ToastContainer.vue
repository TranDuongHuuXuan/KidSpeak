<script setup>
import { nextTick, ref, watch } from 'vue'
import { CheckCircle2, CircleAlert, Info, TriangleAlert, X } from '@lucide/vue'
import { useToast } from '../../../composable/useToast'

const { toasts, confirmation, toast } = useToast()
const confirmButton = ref(null)
watch(confirmation, (value) => {
  if (value) nextTick(() => confirmButton.value?.focus())
})
const styles = {
  success: { icon: CheckCircle2, color: 'text-emerald-600', border: 'border-emerald-200', bar: 'bg-emerald-500', live: 'polite' },
  error: { icon: CircleAlert, color: 'text-rose-600', border: 'border-rose-200', bar: 'bg-rose-500', live: 'assertive' },
  warning: { icon: TriangleAlert, color: 'text-amber-600', border: 'border-amber-200', bar: 'bg-amber-500', live: 'polite' },
  info: { icon: Info, color: 'text-sky-600', border: 'border-sky-200', bar: 'bg-sky-500', live: 'polite' },
}
</script>

<template>
  <section class="pointer-events-none fixed right-3 top-3 z-[200] flex w-[calc(100%-1.5rem)] max-w-sm flex-col gap-3 sm:right-6 sm:top-6" aria-label="Thông báo">
    <TransitionGroup name="toast">
      <article v-for="item in toasts" :key="item.id" class="pointer-events-auto relative overflow-hidden rounded-2xl border bg-white p-4 pr-11 shadow-xl shadow-slate-900/10" :class="styles[item.type].border" :role="item.type === 'error' ? 'alert' : 'status'" :aria-live="styles[item.type].live">
        <div class="flex items-start gap-3">
          <component :is="styles[item.type].icon" :size="21" :stroke-width="2" class="mt-0.5 shrink-0" :class="styles[item.type].color" aria-hidden="true" />
          <div class="min-w-0 flex-1"><p class="text-sm font-bold text-slate-900">{{ item.title }}</p><p v-if="item.message" class="mt-1 whitespace-pre-line text-sm leading-5 text-slate-600">{{ item.message }}</p></div>
        </div>
        <button type="button" class="absolute right-3 top-3 rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700" aria-label="Đóng thông báo" @click="toast.dismiss(item.id)"><X :size="17" aria-hidden="true" /></button>
        <div v-if="item.duration > 0" class="toast-progress absolute inset-x-0 bottom-0 h-1 origin-left" :class="styles[item.type].bar" :style="{ animationDuration: `${item.duration}ms` }" />
      </article>
    </TransitionGroup>
  </section>
  <Transition name="confirm">
    <div v-if="confirmation" class="fixed inset-0 z-[220] flex items-center justify-center bg-slate-950/45 p-4 backdrop-blur-[2px]" @click.self="toast.resolveConfirmation(false)" @keydown.esc.stop.prevent="toast.resolveConfirmation(false)">
      <section class="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl sm:p-6" role="alertdialog" aria-modal="true" aria-labelledby="global-confirm-title" aria-describedby="global-confirm-message" tabindex="-1">
        <h2 id="global-confirm-title" class="text-base font-extrabold text-slate-900">{{ confirmation.title }}</h2>
        <p id="global-confirm-message" class="mt-2 whitespace-pre-line text-sm leading-6 text-slate-600">{{ confirmation.message }}</p>
        <div class="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
          <button type="button" class="min-h-10 rounded-xl border border-slate-200 px-4 text-sm font-bold text-slate-700 hover:bg-slate-50" @click="toast.resolveConfirmation(false)">{{ confirmation.cancelText }}</button>
          <button ref="confirmButton" type="button" class="min-h-10 rounded-xl px-4 text-sm font-bold text-white" :class="confirmation.tone === 'danger' ? 'bg-rose-600 hover:bg-rose-700' : 'bg-sky-700 hover:bg-sky-800'" @click="toast.resolveConfirmation(true)">{{ confirmation.confirmText }}</button>
        </div>
      </section>
    </div>
  </Transition>
</template>

<style scoped>
.toast-enter-active, .toast-leave-active, .toast-move { transition: opacity 180ms ease, transform 180ms ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translate3d(1rem, -0.5rem, 0); }
.toast-leave-active { position: absolute; right: 0; left: 0; }
.toast-progress { animation: toast-shrink linear forwards; }
.confirm-enter-active, .confirm-leave-active { transition: opacity 160ms ease; }
.confirm-enter-from, .confirm-leave-to { opacity: 0; }
@keyframes toast-shrink { from { transform: scaleX(1); } to { transform: scaleX(0); } }
@media (prefers-reduced-motion: reduce) { .toast-enter-active, .toast-leave-active, .toast-move { transition-duration: 1ms; } }
</style>
