<script setup>
import { ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import logo from '../../assets/logo_project.png'

const route = useRoute()
const mobileMenuOpen = ref(false)

const navigationItems = [
  { label: 'Thông tin', to: { path: '/about', hash: '#about' }, hash: '#about' },
  { label: 'Liên lạc', to: { path: '/', hash: '#contact' }, hash: '#contact' },
  { label: 'Nghiên cứu', to: { path: '/', hash: '#research' }, hash: '#research' },
  { label: 'Tin tức', to: { path: '/', hash: '#news' }, hash: '#news' },
  { label: 'Bắt đầu học', to: { name: 'Register' } },
]

watch(
  () => route.fullPath,
  () => {
    mobileMenuOpen.value = false
  },
)
</script>

<template>
  <header
    class="sticky top-0 z-50 border-b border-kids-text/10 bg-white/95 backdrop-blur"
    @keydown.esc="mobileMenuOpen = false"
  >
    <div class="mx-auto flex h-20 w-full max-w-screen-2xl items-center justify-between gap-4 px-4 sm:px-6 lg:grid lg:grid-cols-[1fr_auto_1fr] lg:px-8">
      <RouterLink
        to="/"
        class="flex shrink-0 items-center gap-2.5 rounded-lg text-kids-text outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
        aria-label="Kidspeak - Trang chủ"
        @click="mobileMenuOpen = false"
      >
        <img :src="logo" alt="" class="h-11 w-11 object-contain" />
        <span class="text-xl font-extrabold tracking-tight">Kidspeak</span>
      </RouterLink>

      <nav class="hidden items-center gap-4 md:flex lg:gap-7" aria-label="Điều hướng chính">
        <RouterLink
          v-for="item in navigationItems"
          :key="item.label"
          :to="item.to"
          class="group relative whitespace-nowrap py-2 text-sm font-semibold text-kids-text outline-none transition-colors duration-200 hover:text-kids-secondary focus-visible:rounded-sm focus-visible:ring-2 focus-visible:ring-kids-secondary sm:text-[15px]"
          :aria-current="item.hash && route.hash === item.hash ? 'location' : undefined"
        >
          {{ item.label }}
          <span
            class="absolute inset-x-0 bottom-0 h-0.5 origin-left scale-x-0 rounded-full bg-kids-secondary transition-transform duration-300 group-hover:scale-x-100 group-focus-visible:scale-x-100"
            :class="{ 'scale-x-100': item.hash && route.hash === item.hash }"
          ></span>
        </RouterLink>
      </nav>

      <div class="hidden items-center justify-end gap-3 md:flex lg:gap-5">
        <RouterLink
          to="/login"
          class="group relative whitespace-nowrap py-2 text-sm font-semibold text-kids-text outline-none transition-colors duration-200 hover:text-kids-secondary focus-visible:rounded-sm focus-visible:ring-2 focus-visible:ring-kids-secondary sm:text-[15px]"
        >
          Sign in
          <span class="absolute inset-x-0 bottom-0 h-0.5 origin-left scale-x-0 rounded-full bg-kids-secondary transition-transform duration-300 group-hover:scale-x-100 group-focus-visible:scale-x-100"></span>
        </RouterLink>

        <button
          type="button"
          class="flex h-11 w-11 items-center justify-center rounded-xl text-kids-text transition-colors duration-200 hover:bg-kids-secondary/15 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40 active:scale-95"
          aria-label="Tìm kiếm"
        >
          <svg
            viewBox="0 0 24 24"
            class="h-[22px] w-[22px] fill-none stroke-current"
            stroke-width="1.8"
            stroke-linecap="round"
            aria-hidden="true"
          >
            <circle cx="10.8" cy="10.8" r="6.8" />
            <path d="m16 16 4.2 4.2" />
          </svg>
        </button>

        <RouterLink
          :to="{ name: 'Register' }"
          class="inline-flex h-11 items-center justify-center whitespace-nowrap rounded-xl bg-kids-secondary px-5 text-sm font-semibold text-kids-text outline-none transition duration-200 hover:brightness-95 focus-visible:ring-4 focus-visible:ring-kids-secondary/40 active:scale-[0.98] sm:text-[15px]"
        >
          Bắt đầu học
        </RouterLink>
      </div>

      <button
        type="button"
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl text-kids-text transition-colors hover:bg-kids-secondary/15 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40 md:hidden"
        :aria-expanded="mobileMenuOpen"
        aria-controls="mobile-navigation"
        :aria-label="mobileMenuOpen ? 'Đóng menu' : 'Mở menu'"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <svg
          v-if="!mobileMenuOpen"
          viewBox="0 0 24 24"
          class="h-6 w-6 fill-none stroke-current"
          stroke-width="2"
          stroke-linecap="round"
          aria-hidden="true"
        >
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
        <svg
          v-else
          viewBox="0 0 24 24"
          class="h-6 w-6 fill-none stroke-current"
          stroke-width="2"
          stroke-linecap="round"
          aria-hidden="true"
        >
          <path d="m6 6 12 12M18 6 6 18" />
        </svg>
      </button>
    </div>

    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-2 opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        id="mobile-navigation"
        class="absolute inset-x-0 top-full border-b border-kids-text/10 bg-white px-5 pb-5 pt-2 shadow-lg md:hidden"
      >
        <nav class="flex flex-col" aria-label="Điều hướng di động">
          <RouterLink
            v-for="item in navigationItems"
            :key="item.label"
            :to="item.to"
            class="rounded-xl px-3 py-3 text-base font-semibold text-kids-text transition-colors hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary"
            :aria-current="item.hash && route.hash === item.hash ? 'location' : undefined"
          >
            {{ item.label }}
          </RouterLink>
        </nav>

        <div class="mt-3 flex items-center gap-3 border-t border-kids-text/10 pt-4">
          <RouterLink
            to="/login"
            class="flex h-11 flex-1 items-center justify-center rounded-xl border border-kids-text/15 px-4 text-sm font-semibold text-kids-text transition-colors hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
          >
            Sign in
          </RouterLink>
          <RouterLink
            :to="{ name: 'Register' }"
            class="flex h-11 flex-1 items-center justify-center rounded-xl bg-kids-secondary px-4 text-sm font-semibold text-kids-text transition hover:brightness-95 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40 active:scale-[0.98]"
          >
            Bắt đầu học
          </RouterLink>
        </div>

        <button
          type="button"
          class="mt-3 flex h-11 w-full items-center justify-center gap-2 rounded-xl text-sm font-medium text-kids-text transition-colors hover:bg-kids-secondary/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
          aria-label="Tìm kiếm"
        >
          <svg
            viewBox="0 0 24 24"
            class="h-5 w-5 fill-none stroke-current"
            stroke-width="1.8"
            stroke-linecap="round"
            aria-hidden="true"
          >
            <circle cx="10.8" cy="10.8" r="6.8" />
            <path d="m16 16 4.2 4.2" />
          </svg>
          Tìm kiếm
        </button>
      </div>
    </Transition>
  </header>
</template>
