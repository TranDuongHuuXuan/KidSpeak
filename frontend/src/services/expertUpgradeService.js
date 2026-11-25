import apiClient from '../api/axios'

export const expertUpgradeService = {
  async submit(details) {
    const reason = typeof details.reason === 'string' ? details.reason.trim() : ''
    if (!reason) throw new Error('Vui lòng nhập lý do muốn trở thành giáo viên.')
    const body = new FormData()
    body.append('specialty', details.specialty || '')
    body.append('experience', details.experience || '')
    body.append('reason', reason)
    body.append('introduction', details.introduction || '')
    if (details.previous_request_id) body.append('previous_request_id', details.previous_request_id)
    for (const key of details.keep_document_keys || []) body.append('keep_document_keys', key)
    for (const file of details.files || []) body.append('files', file)
    const response = await apiClient.post('/expert-upgrade-requests', body)
    return response.data
  },
  async mine() {
    const response = await apiClient.get('/expert-upgrade-requests/mine')
    return response.data || []
  },
  async list(status, filters = {}, page = 1, limit = 20) {
    const response = await apiClient.get('/expert-upgrade-requests', {
      params: {
        ...(status ? { status } : {}),
        search: filters.search || undefined,
        email: filters.email || undefined,
        reason: filters.reason || undefined,
        experience: filters.experience || undefined,
        page,
        limit,
      },
    })
    return { items: response.data || [], pagination: response.pagination }
  },
  async activate() {
    const response = await apiClient.post('/expert-upgrade-requests/activate')
    return response.data
  },
  async review(id, status, review_note = '') {
    const response = await apiClient.post(`/expert-upgrade-requests/${id}/review`, { status, review_note })
    return response.data
  },
  async documentUrl(requestId, index, download = false) {
    const response = await apiClient.get(`/expert-upgrade-requests/${requestId}/documents/${index}/url`, { params: download ? { download: true } : {} })
    return response.data
  },
}
