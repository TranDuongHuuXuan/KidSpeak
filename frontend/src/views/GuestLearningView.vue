<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import AppHeader from '../components/common/AppHeader.vue'
import Footer from '../components/common/Footer.vue'
import PronunciationPractice from '../components/guest-learning/PronunciationPractice.vue'
import TopicSelection from '../components/guest-learning/TopicSelection.vue'
import { getTopicBySlug } from '../data/learningTopics'

const route = useRoute()
const topicSlug = computed(() => route.params.topicSlug)
const topic = computed(() => (topicSlug.value ? getTopicBySlug(topicSlug.value) : null))
const isTopicNotFound = computed(() => Boolean(topicSlug.value) && !topic.value)
</script>

<template>
  <div class="min-h-screen w-full overflow-x-clip bg-kids-bg">
    <AppHeader />
    <main>
      <TopicSelection v-if="!topicSlug" />
      <PronunciationPractice v-else-if="topic" :key="topic.slug" :topic="topic" />
      <section v-else-if="isTopicNotFound" class="bg-kids-bg px-5 py-20 text-center sm:px-8">
        <div class="mx-auto max-w-xl rounded-3xl border border-kids-text/10 bg-white p-8 shadow-sm sm:p-12">
          <span class="text-5xl" aria-hidden="true">🔎</span>
          <h1 class="mt-5 text-3xl font-extrabold text-kids-text">Không tìm thấy chủ đề</h1>
          <p class="mt-3 text-sm leading-6 text-kids-text/70">
            Chủ đề này chưa có trong danh sách bài học. Bé có thể quay lại và chọn một chủ đề khác nhé.
          </p>
          <RouterLink
            :to="{ name: 'GuestLearning' }"
            class="mt-6 inline-flex min-h-12 items-center justify-center rounded-xl bg-kids-secondary px-6 text-sm font-bold text-kids-text transition hover:brightness-95"
          >
            Quay lại danh sách chủ đề
          </RouterLink>
        </div>
      </section>
    </main>
    <Footer />
  </div>
</template>
