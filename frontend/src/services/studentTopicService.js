import { learningTopics } from '../data/learningTopics'
import { studentLearningPaths, topicLevels } from '../data/studentTopicMockData'
import { getStudentProgress, getTopicProgress } from './studentProgressService'

const publicationDates = Object.fromEntries(learningTopics.map((topic, index) => [
  topic.slug,
  new Date(Date.UTC(2026, 9, 20 - index)).toISOString(),
]))

function normalizeTopic(topic, progressData) {
  const progress = getTopicProgress(topic.slug, topic.words.length)
  return {
    ...topic,
    id: `TOP-${String(topic.id).padStart(3, '0')}`,
    level: topicLevels[topic.slug] || 'Cơ bản',
    status: 'Published',
    publishedAt: publicationDates[topic.slug],
    isRecommended: topic.id <= 6,
    wordCount: topic.words.length,
    progress,
    isFavorite: progressData.favorites.includes(topic.slug),
    isStarred: progressData.starred.includes(topic.slug),
    words: topic.words.map((word) => ({
      ...word,
      images: word.hasSpecificImage ? [word.image] : [],
      phonetic: '',
      pronunciationGuide: {
        initial: null,
        final: null,
        tone: null,
        mouthShape: null,
        tongueAndLips: null,
        commonMistakes: [],
        practiceSteps: [],
      },
    })),
  }
}

export async function getStudentTopics(options = {}) {
  await Promise.resolve()
  const savedProgress = getStudentProgress()
  const topics = learningTopics
    .filter((topic) => topic.status === 'Published' || topic.status === 'Active' || !topic.status)
    .map((topic) => normalizeTopic(topic, savedProgress))

  const query = options.query?.trim().toLocaleLowerCase('vi') || ''
  let result = topics.filter((topic) => {
    const matchesQuery = !query || `${topic.title} ${topic.description}`.toLocaleLowerCase('vi').includes(query)
    const matchesLevel = !options.level || topic.level === options.level
    const matchesStatus = !options.status || topic.progress.status === options.status
    const matchesFavorite = !options.favoritesOnly || topic.isFavorite
    const matchesStarred = !options.starredOnly || topic.isStarred
    return matchesQuery && matchesLevel && matchesStatus && matchesFavorite && matchesStarred
  })

  if (options.sort === 'name') result = [...result].sort((a, b) => a.title.localeCompare(b.title, 'vi'))
  else if (options.sort === 'progress') result = [...result].sort((a, b) => b.progress.progress - a.progress.progress)
  else if (options.sort === 'recommended') result = [...result].sort((a, b) => Number(b.isRecommended) - Number(a.isRecommended))
  else result = [...result].sort((a, b) => b.publishedAt.localeCompare(a.publishedAt))
  return result
}

export async function getStudentTopicBySlug(slug) {
  await Promise.resolve()
  const savedProgress = getStudentProgress()
  const topic = learningTopics.find((item) => item.slug === slug)
  if (!topic || (topic.status && !['Published', 'Active'].includes(topic.status))) return null
  return normalizeTopic(topic, savedProgress)
}

export async function getStudentLearningPaths() {
  await Promise.resolve()
  return studentLearningPaths.map((path) => {
    const topics = path.topicSlugs.map((slug) => learningTopics.find((topic) => topic.slug === slug)).filter(Boolean)
    const completedTopics = topics.filter((topic) => getTopicProgress(topic.slug, topic.words.length).status === 'completed').length
    const nextTopic = topics.find((topic) => getTopicProgress(topic.slug, topic.words.length).status !== 'completed') || topics[0]
    return {
      ...path,
      topicCount: topics.length,
      completedTopics,
      progress: topics.length ? Math.round((completedTopics / topics.length) * 100) : 0,
      nextTopicSlug: nextTopic?.slug || null,
      status: completedTopics === topics.length && topics.length ? 'completed' : completedTopics ? 'in-progress' : 'not-started',
    }
  })
}
