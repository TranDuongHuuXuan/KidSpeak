import { reactive } from 'vue'
import {
  clearAccessToken,
  getAccessToken,
  getStoredAuthUser,
  isRememberedSession,
  saveAuthSession,
} from '../api/authToken'

const state = reactive({
  user: null,
  isLoading: false,
  isRestored: false,
  restorePromise: null,
})

function isTokenValid(token) {
  if (!token) return false

  try {
    const payloadPart = token.split('.')[1]
    if (!payloadPart) return false

    const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/')
    const binaryPayload = atob(base64.padEnd(Math.ceil(base64.length / 4) * 4, '='))
    const payloadBytes = Uint8Array.from(binaryPayload, (character) => character.charCodeAt(0))
    const payload = JSON.parse(new TextDecoder().decode(payloadBytes))
    return Number.isFinite(payload.exp) && payload.exp * 1000 > Date.now()
  } catch {
    return false
  }
}

function normalizeRole(role) {
  const normalized = typeof role === 'string' ? role.trim().toUpperCase() : ''
  return normalized === 'USER' ? 'STUDENT' : normalized
}

function dashboardForRole(role) {
  return {
    STUDENT: 'StudentDashboard',
    EXPERT: 'ExpertDashboard',
    ADMIN: 'AdminDashboard',
  }[normalizeRole(role)] || null
}

export const authStore = {
  get user() {
    return state.user
  },

  get role() {
    return normalizeRole(state.user?.role_name || getStoredAuthUser()?.role_name)
  },

  get isLoading() {
    return state.isLoading
  },

  get hasSession() {
    return Boolean(getAccessToken())
  },

  get dashboardName() {
    return dashboardForRole(this.role)
  },

  setSession(token, user, remember) {
    saveAuthSession(token, user, remember)
    state.user = user
    state.isRestored = true
  },

  isAuthenticated() {
    const token = getAccessToken()
    if (!isTokenValid(token)) {
      this.clear()
      return false
    }

    if (!state.user) state.user = getStoredAuthUser()
    if (!state.user) {
      this.clear()
      return false
    }
    return true
  },

  async restore(force = false) {
    if (state.restorePromise) return state.restorePromise
    const token = getAccessToken()
    if (!token || !isTokenValid(token)) {
      if (token) this.clear()
      state.isRestored = true
      return null
    }
    if (!force && state.isRestored && state.user) return state.user

    state.isLoading = true
    state.restorePromise = (async () => {
      try {
        const { authService } = await import('../services/authService')
        const user = await authService.getCurrentUser()
        state.user = user
        saveAuthSession(token, user, isRememberedSession())
        return user
      } catch (error) {
        if (error?.status === 401 || error?.status === 403) this.clear()
        return null
      } finally {
        state.isLoading = false
        state.isRestored = true
        state.restorePromise = null
      }
    })()
    return state.restorePromise
  },

  hasRole(roles) {
    if (!this.isAuthenticated() || !Array.isArray(roles)) return false
    return roles.map(normalizeRole).includes(this.role)
  },

  clear() {
    clearAccessToken()
    state.user = null
    state.isRestored = true
  },

  logout() {
    this.clear()
  },
}
