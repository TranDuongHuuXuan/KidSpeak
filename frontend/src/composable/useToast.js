import { computed, reactive } from 'vue'

const DEFAULT_DURATION = { success: 3000, info: 3000, warning: 4000, error: 5000 }
const DEFAULT_TITLE = { success: 'Thành công', info: 'Thông báo', warning: 'Cảnh báo', error: 'Có lỗi xảy ra' }
const state = reactive({ items: [], confirmation: null })
let nextId = 1
let confirmationResolver = null

function removeToast(id) {
  const item = state.items.find((toast) => toast.id === id)
  if (item?.timer) clearTimeout(item.timer)
  state.items = state.items.filter((toast) => toast.id !== id)
}

function show(type, title, message = '', options = {}) {
  if (title && typeof title === 'object') {
    options = title
    title = options.title || ''
    message = options.message || ''
  }
  const normalizedTitle = String(title || '').trim()
  const normalizedMessage = String(message || '').trim()
  if (!normalizedTitle && !normalizedMessage) return null
  const duplicate = state.items.find((item) => item.type === type && item.title === normalizedTitle && item.message === normalizedMessage)
  if (duplicate) return duplicate.id

  const duration = Number.isFinite(options.duration) ? Math.max(0, options.duration) : DEFAULT_DURATION[type]
  const item = { id: nextId++, type, title: normalizedTitle || DEFAULT_TITLE[type], message: normalizedMessage, duration, timer: null }
  if (duration > 0) item.timer = setTimeout(() => removeToast(item.id), duration)
  state.items.push(item)
  return item.id
}

function confirm(message, options = {}) {
  if (confirmationResolver) return Promise.resolve(false)
  if (message && typeof message === 'object') {
    options = message
    message = options.message || ''
  }
  return new Promise((resolve) => {
    confirmationResolver = resolve
    state.confirmation = {
      title: options.title || 'Xác nhận thao tác',
      message: String(message || ''),
      confirmText: options.confirmText || 'Xác nhận',
      cancelText: options.cancelText || 'Hủy',
      tone: options.tone === 'danger' ? 'danger' : 'primary',
    }
  })
}

function resolveConfirmation(accepted) {
  const resolve = confirmationResolver
  confirmationResolver = null
  state.confirmation = null
  resolve?.(accepted)
}

export const toast = {
  success: (title, message, options) => show('success', title, message, options),
  error: (title, message, options) => show('error', title, message, options),
  warning: (title, message, options) => show('warning', title, message, options),
  info: (title, message, options) => show('info', title, message, options),
  confirm,
  resolveConfirmation,
  dismiss: removeToast,
  clear() {
    for (const item of state.items) clearTimeout(item.timer)
    state.items = []
    resolveConfirmation(false)
  },
}

export function useToast() {
  return {
    toast,
    toasts: computed(() => state.items),
    confirmation: computed(() => state.confirmation),
  }
}
