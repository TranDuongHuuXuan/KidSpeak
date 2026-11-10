const colors = {
  'kids-bg': '#fffdf5',
  'kids-surface': '#ffffff',
  'kids-primary': '#ffc107',
  'kids-secondary': '#4fc3f7',
  'kids-cta': '#ff7043',
  'kids-text': '#263238',
  'admin-bg': '#f8fafc',
  'admin-surface': '#ffffff',
  'admin-primary': '#1e293b',
  'admin-secondary': '#64748b',
  'admin-cta': '#2563eb',
  'admin-text': '#334155',
  'feedback-success': '#4caf50',
  'feedback-warning': '#ffb300',
  'feedback-error': '#ef5350',
  'feedback-info': '#2196f3',
}

for (const name of ['primary', 'secondary', 'accent', 'background', 'surface', 'text']) {
  colors[`theme-${name}`] = `rgb(var(--color-${name}-rgb) / <alpha-value>)`
}

export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors,
      fontFamily: {
        sans: ['Be Vietnam Pro', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [],
}