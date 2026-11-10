import { getStudentTopics } from './studentTopicService'
import { getStudentProgress } from './studentProgressService'

const pronunciationParts = [
  { key: 'initial', label: 'Âm đầu' },
  { key: 'final', label: 'Phần vần' },
  { key: 'tone', label: 'Thanh điệu' },
]

const badgeDefinitions = [
  { id: 'first-practice', name: 'Người mới bắt đầu', icon: 'sparkles', description: 'Xác nhận lượt luyện phát âm đầu tiên.', goal: 'attempts', target: 1 },
  { id: 'steady-learner', name: 'Chăm chỉ học tập', icon: 'flame', description: 'Học liên tục ít nhất 3 ngày.', goal: 'streak', target: 3 },
  { id: 'word-expert', name: 'Chuyên gia từ vựng', icon: 'book', description: 'Hoàn thành ít nhất 20 từ vựng.', goal: 'words', target: 20 },
  { id: 'clear-voice', name: 'Bé phát âm tốt', icon: 'microphone', description: 'Đạt điểm trung bình minh họa từ 80 trở lên.', goal: 'average', target: 80 },
  { id: 'persistent-practice', name: 'Kiên trì luyện tập', icon: 'trophy', description: 'Xác nhận ít nhất 10 lượt luyện.', goal: 'attempts', target: 10 },
]

function localDateKey(value) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return null
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function getStudyStreak(dateKeys) {
  const studied = new Set(dateKeys)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const todayKey = localDateKey(today)
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)
  let cursor = studied.has(todayKey) ? today : yesterday
  let streak = 0

  while (studied.has(localDateKey(cursor))) {
    streak += 1
    cursor = new Date(cursor)
    cursor.setDate(cursor.getDate() - 1)
  }
  return streak
}

function average(values) {
  return values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length) : null
}

