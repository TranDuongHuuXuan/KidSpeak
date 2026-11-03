<script setup>
import { computed, ref, watch } from 'vue'
import { ArrowLeft, ArrowRight, Check, Clock3, Copy, Share2 } from '@lucide/vue'
import { RouterLink, useRoute } from 'vue-router'
import AppHeader from '../../components/common/AppHeader.vue'
import Footer from '../../components/common/Footer.vue'
import NewsCard from '../../components/news/NewsCard.vue'
import { formatNewsDate } from '../../components/news/newsFormat.js'
import { getNewsBySlug, newsArticles } from '../../data/news'

const route = useRoute()
const article = computed(() => getNewsBySlug(route.params.slug))
const shareStatus = ref('')
const relatedArticles = computed(() => {
  if (!article.value) return []
  const sameCategory = newsArticles.filter((item) => item.slug !== article.value.slug && item.category === article.value.category)
  const otherArticles = newsArticles.filter((item) => item.slug !== article.value.slug && item.category !== article.value.category)
  return [...sameCategory, ...otherArticles].slice(0, 3)
})

watch(() => route.params.slug, () => {
  shareStatus.value = ''
  window.scrollTo({ top: 0, behavior: 'instant' })
})

async function shareArticle() {
  const shareData = { title: article.value.title, text: article.value.excerpt, url: window.location.href }
  try {
    if (navigator.share) {
      await navigator.share(shareData)
      shareStatus.value = 'Đã mở tùy chọn chia sẻ.'
      return
    }
    if (!navigator.clipboard?.writeText) {
      shareStatus.value = 'Trình duyệt không hỗ trợ sao chép liên kết.'
      return
    }
    await navigator.clipboard.writeText(shareData.url)
    shareStatus.value = 'Đã sao chép liên kết bài viết.'
  } catch (error) {
    if (error.name !== 'AbortError') shareStatus.value = 'Không thể chia sẻ lúc này. Vui lòng thử lại.'
  }
}
</script>

