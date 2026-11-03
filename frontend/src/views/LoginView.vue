<script setup>
import { reactive, ref } from 'vue'

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
const form = reactive({
  identifier: '',
  password: '',
  remember: true,
})

const errors = reactive({
  identifier: '',
  password: '',
  form: '',
})

const showPassword = ref(false)
const loading = ref(false)

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const USERNAME_RE = /^[\p{L}\p{N}._-]{3,}$/u

function validateIdentifier() {
  const value = form.identifier.trim()
  if (!value) {
    errors.identifier = 'Bạn chưa nhập tên đăng nhập hoặc email.'
  } else if (value.includes('@') ? !EMAIL_RE.test(value) : !USERNAME_RE.test(value)) {
    errors.identifier = 'Tên đăng nhập hoặc email chưa đúng. Bạn kiểm tra lại nhé.'
  } else {
    errors.identifier = ''
  }
  return !errors.identifier
}

function validatePassword() {
  if (!form.password) {
    errors.password = 'Bạn chưa nhập mật khẩu.'
  } else if (form.password.length < 6) {
    errors.password = 'Mật khẩu cần có ít nhất 6 ký tự.'
  } else {
    errors.password = ''
  }
  return !errors.password
}

// ---------------------------------------------------------------------------
// Submit
// ---------------------------------------------------------------------------
/**
 * TODO: Kết nối API đăng nhập khi có thông tin backend.
 * Hàm này nhận payload { identifier, password, remember } và
 * cần trả về kết quả đăng nhập (hoặc throw lỗi nếu thất bại).
 * Hiện tại KHÔNG giả lập đăng nhập thành công.
 */
async function requestLogin(/* payload */) {
  throw new Error('NOT_IMPLEMENTED')
}

async function handleSubmit() {
  errors.form = ''

  const okIdentifier = validateIdentifier()
  const okPassword = validatePassword()
  if (!okIdentifier || !okPassword) return

  loading.value = true
  try {
    await requestLogin({
      identifier: form.identifier.trim(),
      password: form.password,
      remember: form.remember,
    })
    // TODO: điều hướng sau khi đăng nhập thành công (router.push(...)).
  } catch (err) {
    errors.form =
      err?.message === 'NOT_IMPLEMENTED'
        ? 'Chức năng đăng nhập chưa được kết nối với máy chủ.'
        : 'Đăng nhập chưa được. Bạn kiểm tra lại thông tin rồi thử lại nhé.'
  } finally {
    loading.value = false
  }
}

function handleGoogleLogin() {
  // TODO: Replace this message with the Google OAuth flow when it is integrated.
  errors.form = 'Đăng nhập bằng Google chưa được tích hợp.'
}

function handleFacebookLogin() {
  // TODO: Replace this message with the Facebook OAuth flow when it is integrated.
  errors.form = 'Đăng nhập bằng Facebook chưa được tích hợp.'
}

// Style dùng chung cho input (chỉ dùng token màu của hệ thống)
const inputBase =
  'h-[52px] w-full rounded-2xl border-2 bg-kids-surface px-4 text-base text-kids-text ' +
  'placeholder:text-kids-text/50 outline-none transition-colors ' +
  'focus:ring-4 focus:ring-kids-secondary/30 disabled:opacity-60'
const inputOk = 'border-kids-text/20 focus:border-kids-secondary'
const inputBad = 'border-kids-cta focus:border-kids-cta'
</script>

