import { reactive } from 'vue'
import {
  clearAccessToken,
  getAccessToken,
  getStoredAuthUser,
  saveAuthSession,
} from '../api/authToken'

const state = reactive({ user: null })

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

export const authStore = {
  get user() {
    return state.user
  },

  setSession(token, user, remember) {
    saveAuthSession(token, user, remember)
    state.user = user
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

  clear() {
    clearAccessToken()
    state.user = null
  },
}
