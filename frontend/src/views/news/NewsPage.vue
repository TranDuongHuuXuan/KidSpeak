<script setup>
import { computed, ref, watch } from 'vue'
import AppHeader from '../../components/common/AppHeader.vue'
import Footer from '../../components/common/Footer.vue'
import FeaturedNews from '../../components/news/FeaturedNews.vue'
import NewsCard from '../../components/news/NewsCard.vue'
import NewsHero from '../../components/news/NewsHero.vue'
import NewsNewsletter from '../../components/news/NewsNewsletter.vue'
import NewsPagination from '../../components/news/NewsPagination.vue'
import NewsToolbar from '../../components/news/NewsToolbar.vue'
import { newsArticles, newsCategories } from '../../data/news'

const activeCategory = ref('Tất cả')
const search = ref('')
const currentPage = ref(1)
const pageSize = 6

const filteredArticles = computed(() => {
  const query = search.value.trim().toLocaleLowerCase('vi')
  return newsArticles.filter((article) => {
    const matchesCategory = activeCategory.value === 'Tất cả' || article.category === activeCategory.value
    const matchesSearch = !query || article.title.toLocaleLowerCase('vi').includes(query)
    return matchesCategory && matchesSearch
  })
})

const pageCount = computed(() => Math.max(1, Math.ceil(filteredArticles.value.length / pageSize)))
const visibleArticles = computed(() => filteredArticles.value.slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize))

watch([activeCategory, search], () => { currentPage.value = 1 })
watch(pageCount, (count) => { if (currentPage.value > count) currentPage.value = count })
</script>

<template>
  <div class="min-h-screen w-full overflow-x-clip bg-kids-bg">
    <AppHeader />
    <main>
      <NewsHero />
      <FeaturedNews :article="newsArticles[0]" />
      <NewsToolbar v-model:active-category="activeCategory" v-model:search="search" :categories="newsCategories" />

      <section id="news-list" class="mx-auto max-w-screen-xl scroll-mt-24 px-5 pb-12 pt-6 sm:px-8 sm:pb-16">
        <div class="mb-5 flex flex-wrap items-end justify-between gap-3">
          <div><p class="text-xs font-bold uppercase tracking-[0.14em] text-kids-text/50">Cùng khám phá</p><h2 class="mt-1 text-2xl font-extrabold text-kids-text">Bài viết mới nhất</h2></div>
          <p class="text-sm text-kids-text/55">{{ filteredArticles.length }} bài viết</p>
        </div>
        <div v-if="visibleArticles.length" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <NewsCard v-for="article in visibleArticles" :key="article.id" :article="article" />
        </div>
        <div v-else class="rounded-3xl border border-dashed border-kids-text/20 bg-white px-5 py-16 text-center">
          <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-kids-secondary/15 text-2xl" aria-hidden="true">🔎</span>
          <h3 class="mt-4 text-lg font-bold text-kids-text">Chưa tìm thấy bài viết</h3>
          <p class="mt-2 text-sm text-kids-text/60">Hãy thử từ khóa khác hoặc chọn một danh mục khác.</p>
          <button type="button" class="mt-5 rounded-xl bg-kids-secondary/20 px-4 py-2 text-sm font-bold text-kids-text transition hover:bg-kids-secondary/35" @click="search = ''; activeCategory = 'Tất cả'">Xóa bộ lọc</button>
        </div>
        <NewsPagination v-model:current-page="currentPage" :page-count="pageCount" />
      </section>
      <NewsNewsletter />
    </main>
    <Footer />
  </div>
</template>
