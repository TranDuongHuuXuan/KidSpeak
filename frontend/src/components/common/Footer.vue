<script setup>
import { RouterLink } from 'vue-router'
import logo from '../../assets/logo_project.png'

const linkGroups = [
  {
    title: 'Khám phá',
    links: [
      { label: 'Giới thiệu', to: null },
      { label: 'Tính năng', to: null },
      { label: 'Hướng dẫn sử dụng', to: null },
      { label: 'Câu hỏi thường gặp', to: null },
    ],
  },
  {
    title: 'Hỗ trợ',
    links: [
      { label: 'Trung tâm trợ giúp', to: null },
      { label: 'Liên hệ', to: null },
      { label: 'Gửi phản hồi', to: null },
      { label: 'Báo lỗi', to: null },
    ],
  },
  {
    title: 'Dành cho phụ huynh',
    links: [
      { label: 'Hướng dẫn luyện tập', to: null },
      { label: 'Theo dõi tiến độ', to: null },
      { label: 'Chính sách bảo mật', to: null },
      { label: 'Điều khoản sử dụng', to: null },
    ],
  },
]

const socialLinks = [
  { label: 'Facebook', href: null, icon: 'facebook' },
  { label: 'YouTube', href: null, icon: 'youtube' },
  { label: 'Email', href: null, icon: 'email' },
]
</script>

<template>
  <footer class="border-t border-kids-text/10 bg-kids-bg text-kids-text">
    <div class="mx-auto w-full max-w-screen-2xl px-5 py-10 sm:px-8 sm:py-12">
      <div class="grid grid-cols-1 gap-9 sm:grid-cols-2 xl:grid-cols-4 xl:gap-10">
        <section class="sm:col-span-2 xl:col-span-1" aria-labelledby="footer-brand">
          <div class="flex items-center gap-3">
            <img :src="logo" alt="" class="h-11 w-11 shrink-0 object-contain" />
            <h2 id="footer-brand" class="text-xl font-extrabold tracking-tight">KidSpeak</h2>
          </div>
          <p class="mt-4 max-w-sm text-sm leading-6 text-kids-text/75">
            Đồng hành cùng trẻ trên hành trình phát triển ngôn ngữ và giao tiếp tự tin hơn mỗi ngày.
          </p>

          <div class="mt-5 flex items-center gap-2.5" aria-label="Mạng xã hội và email">
            <component
              :is="social.href ? 'a' : 'button'"
              v-for="social in socialLinks"
              :key="social.icon"
              :href="social.href || undefined"
              :type="social.href ? undefined : 'button'"
              :disabled="!social.href"
              :aria-label="social.label"
              :title="social.href ? social.label : `Liên kết ${social.label} chưa được cấu hình`"
              :target="social.href?.startsWith('http') ? '_blank' : undefined"
              :rel="social.href?.startsWith('http') ? 'noopener noreferrer' : undefined"
              class="flex h-10 w-10 items-center justify-center rounded-xl border border-kids-text/10 bg-kids-surface text-kids-text/75 transition duration-200 hover:-translate-y-0.5 hover:border-kids-secondary/50 hover:text-kids-secondary focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/30 disabled:cursor-not-allowed disabled:opacity-70"
            >
              <svg
                v-if="social.icon === 'facebook'"
                viewBox="0 0 24 24"
                class="h-5 w-5 fill-current"
                aria-hidden="true"
              >
                <path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3V10H7.3v3h2.8v8h3.4Z" />
              </svg>
              <svg
                v-else-if="social.icon === 'youtube'"
                viewBox="0 0 24 24"
                class="h-5 w-5 fill-current"
                aria-hidden="true"
              >
                <path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8ZM9.6 15.6V8.4l6.3 3.6-6.3 3.6Z" />
              </svg>
              <svg
                v-else
                viewBox="0 0 24 24"
                class="h-5 w-5 fill-none stroke-current"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <rect x="3" y="5" width="18" height="14" rx="2" />
                <path d="m3 7 9 6 9-6" />
              </svg>
            </component>
          </div>
        </section>

        <section v-for="group in linkGroups" :key="group.title">
          <h2 class="text-sm font-bold">{{ group.title }}</h2>
          <ul class="mt-4 flex flex-col gap-3">
            <li v-for="link in group.links" :key="link.label">
              <RouterLink
                v-if="link.to"
                :to="link.to"
                class="text-sm text-kids-text/75 transition-colors duration-200 hover:text-kids-secondary focus-visible:rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary"
              >
                {{ link.label }}
              </RouterLink>
              <span v-else class="text-sm text-kids-text/60" aria-disabled="true">
                {{ link.label }}
              </span>
            </li>
          </ul>
        </section>
      </div>

      <div class="mt-9 flex flex-col gap-3 border-t border-kids-text/10 pt-5 text-center sm:mt-10 sm:flex-row sm:items-center sm:justify-between sm:text-left">
        <p class="text-xs text-kids-text/65">
          © 2026 KidSpeak. All rights reserved.
        </p>
        <p class="text-xs leading-5 text-kids-text/65">
          Mỗi âm thanh nhỏ, một bước tiến lớn trên hành trình phát triển ngôn ngữ của trẻ.
        </p>
      </div>
    </div>
  </footer>
</template>
