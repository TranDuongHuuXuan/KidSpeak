const statusNames = {
  completed: 'Hoàn thành',
  'in-progress': 'Đang học',
  'not-started': 'Chưa bắt đầu',
}

const weekdays = [
  { key: 1, label: 'Thứ 2' },
  { key: 2, label: 'Thứ 3' },
  { key: 3, label: 'Thứ 4' },
  { key: 4, label: 'Thứ 5' },
  { key: 5, label: 'Thứ 6' },
  { key: 6, label: 'Thứ 7' },
  { key: 0, label: 'Chủ nhật' },
]

function dateKey(date) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

function getPeriods(range) {
  const end = new Date()
  end.setHours(0, 0, 0, 0)
  const start = new Date(end)
  start.setDate(start.getDate() - Number(range) + 1)

  if (Number(range) === 7) {
    return Array.from({ length: 7 }, (_, index) => {
      const date = new Date(start)
      date.setDate(start.getDate() + index)
      return {
        key: dateKey(date),
        label: date.toLocaleDateString('vi-VN', { weekday: 'short', day: 'numeric' }),
        start: dateKey(date),
        end: dateKey(date),
      }
    })
  }

  if (Number(range) === 30) {
    const periods = []
    for (let cursor = new Date(start); cursor <= end;) {
      const periodEnd = new Date(cursor)
      periodEnd.setDate(periodEnd.getDate() + 6)
      if (periodEnd > end) periodEnd.setTime(end.getTime())
      periods.push({
        key: dateKey(cursor),
        label: cursor.toLocaleDateString('vi-VN', { day: 'numeric', month: 'numeric' }),
        start: dateKey(cursor),
        end: dateKey(periodEnd),
      })
      cursor = new Date(periodEnd)
      cursor.setDate(cursor.getDate() + 1)
    }
    return periods
  }

  const periods = []
  for (let year = start.getFullYear(), month = start.getMonth(); year < end.getFullYear() || (year === end.getFullYear() && month <= end.getMonth());) {
    const monthStart = new Date(year, month, 1)
    const monthEnd = new Date(year, month + 1, 0)
    const periodStart = monthStart < start ? start : monthStart
    const periodEnd = monthEnd > end ? end : monthEnd
    periods.push({
      key: `${year}-${String(month + 1).padStart(2, '0')}`,
      label: monthStart.toLocaleDateString('vi-VN', { month: 'short', year: '2-digit' }),
      start: dateKey(periodStart),
      end: dateKey(periodEnd),
    })
    month += 1
    if (month > 11) {
      month = 0
      year += 1
    }
  }
  return periods
}

function periodForDate(date, periods) {
  return periods.find((period) => date >= period.start && date <= period.end)
}

function average(values) {
  return values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length) : null
}

export function getStudentResultsChartData(report, range) {
  const periods = getPeriods(range)
  const learningByPeriod = new Map(periods.map((period) => [period.key, []]))
  const pronunciationByPeriod = new Map(periods.map((period) => [period.key, []]))

  for (const item of report.learningProgressHistory) {
    const period = periodForDate(item.date, periods)
    if (period) learningByPeriod.get(period.key).push(item.score)
  }
  for (const attempt of report.attempts) {
    const date = dateKey(new Date(attempt.practicedAt))
    const period = periodForDate(date, periods)
    if (period) pronunciationByPeriod.get(period.key).push(attempt.score)
  }

  const progress = periods.map((period) => ({
    ...period,
    score: average(learningByPeriod.get(period.key)),
  }))
  const pronunciation = periods.map((period) => ({
    ...period,
    score: average(pronunciationByPeriod.get(period.key)),
    attempts: pronunciationByPeriod.get(period.key).length,
  }))
  const distribution = ['completed', 'in-progress', 'not-started'].map((status) => ({
    key: status,
    label: statusNames[status],
    value: report.topics.filter((topic) => topic.progress.status === status).length,
  }))
  const cutoff = periods[0]?.start
  const filteredAttempts = report.attempts.filter((attempt) => dateKey(new Date(attempt.practicedAt)) >= cutoff)
  const components = report.componentScores.map((part) => {
    const scores = filteredAttempts.flatMap((attempt) => attempt.components
      .filter((component) => component.key === part.key)
      .map((component) => component.score))
    return { ...part, score: average(scores), samples: scores.length }
  })
  const weekdayCounts = weekdays.map((weekday) => ({
    ...weekday,
    value: filteredAttempts.filter((attempt) => new Date(attempt.practicedAt).getDay() === weekday.key).length,
  }))

  return {
    progress,
    distribution,
    totalTopics: report.topics.length,
    components,
    bestComponent: components.filter((part) => part.score !== null).sort((a, b) => b.score - a.score)[0] || null,
    lowestComponent: components.filter((part) => part.score !== null).sort((a, b) => a.score - b.score)[0] || null,
    weekdayCounts,
    comparison: periods.map((period, index) => ({
      ...period,
      learning: progress[index].score,
      pronunciation: pronunciation[index].score,
    })),
    learningHasData: progress.some((item) => item.score !== null),
    pronunciationHasData: pronunciation.some((item) => item.score !== null),
    componentsHaveData: components.some((item) => item.score !== null),
    hasPracticeData: filteredAttempts.length > 0,
    hasComparisonData: progress.some((item) => item.score !== null) || pronunciation.some((item) => item.score !== null),
    rangeDays: Number(range),
  }
}
