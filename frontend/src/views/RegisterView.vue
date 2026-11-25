<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/authService'
import { authStore } from '../stores/authStore'
import { setFlashToast } from '../services/flashToast'

const router = useRouter()
const form = reactive({
  fullName: '',
  email: '',
  dateOfBirth: '',
  password: '',
  confirmPassword: '',
  termsAccepted: false,
})

const errors = reactive({
  fullName: '',
  email: '',
  dateOfBirth: '',
  password: '',
  confirmPassword: '',
  termsAccepted: '',
  form: '',
})

const loading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const successMessage = ref('')

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const today = new Date()
const maxDateOfBirth = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

function validateFullName() {
  const value = form.fullName.trim()
  if (value.length < 2) {
    errors.fullName = 'Họ và tên cần có ít nhất 2 ký tự.'
  } else if (value.length > 100) {
    errors.fullName = 'Họ và tên không được vượt quá 100 ký tự.'
  } else {
    errors.fullName = ''
  }
  return !errors.fullName
}

function validateEmail() {
  const value = form.email.trim()
  if (!value) {
    errors.email = 'Bạn chưa nhập địa chỉ email.'
  } else if (!EMAIL_RE.test(value)) {
    errors.email = 'Địa chỉ email chưa đúng định dạng.'
  } else {
    errors.email = ''
  }
  return !errors.email
}

function validateDateOfBirth() {
  const value = form.dateOfBirth
  const dateParts = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
  const parsedDate = dateParts
    ? new Date(Date.UTC(Number(dateParts[1]), Number(dateParts[2]) - 1, Number(dateParts[3])))
    : null
  if (!value) {
    errors.dateOfBirth = 'Bạn hãy chọn ngày sinh.'
  } else if (
    !parsedDate ||
    parsedDate.getUTCFullYear() !== Number(dateParts[1]) ||
    parsedDate.getUTCMonth() !== Number(dateParts[2]) - 1 ||
    parsedDate.getUTCDate() !== Number(dateParts[3])
  ) {
    errors.dateOfBirth = 'Ngày sinh không hợp lệ.'
  } else if (value > maxDateOfBirth) {
    errors.dateOfBirth = 'Ngày sinh không thể nằm trong tương lai.'
  } else {
    errors.dateOfBirth = ''
  }
  return !errors.dateOfBirth
}

function validatePassword() {
  if (!form.password) {
    errors.password = 'Bạn chưa nhập mật khẩu.'
  } else if (form.password.length < 8 || new TextEncoder().encode(form.password).length > 72) {
    errors.password = 'Mật khẩu cần từ 8 ký tự và không vượt quá 72 byte UTF-8.'
  } else if (
    !/[a-z]/.test(form.password) ||
    !/[A-Z]/.test(form.password) ||
    !/\d/.test(form.password) ||
    !/[^a-zA-Z0-9]/.test(form.password)
  ) {
    errors.password = 'Mật khẩu cần có chữ hoa, chữ thường, chữ số và ký tự đặc biệt.'
  } else {
    errors.password = ''
  }

  if (form.confirmPassword) validateConfirmPassword()
  return !errors.password
}

function validateConfirmPassword() {
  if (!form.confirmPassword) {
    errors.confirmPassword = 'Bạn hãy nhập lại mật khẩu.'
  } else if (form.confirmPassword !== form.password) {
    errors.confirmPassword = 'Mật khẩu xác nhận chưa trùng khớp.'
  } else {
    errors.confirmPassword = ''
  }
  return !errors.confirmPassword
}

function validateTerms() {
  errors.termsAccepted = form.termsAccepted
    ? ''
    : 'Bạn cần đồng ý với điều khoản sử dụng để đăng ký.'
  return !errors.termsAccepted
}

async function requestRegister(payload) {
  return authService.register(payload)
}

async function handleSubmit() {
  if (loading.value) return

  errors.form = ''
  successMessage.value = ''

  const isValid = [
    validateFullName(),
    validateEmail(),
    validateDateOfBirth(),
    validatePassword(),
    validateConfirmPassword(),
    validateTerms(),
  ].every(Boolean)

  if (!isValid) return

  loading.value = true
  try {
    const result = await requestRegister({
      full_name: form.fullName.trim(),
      email: form.email.trim(),
      password: form.password,
      date_of_birth: form.dateOfBirth,
    })
    successMessage.value = result?.message || 'Tạo tài khoản thành công. Bạn có thể đăng nhập ngay.'
    setFlashToast(successMessage.value)
    authStore.clear()
    await router.push({ name: 'Login' })
  } catch (error) {
    errors.form = error instanceof Error
      ? error.message
      : 'Đăng ký chưa thành công. Bạn thử lại nhé.'
  } finally {
    loading.value = false
  }
}

