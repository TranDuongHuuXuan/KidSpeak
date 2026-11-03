<script setup>
import { ref } from 'vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, defaultSettings, notify } from '../../data/adminMockData'

const settings = adminData.settings
const savedSettings = ref({ ...settings })
const resetOpen = ref(false)
const logoFile = ref('')

function saveSettings() {
  savedSettings.value = { ...settings }
  notify('Đã lưu cấu hình hệ thống.')
}

function resetSettings() {
  Object.assign(settings, defaultSettings)
  savedSettings.value = { ...defaultSettings }
  logoFile.value = ''
  resetOpen.value = false
  notify('Đã khôi phục cấu hình mặc định.')
}

function selectLogo(event) {
  const [file] = event.target.files || []
  if (file) logoFile.value = file.name
}
</script>

<template>
  <AdminPageShell title="Cấu hình hệ thống" description="Điều chỉnh thông tin, tài khoản và các thiết lập vận hành của KidSpeak.">
    <template #actions>
      <button type="button" class="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50" @click="resetOpen = true">Khôi phục mặc định</button>
      <button type="button" class="inline-flex items-center gap-2 rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700" @click="saveSettings"><AdminIcon name="check" :size="18" />Lưu thay đổi</button>
    </template>

    <div class="grid gap-5 xl:grid-cols-2">
      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="mb-5 flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-amber-700"><AdminIcon name="dashboard" /></span><div><h3 class="font-bold text-slate-800">Thông tin chung</h3><p class="text-xs text-slate-400">Tên và thông tin liên hệ</p></div></div>
        <div class="space-y-4">
          <label class="block text-sm font-semibold text-slate-700">Tên hệ thống<input v-model.trim="settings.systemName" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
          <label class="block text-sm font-semibold text-slate-700">Mô tả<textarea v-model.trim="settings.description" rows="3" class="mt-1.5 w-full rounded-xl border border-slate-200 p-3 font-normal outline-none focus:border-admin-cta" /></label>
          <label class="block text-sm font-semibold text-slate-700">Email liên hệ<input v-model.trim="settings.contactEmail" type="email" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" /></label>
          <label class="block text-sm font-semibold text-slate-700">Logo hệ thống<input type="file" accept="image/*" class="mt-1.5 block w-full rounded-xl border border-slate-200 text-sm file:mr-3 file:border-0 file:bg-slate-50 file:px-3 file:py-2.5 file:font-semibold" @change="selectLogo" /><span class="mt-1 block text-xs font-normal text-slate-400">{{ logoFile || 'Logo hiện tại: KidSpeak' }}</span></label>
        </div>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="mb-5 flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-700"><AdminIcon name="users" /></span><div><h3 class="font-bold text-slate-800">Cấu hình tài khoản</h3><p class="text-xs text-slate-400">Quyền đăng ký và đăng nhập</p></div></div>
        <div class="divide-y divide-slate-100">
          <label class="flex items-center justify-between gap-4 py-4"><span><span class="block text-sm font-semibold text-slate-700">Cho phép đăng ký</span><span class="mt-1 block text-xs text-slate-400">Người dùng mới có thể tạo tài khoản</span></span><input v-model="settings.allowRegistration" type="checkbox" class="h-5 w-5 accent-blue-600" /></label>
          <label class="flex items-center justify-between gap-4 py-4"><span><span class="block text-sm font-semibold text-slate-700">Cho phép đăng nhập</span><span class="mt-1 block text-xs text-slate-400">Cho phép tài khoản truy cập hệ thống</span></span><input v-model="settings.allowLogin" type="checkbox" class="h-5 w-5 accent-blue-600" /></label>
          <label class="flex items-center justify-between gap-4 py-4"><span><span class="block text-sm font-semibold text-slate-700">Xác thực tài khoản</span><span class="mt-1 block text-xs text-slate-400">Yêu cầu xác minh trước khi cấp quyền</span></span><input v-model="settings.requireVerification" type="checkbox" class="h-5 w-5 accent-blue-600" /></label>
        </div>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="mb-5 flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-violet-700"><AdminIcon name="roles" /></span><div><h3 class="font-bold text-slate-800">Cấu hình bảo mật</h3><p class="text-xs text-slate-400">Chính sách mật khẩu và phiên đăng nhập</p></div></div>
        <div class="grid gap-4 sm:grid-cols-2"><label class="block text-sm font-semibold text-slate-700">Độ dài mật khẩu tối thiểu<input v-model.number="settings.passwordLength" type="number" min="6" max="32" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal" /></label><label class="block text-sm font-semibold text-slate-700">Phiên đăng nhập (phút)<input v-model.number="settings.sessionMinutes" type="number" min="5" max="1440" class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal" /></label></div>
        <p class="mt-4 rounded-xl bg-blue-50 p-3 text-xs leading-5 text-blue-700">Khuyến nghị mật khẩu tối thiểu 8 ký tự và kết thúc phiên khi người dùng không hoạt động.</p>
      </article>

      <article class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div class="mb-5 flex items-center gap-3"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-50 text-rose-700"><AdminIcon name="settings" /></span><div><h3 class="font-bold text-slate-800">Cấu hình hệ thống</h3><p class="text-xs text-slate-400">Vận hành và thông báo</p></div></div>
        <div class="divide-y divide-slate-100">
          <label class="flex items-center justify-between gap-4 py-4"><span><span class="block text-sm font-semibold text-slate-700">Chế độ bảo trì</span><span class="mt-1 block text-xs text-slate-400">Tạm dừng truy cập của người dùng</span></span><input v-model="settings.maintenanceMode" type="checkbox" class="h-5 w-5 accent-rose-600" /></label>
          <label class="flex items-center justify-between gap-4 py-4"><span><span class="block text-sm font-semibold text-slate-700">Thông báo hệ thống</span><span class="mt-1 block text-xs text-slate-400">Cho phép gửi thông báo đến người dùng</span></span><input v-model="settings.systemNotifications" type="checkbox" class="h-5 w-5 accent-blue-600" /></label>
        </div>
      </article>
    </div>
    <p class="text-right text-xs text-slate-400">Cấu hình đang dùng: {{ savedSettings.systemName }} · Mock data lưu trong phiên làm việc</p>

    <AdminModal v-model="resetOpen" title="Khôi phục cấu hình mặc định" @submit="resetSettings"><p class="text-sm leading-6 text-slate-600">Các giá trị cấu hình sẽ được đưa về mặc định. Bạn có thể lưu lại sau khi khôi phục.</p><template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold" @click="resetOpen = false">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white">Khôi phục</button></template></AdminModal>
  </AdminPageShell>
</template>
