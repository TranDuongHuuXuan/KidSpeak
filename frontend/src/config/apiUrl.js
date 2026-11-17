const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

export const API_BASE_URL = (
  configuredApiBaseUrl || 'http://localhost:8000/api'
).replace(/\/+$/, '')

const configuredTimeout = Number(import.meta.env.VITE_API_TIMEOUT_MS || 15000)

if (!Number.isFinite(configuredTimeout) || configuredTimeout <= 0) {
  throw new Error('VITE_API_TIMEOUT_MS phải là số dương.')
}

export const API_TIMEOUT_MS = configuredTimeout
