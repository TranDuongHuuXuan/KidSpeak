<script setup>
import { ArrowRight, CheckCircle2, Mail } from '@lucide/vue'
import { computed, ref } from 'vue'

const email = ref('')
const submitted = ref(false)
const attempted = ref(false)
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const emailValid = computed(() => emailPattern.test(email.value.trim()))

function subscribe() {
  attempted.value = true
  if (!emailValid.value) {
    submitted.value = false
    return
  }
  submitted.value = true
  email.value = ''
}
</script>

<template>
  <section class="mx-auto max-w-screen-xl px-5 py-12 sm:px-8 sm:py-16">
    <div class="relative overflow-hidden rounded-3xl bg-kids-text px-6 py-9 text-white sm:px-10 sm:py-12 lg:px-14">
      <span class="absolute -right-10 -top-20 h-64 w-64 rounded-full bg-kids-secondary/15 blur-2xl" aria-hidden="true"></span>
      <span class="absolute -bottom-28 left-1/3 h-56 w-56 rounded-full bg-kids-primary/15 blur-2xl" aria-hidden="true"></span>
      <div class="relative z-10 grid items-center gap-8 lg:grid-cols-[1fr_auto]">
        <div><span class="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-white/10"><Mail :size="21" /></span><h2 class="mt-4 max-w-2xl text-2xl font-extrabold leading-tight sm:text-3xl">Đừng bỏ lỡ những tin tức mới từ KidSpeak!</h2><p class="mt-3 max-w-2xl text-sm leading-6 text-white/70 sm:text-base">Đăng ký nhận thông tin mới nhất về kiến thức phát âm và các hoạt động từ KidSpeak.</p></div>
        <form class="w-full lg:w-[390px]" novalidate @submit.prevent="subscribe">
          <label for="newsletter-email" class="sr-only">Email của bạn</label>
          <div class="flex flex-col gap-2 rounded-2xl bg-white p-2 sm:flex-row">
            <input id="newsletter-email" v-model.trim="email" type="email" autocomplete="email" placeholder="Email của bạn" class="h-11 min-w-0 flex-1 rounded-xl px-3 text-sm text-kids-text outline-none placeholder:text-kids-text/45" :aria-invalid="attempted && !emailValid" aria-describedby="newsletter-message" @input="submitted = false" />
            <button type="submit" class="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-kids-secondary px-4 text-sm font-bold text-kids-text transition hover:brightness-95">Đăng ký <ArrowRight :size="17" /></button>
          </div>
          <p id="newsletter-message" class="mt-2 min-h-5 text-xs" :class="submitted ? 'text-emerald-300' : 'text-white/75'" aria-live="polite">
            <span v-if="submitted" class="inline-flex items-center gap-1"><CheckCircle2 :size="14" />Đăng ký thành công! Cảm ơn bạn.</span>
            <span v-else-if="attempted && !emailValid">Vui lòng nhập địa chỉ email hợp lệ.</span>
            <span v-else>Chúng tôi chỉ gửi những thông tin hữu ích đến bạn.</span>
          </p>
        </form>
      </div>
    </div>
  </section>
</template>
