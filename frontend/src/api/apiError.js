function getValidationMessage(detail) {
  if (typeof detail === 'string') return detail
  if (!Array.isArray(detail)) return ''

  return detail
    .map((item) => item?.msg)
    .filter(Boolean)
    .join(' ')
}

function getStatusMessage(status) {
  const messages = {
    400: 'Yêu cầu không hợp lệ.',
    401: 'Phiên đăng nhập không hợp lệ hoặc đã hết hạn.',
    403: 'Bạn không có quyền thực hiện thao tác này.',
    404: 'Không tìm thấy tài nguyên yêu cầu.',
    422: 'Dữ liệu gửi lên chưa hợp lệ.',
    500: 'Máy chủ gặp lỗi. Vui lòng thử lại sau.',
  }

  return messages[status] || 'Không thể xử lý yêu cầu.'
}

export class ApiError extends Error {
  constructor(message, { status = null, code = null, data = null, cause } = {}) {
    super(message, { cause })
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.data = data
  }
}

export function normalizeApiError(error) {
  const response = error.response
  const status = response?.status ?? null
  const data = response?.data ?? null

  if (response) {
    const detailMessage = typeof data?.detail === 'object'
      ? data.detail?.message
      : getValidationMessage(data?.detail)
    const serverMessage = detailMessage || data?.message
    return new ApiError(
      serverMessage || getStatusMessage(status),
      { status, code: data?.code || data?.detail?.code || error.code || null, data, cause: error },
    )
  }

  if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
    return new ApiError('Yêu cầu đã quá thời gian chờ. Vui lòng thử lại.', {
      code: error.code,
      cause: error,
    })
  }

  return new ApiError('Không thể kết nối máy chủ. Vui lòng kiểm tra kết nối mạng.', {
    code: error.code ?? null,
    cause: error,
  })
}