export async function getStudentResults() {
  const [topics, savedProgress] = await Promise.all([
    getStudentTopics({ sort: 'name' }),
    Promise.resolve(getStudentProgress()),
  ])
  const topicBySlug = new Map(topics.map((topic) => [topic.slug, topic]))
  const attempts = []
  const learningProgressHistory = []
  const studyDates = new Set()
  const studySessions = new Set()

  for (const [topicSlug, entry] of Object.entries(savedProgress.topics)) {
    const topic = topicBySlug.get(topicSlug)
    if (!topic) continue
    const activityDates = [
      ...(Array.isArray(entry.activityDates) ? entry.activityDates : []),
      entry.lastStudiedAt,
    ]
    for (const value of activityDates) {
      const date = localDateKey(value)
      if (!date) continue
      studyDates.add(date)
      studySessions.add(`${date}:${topicSlug}`)
    }
    if (Array.isArray(entry.learningProgressHistory)) {
      for (const item of entry.learningProgressHistory) {
        const date = localDateKey(item?.recordedAt || item?.date)
        if (!date || !Number.isFinite(item?.score)) continue
        learningProgressHistory.push({
          topicSlug,
          topicTitle: topic.title,
          date,
          score: item.score,
          label: item.label || 'Tiến độ hoàn thành chủ đề',
        })
      }
    }
    if (!entry?.wordPracticeHistory || typeof entry.wordPracticeHistory !== 'object') continue

    for (const [wordId, history] of Object.entries(entry.wordPracticeHistory)) {
      if (!Array.isArray(history)) continue
      const word = topic.words.find((item) => item.id === wordId)
      if (!word) continue

      history.forEach((item, index) => {
        if (!Number.isFinite(item?.score) || !localDateKey(item.practicedAt)) return
        const studyDate = localDateKey(item.practicedAt)
        studyDates.add(studyDate)
        studySessions.add(`${studyDate}:${topicSlug}`)
        attempts.push({
          id: `${topicSlug}-${wordId}-${item.practicedAt}-${index}`,
          topicSlug,
          topicTitle: topic.title,
          topicLevel: topic.level,
          wordId,
          word: word.word,
          image: word.image,
          imageAlt: word.imageAlt,
          phonetic: word.phonetic || '',
          score: item.score,
          label: item.label || 'Dữ liệu minh họa',
          practicedAt: item.practicedAt,
          components: Array.isArray(item.components)
            ? item.components.filter((part) => pronunciationParts.some((known) => known.key === part.key) && Number.isFinite(part.score))
            : [],
        })
      })
    }
  }

  attempts.sort((a, b) => new Date(b.practicedAt) - new Date(a.practicedAt))
  const topicProgress = topics.map((topic) => ({
    ...topic,
    studiedWords: topic.progress.completed,
    statusLabel: topic.progress.status === 'completed'
      ? 'Hoàn thành'
      : topic.progress.status === 'in-progress' ? 'Đang học' : 'Chưa bắt đầu',
  }))
  const participatedTopics = topicProgress.filter((topic) => topic.progress.status !== 'not-started')
  const learnedWordKeys = new Set(topicProgress.flatMap((topic) =>
    topic.progress.completedWordIds.map((wordId) => `${topic.slug}:${wordId}`)))
  const practicedWordKeys = new Set(attempts.map((attempt) => `${attempt.topicSlug}:${attempt.wordId}`))
  const byDayTopic = new Map()

  for (const attempt of attempts) {
    const date = localDateKey(attempt.practicedAt)
    const sessionKey = `${date}:${attempt.topicSlug}`
    const session = byDayTopic.get(sessionKey) || {
      id: sessionKey,
      date,
      topicSlug: attempt.topicSlug,
      topicTitle: attempt.topicTitle,
      topicLevel: attempt.topicLevel,
      wordIds: new Set(),
      scores: [],
      attempts: 0,
    }
    session.wordIds.add(attempt.wordId)
    session.scores.push(attempt.score)
    session.attempts += 1
    byDayTopic.set(sessionKey, session)
  }

  const history = [...byDayTopic.values()]
    .map((session) => {
      const topic = topicBySlug.get(session.topicSlug)
      return {
        ...session,
        learnedWords: session.wordIds.size,
        practicedWords: session.wordIds.size,
        averageScore: average(session.scores),
        status: topic?.progress.status || 'not-started',
        statusLabel: topic?.progress.status === 'completed'
          ? 'Hoàn thành'
          : topic?.progress.status === 'in-progress' ? 'Đang học' : 'Chưa bắt đầu',
        wordIds: [...session.wordIds],
      }
    })
    .sort((a, b) => b.date.localeCompare(a.date))

  const latestByWord = new Map()
  for (const attempt of attempts) {
    const key = `${attempt.topicSlug}:${attempt.wordId}`
    if (!latestByWord.has(key)) latestByWord.set(key, attempt)
  }

  const needsPractice = [...latestByWord.values()]
    .filter((attempt) => attempt.score < 80 || attempt.components.some((part) => part.score < 75))
    .map((attempt) => {
      const weakestParts = attempt.components
        .filter((part) => part.score < 75)
        .sort((a, b) => a.score - b.score)
      const allAttempts = savedProgress.topics[attempt.topicSlug]?.wordPracticeHistory?.[attempt.wordId] || []
      return {
        ...attempt,
        attempts: allAttempts.length,
        improvementParts: weakestParts,
        improvementLabel: weakestParts.length
          ? weakestParts.map((part) => part.label).join(', ')
          : 'Chưa có điểm thành phần cần cải thiện',
      }
    })
    .sort((a, b) => a.score - b.score)

  const componentScores = pronunciationParts.map((part) => {
    const scores = attempts.flatMap((attempt) => attempt.components
      .filter((item) => item.key === part.key)
      .map((item) => item.score))
    return { ...part, score: average(scores), samples: scores.length }
  })
  const scoredParts = componentScores.filter((part) => part.score !== null)
  const bestPart = scoredParts.length ? [...scoredParts].sort((a, b) => b.score - a.score)[0] : null
  const improvePart = scoredParts.length ? [...scoredParts].sort((a, b) => a.score - b.score)[0] : null
  const averagePronunciation = average(attempts.map((attempt) => attempt.score))
  const averageLearning = average(participatedTopics.map((topic) => topic.progress.progress))
  const streak = getStudyStreak([...studyDates])
  const badgeValues = {
    attempts: attempts.length,
    streak,
    words: learnedWordKeys.size,
    average: averagePronunciation || 0,
  }
  const badges = badgeDefinitions.map((badge) => ({
    ...badge,
    earned: badgeValues[badge.goal] >= badge.target,
    current: badgeValues[badge.goal],
  }))
  const completedTopics = topicProgress.filter((topic) => topic.progress.status === 'completed').length
  const inProgressTopics = topicProgress.filter((topic) => topic.progress.status === 'in-progress').length

  return {
    topics: topicProgress,
    attempts,
    learningProgressHistory,
    history,
    needsPractice,
    componentScores,
    bestPart,
    improvePart,
    badges,
    stats: {
      totalTopics: topics.length,
      participatedTopics: participatedTopics.length,
      completedTopics,
      inProgressTopics,
      notStartedTopics: topics.length - participatedTopics.length,
      learnedWords: learnedWordKeys.size,
      practicedWords: practicedWordKeys.size,
      practiceAttempts: attempts.length,
      averageLearning,
      averagePronunciation,
      highestScore: attempts.length ? Math.max(...attempts.map((attempt) => attempt.score)) : null,
      goalWords: new Set([...latestByWord.values()].filter((attempt) => attempt.score >= 80).map((attempt) => `${attempt.topicSlug}:${attempt.wordId}`)).size,
      wordsToImprove: needsPractice.length,
      studyStreak: streak,
      studySessions: studySessions.size,
    },
  }
}
