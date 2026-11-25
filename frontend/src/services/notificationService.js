import apiClient from '../api/axios'

export const notificationService = {
  async list() {
    const response = await apiClient.get('/notifications')
    return response.data || []
  },
  async markRead(id) {
    const response = await apiClient.patch(`/notifications/${id}/read`)
    return response.data
  },
}