const inputBase =
  'h-[52px] w-full rounded-2xl border-2 bg-kids-surface px-4 text-base text-kids-text ' +
  'placeholder:text-kids-text/50 outline-none transition-colors ' +
  'focus:ring-4 focus:ring-kids-secondary/30 disabled:opacity-60'
const inputOk = 'border-kids-text/20 focus:border-kids-secondary'
const inputBad = 'border-kids-cta focus:border-kids-cta'
</script>

<template>
  <main class="min-h-screen bg-kids-bg text-kids-text lg:grid lg:grid-cols-2">
    <section
      class="relative hidden flex-col items-center justify-center gap-8 overflow-hidden px-12 py-12 lg:flex"
      aria-hidden="true"
    >
      <div class="absolute -left-24 -top-24 h-72 w-72 rounded-full bg-kids-primary/30"></div>
      <div class="absolute -bottom-20 -right-16 h-64 w-64 rounded-full bg-kids-secondary/20"></div>

      <div class="relative w-full max-w-md rounded-3xl bg-kids-surface p-6 shadow-xl">
        <div class="rounded-2xl bg-kids-primary/15 p-4">
          <svg viewBox="0 0 400 330" class="h-auto w-full" role="img">
            <g fill="none" stroke-width="8" stroke-linecap="round" class="stroke-kids-secondary">
              <path d="M312 130 q24 25 0 50" />
              <path d="M338 108 q42 47 0 94" />
              <path d="M88 130 q-24 25 0 50" />
              <path d="M62 108 q-42 47 0 94" />
            </g>
            <rect x="178" y="22" width="44" height="80" rx="22"
              class="fill-kids-secondary stroke-kids-text" stroke-width="5" />
            <path d="M190 48h20M190 64h20" class="stroke-kids-surface" stroke-width="4" stroke-linecap="round" />
            <circle cx="200" cy="172" r="90"
              class="fill-kids-primary stroke-kids-text" stroke-width="5" />
            <circle cx="168" cy="152" r="11" class="fill-kids-text" />
            <circle cx="232" cy="152" r="11" class="fill-kids-text" />
            <circle cx="172" cy="148" r="4" class="fill-kids-surface" />
            <circle cx="236" cy="148" r="4" class="fill-kids-surface" />
            <circle cx="140" cy="186" r="14" class="fill-kids-cta" opacity="0.45" />
            <circle cx="260" cy="186" r="14" class="fill-kids-cta" opacity="0.45" />
            <path d="M172 190 Q200 232 228 190 Z"
              class="fill-kids-text stroke-kids-text" stroke-width="4" stroke-linejoin="round" />
            <path d="M184 206 Q200 220 216 206 Q200 198 184 206 Z" class="fill-kids-cta" />
            <g stroke-width="4" class="stroke-kids-text" stroke-linejoin="round">
              <rect x="108" y="270" width="48" height="48" rx="8" class="fill-kids-cta" />
              <rect x="160" y="270" width="48" height="48" rx="8" class="fill-kids-secondary" />
              <rect x="212" y="270" width="48" height="48" rx="8" class="fill-kids-surface" />
              <rect x="268" y="270" width="48" height="48" rx="8" class="fill-kids-primary" />
            </g>
            <g class="fill-kids-text" font-size="28" font-weight="800" text-anchor="middle">
              <text x="132" y="303">A</text>
              <text x="184" y="303">B</text>
              <text x="236" y="303">C</text>
              <text x="292" y="303">Ơ</text>
            </g>
          </svg>
        </div>
        <span class="absolute -bottom-5 -right-5 flex h-14 w-14 items-center justify-center rounded-full bg-kids-primary shadow-lg">
          <svg viewBox="0 0 24 24" class="h-7 w-7 fill-none stroke-kids-text" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z" />
          </svg>
        </span>
      </div>

      <div class="relative max-w-md text-center">
        <h2 class="text-4xl font-extrabold leading-tight">Cùng Spark bắt đầu hành trình mới!</h2>
        <p class="mt-3 text-lg text-kids-text/80">
          Tạo tài khoản để luyện phát âm vui hơn mỗi ngày.
        </p>
      </div>
    </section>

    <section class="flex items-center justify-center px-4 py-8 sm:px-8 sm:py-10">
      <div class="w-full max-w-md">
        <div class="mb-6 flex items-center gap-3">
          <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-kids-primary">
            <svg viewBox="0 0 24 24" class="h-7 w-7 fill-none stroke-kids-text" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <rect x="9" y="2" width="6" height="12" rx="3" />
              <path d="M5 11a7 7 0 0 0 14 0M12 18v4M8 22h8" />
            </svg>
          </span>
          <span class="text-2xl font-extrabold">KidSpeak</span>
        </div>

        <div class="rounded-3xl bg-kids-surface p-6 shadow-xl sm:p-8">
          <header class="mb-6 flex flex-col gap-2">
            <h1 class="text-3xl font-extrabold">Tạo tài khoản KidSpeak</h1>
            <p class="text-kids-text/80">Bắt đầu hành trình luyện phát âm cùng Spark nhé!</p>
          </header>

          <div
            v-if="errors.form"
            class="mb-5 flex items-start gap-3 rounded-2xl border-2 border-kids-cta bg-kids-cta/10 p-3"
            role="alert"
          >
            <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-kids-cta text-sm font-bold" aria-hidden="true">!</span>
            <p class="text-sm font-medium">{{ errors.form }}</p>
          </div>
          <div
            v-if="successMessage"
            class="mb-5 rounded-2xl border-2 border-feedback-success bg-feedback-success/10 p-3 text-sm font-medium"
            role="status"
          >
            {{ successMessage }}
          </div>

          <form class="flex flex-col gap-6" novalidate @submit.prevent="handleSubmit">
            <div class="flex flex-col gap-5">
              <div class="flex flex-col gap-2">
                <label for="fullName" class="text-sm font-bold">Họ và tên</label>
                <input
                  id="fullName"
                  v-model="form.fullName"
                  :class="[inputBase, errors.fullName ? inputBad : inputOk]"
                  type="text"
                  autocomplete="name"
                  placeholder="Nhập họ và tên của bạn"
                  required
                  minlength="2"
                  maxlength="100"
                  :aria-invalid="!!errors.fullName"
                  :aria-describedby="errors.fullName ? 'fullName-error' : undefined"
                  :disabled="loading"
                  @blur="validateFullName"
                  @input="errors.fullName && validateFullName()"
                />
                <p v-if="errors.fullName" id="fullName-error" class="text-sm font-medium text-kids-cta" role="alert">
                  {{ errors.fullName }}
                </p>
              </div>

              <div class="flex flex-col gap-2">
                <label for="email" class="text-sm font-bold">Địa chỉ email</label>
                <input
                  id="email"
                  v-model="form.email"
                  :class="[inputBase, errors.email ? inputBad : inputOk]"
                  type="email"
                  autocomplete="email"
                  placeholder="example@email.com"
                  required
                  :aria-invalid="!!errors.email"
                  :aria-describedby="errors.email ? 'email-error' : undefined"
                  :disabled="loading"
                  @blur="validateEmail"
                  @input="errors.email && validateEmail()"
                />
                <p v-if="errors.email" id="email-error" class="text-sm font-medium text-kids-cta" role="alert">
                  {{ errors.email }}
                </p>
              </div>

              <div class="flex flex-col gap-2">
                <label for="dateOfBirth" class="text-sm font-bold">Ngày sinh</label>
                <input
                  id="dateOfBirth"
                  v-model="form.dateOfBirth"
                  :class="[inputBase, errors.dateOfBirth ? inputBad : inputOk]"
                  type="date"
                  lang="vi"
                  :max="maxDateOfBirth"
                  required
                  :aria-invalid="!!errors.dateOfBirth"
                  :aria-describedby="errors.dateOfBirth ? 'dateOfBirth-error' : 'dateOfBirth-hint'"
                  :disabled="loading"
                  @blur="validateDateOfBirth"
                  @change="validateDateOfBirth"
                />
                <p v-if="errors.dateOfBirth" id="dateOfBirth-error" class="text-sm font-medium text-kids-cta" role="alert">
                  {{ errors.dateOfBirth }}
                </p>
                <p v-else id="dateOfBirth-hint" class="text-xs text-kids-text/60">
                  Ngày sinh được gửi theo định dạng YYYY-MM-DD.
                </p>
              </div>

              <div class="flex flex-col gap-2">
                <label for="password" class="text-sm font-bold">Mật khẩu</label>
                <div class="relative">
                  <input
                    id="password"
                    v-model="form.password"
                    :class="[inputBase, 'pr-14', errors.password ? inputBad : inputOk]"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="new-password"
                    placeholder="Nhập mật khẩu của bạn"
                    required
                    minlength="8"
                    maxlength="72"
                    :aria-invalid="!!errors.password"
                    :aria-describedby="errors.password ? 'password-error' : 'password-hint'"
                    :disabled="loading"
                    @blur="validatePassword"
                    @input="errors.password && validatePassword()"
                  />
                  <button
                    type="button"
                    class="absolute inset-y-0 right-2 my-auto flex h-10 w-10 items-center justify-center rounded-xl outline-none transition-colors hover:bg-kids-secondary/20 focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                    :aria-label="showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'"
                    :aria-pressed="showPassword"
                    @click="showPassword = !showPassword"
                  >
                    <svg viewBox="0 0 24 24" class="h-5 w-5 fill-none stroke-kids-text" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path v-if="!showPassword" d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" />
                      <path v-else d="M9.9 5.2A10 10 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4M6.6 6.6C3.7 8.4 2 12 2 12s3.6 7 10 7a9.7 9.7 0 0 0 4.4-1M3 3l18 18" />
                      <circle v-if="!showPassword" cx="12" cy="12" r="3" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" id="password-error" class="text-sm font-medium text-kids-cta" role="alert">
                  {{ errors.password }}
                </p>
                <p v-else id="password-hint" class="text-xs text-kids-text/60">
                  Từ 8 ký tự, gồm chữ hoa, chữ thường, chữ số và ký tự đặc biệt.
                </p>
              </div>

              <div class="flex flex-col gap-2">
                <label for="confirmPassword" class="text-sm font-bold">Xác nhận mật khẩu</label>
                <div class="relative">
                  <input
                    id="confirmPassword"
                    v-model="form.confirmPassword"
                    :class="[inputBase, 'pr-14', errors.confirmPassword ? inputBad : inputOk]"
                    :type="showConfirmPassword ? 'text' : 'password'"
                    autocomplete="new-password"
                    placeholder="Nhập lại mật khẩu"
                    required
                    :aria-invalid="!!errors.confirmPassword"
                    :aria-describedby="errors.confirmPassword ? 'confirmPassword-error' : undefined"
                    :disabled="loading"
                    @blur="validateConfirmPassword"
                    @input="errors.confirmPassword && validateConfirmPassword()"
                  />
                  <button
                    type="button"
                    class="absolute inset-y-0 right-2 my-auto flex h-10 w-10 items-center justify-center rounded-xl outline-none transition-colors hover:bg-kids-secondary/20 focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                    :aria-label="showConfirmPassword ? 'Ẩn mật khẩu xác nhận' : 'Hiện mật khẩu xác nhận'"
                    :aria-pressed="showConfirmPassword"
                    @click="showConfirmPassword = !showConfirmPassword"
                  >
                    <svg viewBox="0 0 24 24" class="h-5 w-5 fill-none stroke-kids-text" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path v-if="!showConfirmPassword" d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" />
                      <path v-else d="M9.9 5.2A10 10 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4M6.6 6.6C3.7 8.4 2 12 2 12s3.6 7 10 7a9.7 9.7 0 0 0 4.4-1M3 3l18 18" />
                      <circle v-if="!showConfirmPassword" cx="12" cy="12" r="3" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.confirmPassword" id="confirmPassword-error" class="text-sm font-medium text-kids-cta" role="alert">
                  {{ errors.confirmPassword }}
                </p>
              </div>
            </div>

            <div class="flex flex-col gap-1">
              <label for="termsAccepted" class="flex items-start gap-3 text-sm">
                <input
                  id="termsAccepted"
                  v-model="form.termsAccepted"
                  type="checkbox"
                  class="mt-0.5 h-4 w-4 rounded border-kids-text/30 accent-kids-secondary focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                  :aria-invalid="!!errors.termsAccepted"
                  :aria-describedby="errors.termsAccepted ? 'terms-error' : undefined"
                  :disabled="loading"
                  @change="validateTerms"
                />
                <span>Tôi đồng ý với điều khoản sử dụng.</span>
              </label>
              <p v-if="errors.termsAccepted" id="terms-error" class="pl-7 text-sm font-medium text-kids-cta" role="alert">
                {{ errors.termsAccepted }}
              </p>
            </div>

            <button
              type="submit"
              class="flex h-[52px] w-full items-center justify-center gap-2 rounded-2xl bg-kids-cta px-6 text-base font-semibold text-kids-text shadow-md outline-none transition hover:brightness-95 focus-visible:ring-4 focus-visible:ring-kids-secondary/50 active:translate-y-px disabled:cursor-not-allowed disabled:opacity-70"
              :disabled="loading"
              :aria-busy="loading"
            >
              <svg
                v-if="loading"
                viewBox="0 0 24 24"
                class="h-5 w-5 animate-spin fill-none stroke-kids-text motion-reduce:animate-none"
                stroke-width="3"
                stroke-linecap="round"
                aria-hidden="true"
              >
                <path d="M12 3a9 9 0 1 0 9 9" />
              </svg>
              {{ loading ? 'Đang tạo tài khoản...' : 'Tạo tài khoản' }}
            </button>
          </form>
        </div>

        <div class="mt-5">
            <p class="text-center text-sm">
                Đã có tài khoản?
                <RouterLink
                to="/login"
                class="rounded font-bold underline decoration-kids-cta decoration-2 underline-offset-4 outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                >
                Đăng nhập ngay
                </RouterLink>
            </p>
        </div>
      </div>
    </section>
  </main>
</template>
