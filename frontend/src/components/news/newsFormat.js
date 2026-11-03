export function formatNewsDate(date) {
  return new Intl.DateTimeFormat('vi-VN', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(`${date}T00:00:00`))
}
