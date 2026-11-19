import apiClient from '../api/axios'
import { API_ENDPOINTS } from '../config/apiEndpoints'

function multipart(payload) {
  const formData = new FormData()
  for (const [key, value] of Object.entries(payload)) {
    if (value !== undefined && value !== null) formData.append(key, value)
  }
  return formData
}

function unwrap(response) {
  return response?.data
}

export const expertLessonService = {
  async listCategories({ skip = 0, limit = 20 } = {}) {
    return apiClient.get(API_ENDPOINTS.LESSON_CATEGORIES, { params: { skip, limit } })
  },

  async getCategory(categoryId) {
    return apiClient.get(`${API_ENDPOINTS.LESSON_CATEGORIES}/${categoryId}`)
  },

  async createCategory(payload) {
    return unwrap(await apiClient.post(API_ENDPOINTS.LESSON_CATEGORIES, multipart(payload), {
      headers: { 'Content-Type': 'multipart/form-data' },
    }))
  },

  async updateCategory(categoryId, payload) {
    return unwrap(await apiClient.put(
      `${API_ENDPOINTS.LESSON_CATEGORIES}/${categoryId}`,
      multipart(payload),
      { headers: { 'Content-Type': 'multipart/form-data' } },
    ))
  },

  async deleteCategory(categoryId) {
    return apiClient.delete(`${API_ENDPOINTS.LESSON_CATEGORIES}/${categoryId}`)
  },

  async listLessons(params = {}) {
    return apiClient.get(API_ENDPOINTS.LESSONS, { params })
  },

  async getLesson(lessonId) {
    return apiClient.get(`${API_ENDPOINTS.LESSONS}/${lessonId}`)
  },

  async createLesson(payload) {
    return unwrap(await apiClient.post(API_ENDPOINTS.LESSONS, multipart(payload), {
      headers: { 'Content-Type': 'multipart/form-data' },
    }))
  },

  async updateLesson(lessonId, payload) {
    return unwrap(await apiClient.put(
      `${API_ENDPOINTS.LESSONS}/${lessonId}`,
      multipart(payload),
      { headers: { 'Content-Type': 'multipart/form-data' } },
    ))
  },

  async deleteLesson(lessonId) {
    return apiClient.delete(`${API_ENDPOINTS.LESSONS}/${lessonId}`)
  },
}
