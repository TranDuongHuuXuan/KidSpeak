import axios from 'axios'
import { API_BASE_URL, API_TIMEOUT_MS } from '../config/apiUrl'
import { getAccessToken } from './authToken'
import { normalizeApiError } from './apiError'
import { authStore } from '../stores/authStore'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT_MS,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  withCredentials: false,
})

apiClient.interceptors.request.use(
  (config) => {
    if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
      // Let the browser set multipart/form-data with its matching boundary.
      config.headers.delete('Content-Type')
    }
    if (!config.skipAuth) {
      const accessToken = getAccessToken()
      if (accessToken) {
        config.headers.set('Authorization', `Bearer ${accessToken}`)
      }
    }

    return config
  },
  (error) => Promise.reject(normalizeApiError(error)),
)

apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401 && !error.config?.skipAuth) {
      authStore.clear()
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('kidspeak:auth-expired'))
      }
    } else if (error.response?.status === 403 && typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('kidspeak:api-forbidden', {
        detail: { message: error.response.data?.detail || 'Bạn không có quyền thực hiện thao tác này.' },
      }))
    }

    return Promise.reject(normalizeApiError(error))
  },
)

export default apiClient
