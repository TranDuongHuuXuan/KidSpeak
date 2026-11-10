const STORAGE_KEY = 'kidspeak-student-learning-progress-v1'

function createEmptyProgress() {
  return { version: 1, topics: {}, favorites: [], starred: [] }
}

function readProgress() {
  let stored
  try {
    stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) return createEmptyProgress()
    const parsed = JSON.parse(stored)
    if (
      parsed?.version !== 1
      || !parsed.topics
      || typeof parsed.topics !== 'object'
      || Array.isArray(parsed.topics)
      || !Array.isArray(parsed.favorites)
      || !Array.isArray(parsed.starred)
    ) {
      throw new Error('Dữ liệu tiến độ không đúng định dạng.')
    }
    return parsed
  } catch (error) {
    throw new Error('Không thể đọc tiến độ học tập đã lưu. Hãy kiểm tra bộ nhớ trình duyệt rồi thử lại.', { cause: error })
  }
}

function writeProgress(progress) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
  } catch (error) {
    throw new Error('Không thể lưu tiến độ học tập vào trình duyệt.', { cause: error })
  }
  return progress
}

function getTopicEntry(progress, slug) {
  return progress.topics[slug] || {
    startedAt: null,
    lastStudiedAt: null,
    currentWordId: null,
    completedWordIds: [],
    practicedWordIds: [],
    latestIllustrativeScore: null,
    wordPracticeHistory: {},
  }
}

function addActivityDate(entry, timestamp) {
  const dateKey = (value) => {
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) return null
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  }
  const dates = Array.isArray(entry.activityDates) ? entry.activityDates.filter((value) => dateKey(value)) : []
  if (!dates.some((value) => dateKey(value) === dateKey(timestamp))) dates.push(timestamp)
  return dates.slice(-365)
}

function addLearningProgressSnapshot(entry, timestamp, totalWords, completedWordIds = entry.completedWordIds) {
  if (!Number.isInteger(totalWords) || totalWords <= 0) return entry.learningProgressHistory || []
  const date = new Date(timestamp)
  const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
  const snapshots = Array.isArray(entry.learningProgressHistory) ? [...entry.learningProgressHistory] : []
  const snapshot = {
    date: dateKey,
    recordedAt: timestamp,
    score: Math.round((Math.min(completedWordIds.length, totalWords) / totalWords) * 100),
    label: 'Tiến độ hoàn thành chủ đề',
  }
  const existingIndex = snapshots.findIndex((item) => item.date === dateKey)
  if (existingIndex >= 0) snapshots[existingIndex] = snapshot
  else snapshots.push(snapshot)
  return snapshots.slice(-365)
}

export function getStudentProgress() {
  return readProgress()
}

export function getTopicProgress(slug, totalWords) {
  const progress = readProgress()
  const entry = getTopicEntry(progress, slug)
  const completedWordIds = entry.completedWordIds.filter((id) => typeof id === 'string')
  const completed = Math.min(completedWordIds.length, totalWords)
  return {
    started: Boolean(entry.startedAt),
    startedAt: entry.startedAt,
    lastStudiedAt: entry.lastStudiedAt,
    currentWordId: entry.currentWordId,
    completedWordIds,
    practicedWordIds: entry.practicedWordIds.filter((id) => typeof id === 'string'),
    completed,
    progress: totalWords ? Math.round((completed / totalWords) * 100) : 0,
    status: completed === totalWords && totalWords > 0 ? 'completed' : completed > 0 || entry.startedAt ? 'in-progress' : 'not-started',
    latestIllustrativeScore: entry.latestIllustrativeScore,
  }
}

export function startTopic(slug, firstWordId, totalWords) {
  const progress = readProgress()
  const entry = getTopicEntry(progress, slug)
  const now = new Date().toISOString()
  progress.topics[slug] = {
    ...entry,
    startedAt: entry.startedAt || now,
    lastStudiedAt: now,
    currentWordId: entry.currentWordId || firstWordId || null,
    activityDates: addActivityDate(entry, now),
    learningProgressHistory: addLearningProgressSnapshot(entry, now, totalWords),
  }
  return writeProgress(progress)
}

export function saveCurrentWord(slug, wordId, totalWords) {
  const progress = readProgress()
  const entry = getTopicEntry(progress, slug)
  const now = new Date().toISOString()
  progress.topics[slug] = {
    ...entry,
    startedAt: entry.startedAt || now,
    lastStudiedAt: now,
    currentWordId: wordId,
    activityDates: addActivityDate(entry, now),
    learningProgressHistory: addLearningProgressSnapshot(entry, now, totalWords),
  }
  return writeProgress(progress)
}

export function savePracticeResult(slug, wordId, score, components = [], totalWords) {
  const progress = readProgress()
  const entry = getTopicEntry(progress, slug)
  const completedWordIds = new Set(entry.completedWordIds)
  completedWordIds.add(wordId)
  const practicedWordIds = new Set(entry.practicedWordIds)
  practicedWordIds.add(wordId)
  const wordPracticeHistory = { ...(entry.wordPracticeHistory || {}) }
  const history = Array.isArray(wordPracticeHistory[wordId]) ? [...wordPracticeHistory[wordId]] : []
  const now = new Date().toISOString()
  history.push({
    score,
    label: 'Dữ liệu minh họa',
    practicedAt: now,
    components: components.map(({ key, label, score: componentScore }) => ({
      key,
      label,
      score: componentScore,
    })),
  })
  wordPracticeHistory[wordId] = history
  progress.topics[slug] = {
    ...entry,
    startedAt: entry.startedAt || now,
    lastStudiedAt: now,
    currentWordId: wordId,
    activityDates: addActivityDate(entry, now),
    completedWordIds: [...completedWordIds],
    practicedWordIds: [...practicedWordIds],
    latestIllustrativeScore: { wordId, score, label: 'Dữ liệu minh họa', practicedAt: now },
    wordPracticeHistory,
    learningProgressHistory: addLearningProgressSnapshot(
      entry,
      now,
      totalWords,
      [...completedWordIds],
    ),
  }
  return writeProgress(progress)
}

export function getWordPracticeStats(slug, wordId) {
  const entry = getTopicEntry(readProgress(), slug)
  const history = Array.isArray(entry.wordPracticeHistory?.[wordId]) ? entry.wordPracticeHistory[wordId] : []
  const scores = history.map((item) => item.score).filter((score) => Number.isFinite(score))
  return {
    attempts: history.length,
    bestScore: scores.length ? Math.max(...scores) : null,
    latestScore: history.at(-1)?.score ?? null,
    completed: entry.completedWordIds.includes(wordId),
    history: [...history].reverse().slice(0, 20),
  }
}

export function toggleTopicFlag(slug, flag) {
  if (!['favorites', 'starred'].includes(flag)) throw new TypeError('Loại đánh dấu chủ đề không hợp lệ.')
  const progress = readProgress()
  const values = new Set(progress[flag])
  if (values.has(slug)) values.delete(slug)
  else values.add(slug)
  progress[flag] = [...values]
  return writeProgress(progress)
}

export function getNextUncompletedWord(topic, topicProgress) {
  if (!topic.words.length) return null
  const currentIndex = topic.words.findIndex((word) => word.id === topicProgress.currentWordId)
  if (currentIndex >= 0 && !topicProgress.completedWordIds.includes(topic.words[currentIndex].id)) {
    return topic.words[currentIndex]
  }
  return topic.words.find((word) => !topicProgress.completedWordIds.includes(word.id)) || topic.words[0]
}
