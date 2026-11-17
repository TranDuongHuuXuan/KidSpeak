import apiClient from '../api/axios'
import { saveAccessToken } from '../api/authToken'
import { API_ENDPOINTS } from '../config/apiEndpoints'

export const authService = {
  async login({ email, password, remember = true }) {
    const response = await apiClient.post(
      API_ENDPOINTS.AUTH.LOGIN,
      { email, password },
      { skipAuth: true },
    )
    const loginData = response?.data

    if (!loginData?.access_token) {
      throw new Error('Phản hồi đăng nhập không có access token.')
    }

    saveAccessToken(loginData.access_token, remember)
    return loginData
  },

  async register(payload) {
    return apiClient.post(
      API_ENDPOINTS.AUTH.REGISTER,
      payload,
      { skipAuth: true },
    )
  },
}
