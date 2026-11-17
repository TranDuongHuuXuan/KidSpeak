import apiClient from '../api/axios'
import { API_ENDPOINTS } from '../config/apiEndpoints'
import { authStore } from '../stores/authStore'

export const authService = {
  async login({ email, password, remember = true }) {
    const response = await apiClient.post(
      API_ENDPOINTS.AUTH.LOGIN,
      { email, password },
      { skipAuth: true },
    )
    const loginData = response?.data

    if (!loginData?.access_token || !loginData?.user_principal) {
      throw new Error('Phản hồi đăng nhập không có thông tin phiên hợp lệ.')
    }

    authStore.setSession(loginData.access_token, loginData.user_principal, remember)
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
