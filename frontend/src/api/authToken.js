const ACCESS_TOKEN_KEY = 'kidspeak-access-token'
const AUTH_USER_KEY = 'kidspeak-auth-user'

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
    || sessionStorage.getItem(ACCESS_TOKEN_KEY)
}

export function saveAccessToken(token, remember = true) {
  const targetStorage = remember ? localStorage : sessionStorage
  const otherStorage = remember ? sessionStorage : localStorage

  otherStorage.removeItem(ACCESS_TOKEN_KEY)
  otherStorage.removeItem(AUTH_USER_KEY)
  targetStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function saveAuthSession(token, user, remember = true) {
  const targetStorage = remember ? localStorage : sessionStorage
  const otherStorage = remember ? sessionStorage : localStorage
  const safeUser = {
    id: user.id,
    full_name: user.full_name,
    email: user.email,
    role_id: user.role_id,
    avatar: user.avatar,
    is_active: user.is_active,
  }

  otherStorage.removeItem(ACCESS_TOKEN_KEY)
  otherStorage.removeItem(AUTH_USER_KEY)
  targetStorage.setItem(ACCESS_TOKEN_KEY, token)
  targetStorage.setItem(AUTH_USER_KEY, JSON.stringify(safeUser))
}

export function getStoredAuthUser() {
  const token = getAccessToken()
  if (!token) return null

  const storage = localStorage.getItem(ACCESS_TOKEN_KEY) ? localStorage : sessionStorage
  const serializedUser = storage.getItem(AUTH_USER_KEY)
  if (!serializedUser) return null

  try {
    return JSON.parse(serializedUser)
  } catch (error) {
    clearAccessToken()
    throw new Error('Không thể đọc thông tin phiên đăng nhập đã lưu.', { cause: error })
  }
}

export function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  sessionStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(AUTH_USER_KEY)
  sessionStorage.removeItem(AUTH_USER_KEY)
}