<template>
  <main class="min-h-screen bg-kids-bg text-kids-text lg:grid lg:grid-cols-2">
    <!-- ===================== Khu minh họa (desktop) ===================== -->
    <section
      class="relative hidden flex-col items-center justify-center gap-8 overflow-hidden px-12 py-12 lg:flex"
      aria-hidden="true"
    >
      <!-- Hình nền trang trí -->
      <div class="absolute -left-24 -top-24 h-72 w-72 rounded-full bg-kids-primary/30"></div>
      <div class="absolute -bottom-20 -right-16 h-64 w-64 rounded-full bg-kids-secondary/20"></div>

      <div
        class="relative w-full max-w-md rounded-3xl bg-kids-surface p-6 shadow-xl"
      >
        <div class="rounded-2xl bg-kids-primary/15 p-4">
          <!-- Mascot "Spark" -->
          <svg viewBox="0 0 400 330" class="h-auto w-full" role="img">
            <!-- Sóng âm -->
            <g fill="none" stroke-width="8" stroke-linecap="round" class="stroke-kids-secondary">
              <path d="M312 130 q24 25 0 50" />
              <path d="M338 108 q42 47 0 94" />
              <path d="M88 130 q-24 25 0 50" />
              <path d="M62 108 q-42 47 0 94" />
            </g>

            <!-- Micro trên đầu -->
            <rect x="178" y="22" width="44" height="80" rx="22"
              class="fill-kids-secondary stroke-kids-text" stroke-width="5" />
            <path d="M190 48h20M190 64h20" class="stroke-kids-surface" stroke-width="4" stroke-linecap="round" />

            <!-- Thân / đầu -->
            <circle cx="200" cy="172" r="90"
              class="fill-kids-primary stroke-kids-text" stroke-width="5" />

            <!-- Mắt -->
            <circle cx="168" cy="152" r="11" class="fill-kids-text" />
            <circle cx="232" cy="152" r="11" class="fill-kids-text" />
            <circle cx="172" cy="148" r="4" class="fill-kids-surface" />
            <circle cx="236" cy="148" r="4" class="fill-kids-surface" />

            <!-- Má hồng -->
            <circle cx="140" cy="186" r="14" class="fill-kids-cta" opacity="0.45" />
            <circle cx="260" cy="186" r="14" class="fill-kids-cta" opacity="0.45" />

            <!-- Miệng đang nói -->
            <path d="M172 190 Q200 232 228 190 Z"
              class="fill-kids-text stroke-kids-text" stroke-width="4" stroke-linejoin="round" />
            <path d="M184 206 Q200 220 216 206 Q200 198 184 206 Z" class="fill-kids-cta" />

            <!-- Khối chữ cái -->
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

        <!-- Huy hiệu sao -->
        <span
          class="absolute -bottom-5 -right-5 flex h-14 w-14 items-center justify-center rounded-full bg-kids-primary shadow-lg"
        >
          <svg viewBox="0 0 24 24" class="h-7 w-7 fill-none stroke-kids-text" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z" />
          </svg>
        </span>
      </div>

      <div class="relative max-w-md text-center">
        <h2 class="text-4xl font-extrabold leading-tight">
          Mỗi lần nói là một lần giỏi hơn
        </h2>
        <p class="mt-3 text-lg text-kids-text/80">
          Cùng bạn Spark luyện phát âm mỗi ngày, vui như đang chơi.
        </p>
      </div>
    </section>

    <!-- ========================= Khu đăng nhập ========================= -->
    <section class="flex items-center justify-center px-4 py-10 sm:px-8">
      <div class="w-full max-w-md">
        <!-- Logo -->
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

        <div class="flex flex-col gap-6 rounded-3xl bg-kids-surface p-6 shadow-xl sm:p-8 lg:min-h-[580px]">
          <div class="flex flex-col gap-2">
            <h1 class="text-3xl font-extrabold">Chào mừng bạn trở lại!</h1>
            <p class="text-kids-text/80">
              Đăng nhập để cùng Spark luyện nói tiếp nào.
            </p>
          </div>

          <form class="flex flex-1 flex-col gap-6" novalidate @submit.prevent="handleSubmit">
            <div class="flex flex-1 flex-col justify-center gap-5">
              <!-- Lỗi chung -->
              <div
                v-if="errors.form"
                class="flex items-start gap-3 rounded-2xl border-2 border-kids-cta bg-kids-cta/10 p-3"
                role="alert"
              >
                <span
                  class="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-kids-cta text-sm font-bold"
                  aria-hidden="true"
                >!</span>
                <p class="text-sm font-medium">{{ errors.form }}</p>
              </div>

            <div class="flex flex-col gap-5">
              <!-- Tên đăng nhập / email -->
              <div class="flex flex-col gap-2">
                <label for="identifier" class="block text-sm font-bold">
                  Tên đăng nhập hoặc email
                </label>
                <input
                  id="identifier"
                  v-model="form.identifier"
                  type="text"
                  inputmode="email"
                  autocomplete="username"
                  placeholder="ten-cua-ban hoặc ban@example.com"
                  :class="[inputBase, errors.identifier ? inputBad : inputOk]"
                  :aria-invalid="!!errors.identifier"
                  :aria-describedby="errors.identifier ? 'identifier-error' : undefined"
                  :disabled="loading"
                  @blur="validateIdentifier"
                  @input="errors.identifier && validateIdentifier()"
                />
                <p v-if="errors.identifier" id="identifier-error" class="flex items-center gap-2 text-sm font-medium">
                  <span class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-kids-cta text-xs font-bold" aria-hidden="true">!</span>
                  {{ errors.identifier }}
                </p>
              </div>

              <!-- Mật khẩu -->
              <div class="flex flex-col gap-2">
                <label for="password" class="block text-sm font-bold">Mật khẩu</label>
                <div class="relative">
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    autocomplete="current-password"
                    placeholder="Ít nhất 6 ký tự"
                    :class="[inputBase, 'pr-14', errors.password ? inputBad : inputOk]"
                    :aria-invalid="!!errors.password"
                    :aria-describedby="errors.password ? 'password-error' : undefined"
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
                    <!-- Mắt mở -->
                    <svg v-if="!showPassword" viewBox="0 0 24 24" class="h-5 w-5 fill-none stroke-kids-text"
                      stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                    <!-- Mắt gạch -->
                    <svg v-else viewBox="0 0 24 24" class="h-5 w-5 fill-none stroke-kids-text"
                      stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                      <path d="M9.9 5.2A10 10 0 0 1 12 5c6.4 0 10 7 10 7a17 17 0 0 1-3.2 4M6.6 6.6C3.7 8.4 2 12 2 12s3.6 7 10 7a9.7 9.7 0 0 0 4.4-1M3 3l18 18" />
                      <path d="M9.9 9.9a3 3 0 0 0 4.2 4.2" />
                    </svg>
                  </button>
                </div>
                <p v-if="errors.password" id="password-error" class="flex items-center gap-2 text-sm font-medium">
                  <span class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-kids-cta text-xs font-bold" aria-hidden="true">!</span>
                  {{ errors.password }}
                </p>
              </div>
            </div>

            <!-- Ghi nhớ + quên mật khẩu -->
            <div class="flex flex-wrap items-center justify-between gap-3">
              <label class="flex cursor-pointer items-center gap-2.5 text-sm font-medium">
                <input
                  v-model="form.remember"
                  type="checkbox"
                  class="h-5 w-5 cursor-pointer rounded accent-kids-cta focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-kids-secondary"
                  :disabled="loading"
                />
                Ghi nhớ đăng nhập
              </label>
              <!-- Đổi thành <RouterLink to="..."> nếu dự án đã có route tương ứng -->
              <a
                href="/forgot-password"
                class="rounded text-sm font-bold underline decoration-kids-cta decoration-2 underline-offset-4 outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
              >
                Quên mật khẩu?
              </a>
            </div>

            </div>

            <!-- Nút đăng nhập -->
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
              {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
            </button>

            <div class="flex flex-col gap-3">
              <div class="flex items-center gap-3 text-sm text-kids-text/60" aria-hidden="true">
                <span class="h-px flex-1 bg-kids-text/15"></span>
                <span class="shrink-0">Hoặc tiếp tục với</span>
                <span class="h-px flex-1 bg-kids-text/15"></span>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  class="flex h-12 min-w-0 items-center justify-center gap-2 rounded-2xl border border-kids-text/15 bg-white px-3 text-sm font-semibold text-kids-text transition hover:bg-kids-secondary/10 active:scale-[0.98] focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                  @click="handleGoogleLogin"    
                >
                  <svg viewBox="0 0 48 48" class="h-5 w-5 shrink-0" aria-hidden="true">
                    <path fill="#4285F4" d="M43.6 20.5H42V20H24v8h11.3A12 12 0 1 1 32 14.8l5.7-5.7A20 20 0 1 0 44 24c0-1.2-.1-2.4-.4-3.5Z" />
                    <path fill="#34A853" d="M6.3 14.7 13 19.6A12 12 0 0 1 32 14.8l5.7-5.7A20 20 0 0 0 4.5 12.3l1.8 2.4Z" />
                    <path fill="#FBBC05" d="M4.5 35.7 11 30.8A12 12 0 0 1 11 17.2l-6.5-4.9a20 20 0 0 0 0 23.4Z" />
                    <path fill="#EA4335" d="M24 44c5.4 0 10-1.8 13.3-4.9l-6.5-5a12 12 0 0 1-19.8-3.3l-6.5 4.9A20 20 0 0 0 24 44Z" />
                  </svg>
                  <span class="truncate">Google</span>
                </button>

                <button
                  type="button"
                  class="flex h-12 min-w-0 items-center justify-center gap-2 rounded-2xl border border-kids-text/15 bg-white px-3 text-sm font-semibold text-kids-text transition hover:bg-kids-secondary/10 active:scale-[0.98] focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                  @click="handleFacebookLogin"
                >
                  <svg viewBox="0 0 24 24" class="h-5 w-5 shrink-0" aria-hidden="true">
                    <path fill="#1877F2" d="M24 12a12 12 0 1 0-13.875 11.85v-8.38H7.08V12h3.045V9.36c0-3.007 1.792-4.668 4.533-4.668 1.312 0 2.686.234 2.686.234v2.953h-1.513c-1.49 0-1.954.925-1.954 1.874V12h3.325l-.532 3.47h-2.793v8.38A12 12 0 0 0 24 12Z" />
                    <path fill="#fff" d="m16.67 15.47.53-3.47h-3.32V9.75c0-.95.46-1.87 1.95-1.87h1.51V4.93s-1.37-.24-2.69-.24c-2.74 0-4.53 1.66-4.53 4.67V12H7.08v3.47h3.04v8.38a12.1 12.1 0 0 0 3.74 0v-8.38h2.81Z" />
                  </svg>
                  <span class="truncate">Facebook</span>
                </button>
              </div>
            </div>
          </form>
        </div>

        <!-- Đăng ký -->
        <div class="mt-5">
            <p class="text-center text-sm">
                Chưa có tài khoản?
                <a
                href="/register"
                class="rounded font-bold underline decoration-kids-cta decoration-2 underline-offset-4 outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
                >
                Đăng ký ngay
                </a>
            </p>
        </div>
      </div>
    </section>
  </main>
</template>