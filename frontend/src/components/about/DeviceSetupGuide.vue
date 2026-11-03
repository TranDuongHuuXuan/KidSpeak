<script setup>
import { ref } from 'vue'

const activeTab = ref('microphone')
const instructions = {
  microphone: {
    label: 'Cài đặt Microphone',
    steps: [
      'Mở KidSpeak bằng trình duyệt Chrome.',
      'Nhấn biểu tượng thông tin hoặc cài đặt trang bên cạnh thanh địa chỉ.',
      'Tìm mục Microphone và chọn Allow (Cho phép).',
      'Tải lại trang và kiểm tra micro trong chức năng có sử dụng thu âm.',
    ],
  },
  camera: {
    label: 'Cài đặt Camera',
    steps: [
      'Mở trang KidSpeak bằng trình duyệt.',
      'Truy cập phần quyền trang web bên cạnh thanh địa chỉ.',
      'Tìm mục Camera và chọn Allow nếu tính năng đang dùng yêu cầu camera.',
      'Tải lại trang và kiểm tra camera trong tính năng tương ứng.',
    ],
  },
}

function selectTabWithArrow(event) {
  if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return
  event.preventDefault()
  activeTab.value = activeTab.value === 'microphone' ? 'camera' : 'microphone'
  document.getElementById(`device-tab-${activeTab.value}`)?.focus()
}

const troubleshooting = [
  {
    title: 'Trình duyệt không nhận micro',
    description: 'Kiểm tra quyền Microphone của trang và quyền truy cập micro trong cài đặt hệ điều hành.',
  },
  {
    title: 'Micro đang được ứng dụng khác sử dụng',
    description: 'Đóng ứng dụng đang dùng micro rồi tải lại trang trước khi thử lại.',
  },
  {
    title: 'Camera không hoạt động',
    description: 'Camera chỉ cần được cấp quyền nếu tính năng cụ thể yêu cầu; kiểm tra quyền trang và thiết bị.',
  },
  {
    title: 'Đã cấp quyền nhưng thiết bị vẫn chưa nhận',
    description: 'Tải lại trang, kiểm tra thiết bị đầu vào mặc định và thử lại bằng trình duyệt cập nhật.',
  },
]
</script>

<template>
  <section class="bg-white py-16 sm:py-20 lg:py-24">
    <div class="mx-auto max-w-screen-2xl px-5 sm:px-8 lg:px-12">
      <div class="mx-auto max-w-3xl text-center">
        <p class="text-sm font-bold uppercase tracking-[0.14em] text-kids-secondary">Hỗ trợ phụ huynh</p>
        <h2 class="mt-3 text-3xl font-extrabold text-kids-text sm:text-4xl">Hướng dẫn cài đặt thiết bị</h2>
        <p class="mt-4 leading-7 text-kids-text/70">
          Một vài bước cơ bản để kiểm tra quyền micro hoặc camera trong trình duyệt.
          Đây là hướng dẫn chung, không phải ảnh chụp giao diện trình duyệt.
        </p>
      </div>

      <div class="mx-auto mt-9 max-w-4xl">
        <div class="flex flex-col gap-2 rounded-2xl bg-kids-bg p-2 sm:flex-row" role="tablist" aria-label="Chọn hướng dẫn thiết bị">
          <button
            id="device-tab-microphone"
            type="button"
            role="tab"
            aria-controls="device-panel-microphone"
            :aria-selected="activeTab === 'microphone'"
            :tabindex="activeTab === 'microphone' ? 0 : -1"
            class="min-h-12 flex-1 rounded-xl px-4 py-3 text-sm font-bold transition focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
            :class="activeTab === 'microphone' ? 'bg-white text-kids-text shadow-sm' : 'text-kids-text/65 hover:bg-white/70'"
            @click="activeTab = 'microphone'"
            @keydown="selectTabWithArrow"
          >
            Cài đặt Microphone
          </button>
          <button
            id="device-tab-camera"
            type="button"
            role="tab"
            aria-controls="device-panel-camera"
            :aria-selected="activeTab === 'camera'"
            :tabindex="activeTab === 'camera' ? 0 : -1"
            class="min-h-12 flex-1 rounded-xl px-4 py-3 text-sm font-bold transition focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-kids-secondary/40"
            :class="activeTab === 'camera' ? 'bg-white text-kids-text shadow-sm' : 'text-kids-text/65 hover:bg-white/70'"
            @click="activeTab = 'camera'"
            @keydown="selectTabWithArrow"
          >
            Cài đặt Camera
          </button>
        </div>

        <div
          v-for="(guide, key) in instructions"
          v-show="activeTab === key"
          :id="`device-panel-${key}`"
          :key="key"
          role="tabpanel"
          :aria-labelledby="`device-tab-${key}`"
          class="mt-5"
          tabindex="0"
        >
          <ol class="grid gap-3 sm:grid-cols-2">
            <li
              v-for="(step, index) in guide.steps"
              :key="step"
              class="flex gap-4 rounded-2xl border border-kids-text/10 bg-kids-bg/50 p-4 sm:p-5"
            >
              <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-kids-primary/40 text-sm font-extrabold text-kids-text">
                {{ index + 1 }}
              </span>
              <p class="pt-1 text-sm leading-6 text-kids-text/75">{{ step }}</p>
            </li>
          </ol>
          <p
            v-if="key === 'camera'"
            class="mt-4 rounded-xl bg-kids-secondary/10 px-4 py-3 text-sm leading-6 text-kids-text/75"
          >
            Camera không bắt buộc cho các bước đăng ký hiện có; chỉ cấp quyền khi một chức năng cụ thể yêu cầu.
          </p>
        </div>
      </div>

      <div class="mt-12">
        <h3 class="text-center text-xl font-extrabold text-kids-text sm:text-2xl">Một số cách xử lý thường gặp</h3>
        <div class="mt-5 grid gap-3 sm:grid-cols-2">
          <article
            v-for="item in troubleshooting"
            :key="item.title"
            class="rounded-2xl border border-kids-text/10 bg-white p-4"
          >
            <h4 class="text-sm font-bold text-kids-text">{{ item.title }}</h4>
            <p class="mt-2 text-sm leading-6 text-kids-text/70">{{ item.description }}</p>
          </article>
        </div>
        <p class="mt-4 text-center text-xs leading-5 text-kids-text/60">
          Giao diện hiện tại chưa tích hợp thu âm hoặc sử dụng camera; các bước trên chỉ hướng dẫn quyền thiết bị ở mức trình duyệt.
        </p>
      </div>
    </div>
  </section>
</template>
