const FLASH_TOAST_KEY = 'kidspeak-flash-toast'

export function setFlashToast(message) {
  sessionStorage.setItem(FLASH_TOAST_KEY, message)
}

export function consumeFlashToast() {
  const message = sessionStorage.getItem(FLASH_TOAST_KEY)
  sessionStorage.removeItem(FLASH_TOAST_KEY)
  return message
}
