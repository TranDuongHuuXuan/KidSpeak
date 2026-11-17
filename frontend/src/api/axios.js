import axios from 'axios'
import { API_BASE_URL, API_TIMEOUT_MS } from '../config/apiUrl'
import { clearAccessToken, getAccessToken } from './authToken'
import { normalizeApiError } from './apiError'

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
    if (error.response?.status === 401) {
      clearAccessToken()
    }

    return Promise.reject(normalizeApiError(error))
  },
)

export default apiClient