<template>
  <div class="min-h-screen w-full overflow-x-clip bg-kids-bg">
    <AppHeader />
    <main>
      <div v-if="article">
        <div class="border-b border-kids-text/5 bg-white/70">
          <nav aria-label="Breadcrumb" class="mx-auto max-w-screen-xl px-5 py-4 text-sm sm:px-8">
            <ol class="flex flex-wrap items-center gap-2 text-kids-text/55">
              <li><RouterLink to="/" class="hover:text-kids-cta">Trang chủ</RouterLink></li><li aria-hidden="true">/</li>
              <li><RouterLink :to="{ name: 'News' }" class="hover:text-kids-cta">Tin tức</RouterLink></li><li aria-hidden="true">/</li>
              <li class="line-clamp-1 max-w-[50vw] font-semibold text-kids-text" aria-current="page">{{ article.title }}</li>
            </ol>
          </nav>
        </div>
        <article class="mx-auto max-w-4xl px-5 pb-12 pt-8 sm:px-8 sm:pt-12">
          <RouterLink :to="{ name: 'News' }" class="inline-flex items-center gap-2 rounded-lg text-sm font-semibold text-kids-text/65 transition hover:text-kids-cta focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-kids-secondary"><ArrowLeft :size="17" />Quay lại tin tức</RouterLink>
          <div class="mt-7"><span class="inline-flex rounded-full bg-kids-secondary/20 px-3 py-1.5 text-xs font-bold text-kids-text">{{ article.category }}</span>
            <h1 class="mt-4 text-3xl font-extrabold leading-tight tracking-tight text-kids-text sm:text-4xl lg:text-5xl">{{ article.title }}</h1>
            <p class="mt-4 text-base leading-7 text-kids-text/65 sm:text-lg">{{ article.excerpt }}</p>
            <div class="mt-6 flex flex-wrap items-center justify-between gap-4 border-y border-kids-text/10 py-4">
              <div><p class="text-sm font-bold text-kids-text">{{ article.author }}</p><p class="mt-1 text-xs text-kids-text/55">{{ formatNewsDate(article.publishedAt) }}</p></div>
              <div class="flex items-center gap-4"><span class="inline-flex items-center gap-1.5 text-xs text-kids-text/55"><Clock3 :size="15" />{{ article.readTime }} phút đọc</span><button type="button" class="inline-flex items-center gap-2 rounded-xl border border-kids-text/15 bg-white px-3.5 py-2 text-xs font-bold text-kids-text transition hover:border-kids-secondary hover:bg-kids-secondary/10" @click="shareArticle"><Share2 :size="15" />Chia sẻ</button></div>
            </div>
            <p v-if="shareStatus" role="status" class="mt-2 text-right text-xs text-kids-text/60">{{ shareStatus }}</p>
          </div>

          <figure class="mt-8 flex aspect-[16/9] items-center justify-center overflow-hidden rounded-3xl bg-white p-8 shadow-sm sm:mt-10 sm:p-12">
            <img :src="article.thumbnail" :alt="article.title" class="h-full w-full object-contain" />
          </figure>

          <div class="mx-auto mt-9 max-w-3xl space-y-6 text-base leading-8 text-kids-text/80 sm:mt-12 sm:text-lg sm:leading-9">
            <template v-for="(block, index) in article.content" :key="`${block.type}-${index}`">
              <h2 v-if="block.type === 'h2'" class="!mb-0 !mt-10 text-2xl font-extrabold leading-tight text-kids-text sm:text-3xl">{{ block.text }}</h2>
              <h3 v-else-if="block.type === 'h3'" class="!mb-0 !mt-7 text-xl font-bold leading-tight text-kids-text sm:text-2xl">{{ block.text }}</h3>
              <p v-else-if="block.type === 'paragraph'" class="!my-0">{{ block.text }}</p>
              <figure v-else-if="block.type === 'image'" class="!my-9 flex aspect-[16/9] items-center justify-center overflow-hidden rounded-2xl bg-white p-7 shadow-sm sm:p-10">
                <img :src="block.src" :alt="block.alt" loading="lazy" class="h-full w-full object-contain" />
                <figcaption class="sr-only">{{ block.alt }}</figcaption>
              </figure>
            </template>
          </div>

          <div class="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-kids-text/10 pt-6">
            <RouterLink :to="{ name: 'News' }" class="inline-flex items-center gap-2 rounded-xl border border-kids-text/15 bg-white px-4 py-2.5 text-sm font-bold text-kids-text transition hover:bg-kids-bg"><ArrowLeft :size="17" />Tất cả tin tức</RouterLink>
            <button type="button" class="inline-flex items-center gap-2 rounded-xl bg-kids-text px-4 py-2.5 text-sm font-bold text-white transition hover:bg-kids-text/85" @click="shareArticle"><Copy :size="16" />Chia sẻ bài viết</button>
          </div>
        </article>

        <section class="border-t border-kids-text/5 bg-white/60 py-12 sm:py-16">
          <div class="mx-auto max-w-screen-xl px-5 sm:px-8">
            <div class="mb-6 flex items-end justify-between gap-3"><div><p class="text-xs font-bold uppercase tracking-[0.14em] text-kids-cta">Đọc tiếp</p><h2 class="mt-1 text-2xl font-extrabold text-kids-text">Bài viết liên quan</h2></div><RouterLink :to="{ name: 'News' }" class="inline-flex items-center gap-1 text-sm font-bold text-kids-text hover:text-kids-cta">Tất cả bài viết <ArrowRight :size="16" /></RouterLink></div>
            <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3"><NewsCard v-for="related in relatedArticles" :key="related.id" :article="related" /></div>
          </div>
        </section>
      </div>
      <section v-else class="mx-auto max-w-3xl px-5 py-24 text-center sm:px-8">
        <span class="text-5xl" aria-hidden="true">📰</span><h1 class="mt-5 text-3xl font-extrabold text-kids-text">Không tìm thấy bài viết</h1><p class="mt-3 text-kids-text/65">Bài viết này có thể đã được chuyển hoặc không tồn tại.</p><RouterLink :to="{ name: 'News' }" class="mt-6 inline-flex items-center gap-2 rounded-xl bg-kids-secondary px-5 py-3 text-sm font-bold text-kids-text hover:brightness-95"><ArrowLeft :size="17" />Quay lại trang tin tức</RouterLink>
      </section>
    </main>
    <Footer />
  </div>
</template>
