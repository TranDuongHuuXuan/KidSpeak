import { studentMockDashboard } from '../data/studentMockData'
import { getStudentTopics } from './studentTopicService'

export async function fetchStudentDashboard() {
  await new Promise((resolve) => setTimeout(resolve, 250))
  const topics = await getStudentTopics({ sort: 'recommended' })
  const featuredTopics = topics.slice(0, 6)
  const continuingTopic = topics.find((topic) => topic.progress.status === 'in-progress') || topics[0]
  const iconNames = ['paw', 'star', 'heart', 'book', 'route', 'sparkles']
  const colorNames = [
    'bg-sky-50 text-sky-700',
    'bg-rose-50 text-rose-700',
    'bg-violet-50 text-violet-700',
    'bg-amber-50 text-amber-700',
    'bg-emerald-50 text-emerald-700',
    'bg-orange-50 text-orange-700',
  ]

  return {
    ...studentMockDashboard,
    topics: featuredTopics.map((topic, index) => ({
      id: topic.slug,
      title: topic.title,
      words: topic.wordCount,
      level: topic.level,
      progress: topic.progress.progress,
      image: topic.image,
      icon: iconNames[index],
      color: colorNames[index],
    })),
    continueLearning: continuingTopic
      ? {
          title: continuingTopic.title,
          description: continuingTopic.description,
          image: continuingTopic.image,
          completed: continuingTopic.progress.completed,
          total: continuingTopic.wordCount,
          progress: continuingTopic.progress.progress,
          topicId: continuingTopic.slug,
        }
      : null,
  }
}
