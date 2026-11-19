import apiClient from '../api/axios'
import { API_ENDPOINTS } from '../config/apiEndpoints'

export const mediaStorageService = {
  async uploadAvatar(file) {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post(API_ENDPOINTS.MEDIA.AVATAR, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async getAvatar() {
    const response = await apiClient.get(API_ENDPOINTS.MEDIA.AVATAR)
    return response.data
  },

  async deleteAvatar() {
    return apiClient.delete(API_ENDPOINTS.MEDIA.AVATAR)
  },
}
