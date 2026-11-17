const ACCESS_TOKEN_KEY = 'kidspeak-access-token'

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY)
    || sessionStorage.getItem(ACCESS_TOKEN_KEY)
}

export function saveAccessToken(token, remember = true) {
  const targetStorage = remember ? localStorage : sessionStorage
  const otherStorage = remember ? sessionStorage : localStorage

  otherStorage.removeItem(ACCESS_TOKEN_KEY)
  targetStorage.setItem(ACCESS_TOKEN_KEY, token)
}

export function clearAccessToken() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  sessionStorage.removeItem(ACCESS_TOKEN_KEY)
}
