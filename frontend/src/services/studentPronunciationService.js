import { illustrativePronunciationResult } from '../data/studentPronunciationMockData'
import { getWordPracticeStats, savePracticeResult } from './studentProgressService'

export async function createIllustrativePronunciationResult({ topicSlug, wordId, hasRecording, totalWords }) {
  if (!hasRecording) throw new Error('Hãy ghi âm trước khi xem kết quả minh họa.')
  await Promise.resolve()
  savePracticeResult(
    topicSlug,
    wordId,
    illustrativePronunciationResult.overall,
    illustrativePronunciationResult.components,
    totalWords,
  )
  return {
    ...illustrativePronunciationResult,
    components: illustrativePronunciationResult.components.map((component) => ({ ...component })),
  }
}

export function getPracticeStatistics(topicSlug, wordId) {
  return getWordPracticeStats(topicSlug, wordId)
}
