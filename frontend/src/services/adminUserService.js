import apiClient from '../api/axios'

const ROOT = '/admin/users'

export const adminUserService = {
  async list(params) {
    const response = await apiClient.get(ROOT, { params })
    return response?.data
  },
  async get(id) {
    const response = await apiClient.get(`${ROOT}/${id}`)
    return response?.data
  },
  async update(id, payload) {
    const response = await apiClient.patch(`${ROOT}/${id}`, payload)
    return response?.data
  },
  async setActive(id, active) {
    const action = active ? 'activate' : 'deactivate'
    const response = await apiClient.patch(`${ROOT}/${id}/${action}`)
    return response?.data
  },
}
