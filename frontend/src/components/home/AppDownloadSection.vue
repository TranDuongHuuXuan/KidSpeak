<script setup>
import appIllustration from '../../assets/images/home/auto-kidspeak.svg'

const platforms = [
  { name: 'App Store', mark: 'A', label: 'Sắp ra mắt' },
  { name: 'Google Play', mark: '▶', label: 'Sắp ra mắt' },
]
</script>

<template>
  <section class="bg-kids-secondary/10 py-16 sm:py-20 lg:py-24">
    <div class="mx-auto grid max-w-screen-2xl items-center gap-10 px-5 sm:px-8 lg:grid-cols-2 lg:gap-16 lg:px-12">
      <div>
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">
          KIDSPEAK MOBILE APP
        </p>
        <h2 class="mt-3 text-3xl font-extrabold leading-tight text-kids-text sm:text-4xl">
          KidSpeak – Người bạn đồng hành trong hành trình luyện phát âm của bé.
        </h2>
        <p class="mt-5 max-w-xl text-base leading-7 text-kids-text/75">
          Trải nghiệm luyện phát âm mọi lúc, mọi nơi với các bài tập tương tác và công nghệ AI hỗ trợ phân tích giọng nói.
        </p>

        <div class="mt-7 grid max-w-xl gap-3 sm:grid-cols-2">
          <button
            v-for="platform in platforms"
            :key="platform.name"
            type="button"
            disabled
            class="flex min-h-[72px] items-center gap-3 rounded-2xl border border-kids-text/10 bg-kids-surface px-4 py-3 text-left opacity-80"
            :aria-label="`${platform.name}: ${platform.label}`"
          >
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-kids-secondary/15 text-lg font-bold text-kids-text" aria-hidden="true">
              {{ platform.mark }}
            </span>
            <span class="min-w-0">
              <span class="block text-sm font-bold text-kids-text">{{ platform.name }}</span>
              <span class="mt-0.5 block text-xs font-medium text-kids-text/60">{{ platform.label }}</span>
            </span>
          </button>
        </div>
        <p class="mt-3 text-xs text-kids-text/60">
          Liên kết tải ứng dụng sẽ được cập nhật khi có phiên bản phát hành chính thức.
        </p>
      </div>

      <div class="mx-auto flex min-h-72 w-full max-w-xl items-center justify-center rounded-[2rem] bg-white p-5 shadow-sm sm:min-h-[26rem] sm:p-8">
        <img
          :src="appIllustration"
          alt="Minh họa KidSpeak trên thiết bị di động, không phải ảnh chụp ứng dụng thực tế"
          class="h-auto max-h-[24rem] w-full object-contain"
          loading="lazy"
        />
      </div>
    </div>
  </section>
</template>
