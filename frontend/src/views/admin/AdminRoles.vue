<script setup>
import { computed, reactive, ref } from 'vue'
import AdminIcon from '../../components/admin/AdminIcon.vue'
import AdminModal from '../../components/admin/AdminModal.vue'
import AdminPageShell from '../../components/admin/AdminPageShell.vue'
import { adminData, notify } from '../../data/adminMockData'

const permissionList = [
  { key: 'users', label: 'Quản lý người dùng', description: 'Xem, thêm và cập nhật tài khoản' },
  { key: 'lessons', label: 'Quản lý bài học', description: 'Tạo, chỉnh sửa và gửi bài học' },
  { key: 'viewLessons', label: 'Xem bài học', description: 'Truy cập nội dung bài học' },
  { key: 'notifications', label: 'Quản lý thông báo', description: 'Soạn và gửi thông báo hệ thống' },
]
const modalOpen = ref(false)
const deleteTarget = ref(null)
const editingRole = ref(null)
const form = reactive({ name: '', description: '' })
const permissionDefaults = () => Object.fromEntries(permissionList.map(({ key }) => [key, false]))
const roleUserCount = (role) => adminData.users.filter((user) => user.role === role.name).length
const roleTotal = computed(() => adminData.roles.length)

function openRole(role = null) {
  editingRole.value = role
  Object.assign(form, role ? { name: role.name, description: role.description } : { name: '', description: '' })
  modalOpen.value = true
}

function saveRole() {
  if (editingRole.value) {
    const previousName = editingRole.value.name
    Object.assign(editingRole.value, { name: form.name, description: form.description })
    if (previousName !== form.name) {
      adminData.users.forEach((user) => {
        if (user.role === previousName) user.role = form.name
      })
    }
    notify('Đã cập nhật vai trò.')
  } else {
    adminData.roles.push({ id: Math.max(0, ...adminData.roles.map((role) => role.id)) + 1, name: form.name, description: form.description, permissions: permissionDefaults() })
    notify('Đã thêm vai trò mới.')
  }
  modalOpen.value = false
}

function deleteRole() {
  if (!deleteTarget.value) return
  if (roleUserCount(deleteTarget.value) > 0) {
    notify('Không thể xóa vai trò đang được người dùng sử dụng.')
    deleteTarget.value = null
    return
  }
  adminData.roles.splice(adminData.roles.indexOf(deleteTarget.value), 1)
  deleteTarget.value = null
  notify('Đã xóa vai trò.')
}
</script>

<template>
  <AdminPageShell title="Quản lý phân quyền" description="Thiết lập vai trò và phạm vi quyền hạn cho từng nhóm người dùng.">
    <template #actions><button type="button" class="inline-flex items-center gap-2 rounded-xl bg-admin-cta px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700" @click="openRole()"><AdminIcon name="plus" :size="18" />Thêm vai trò</button></template>

    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <article v-for="role in adminData.roles" :key="role.id" class="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        <div class="flex items-center justify-between"><span class="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-admin-cta"><AdminIcon name="roles" /></span><div class="flex gap-1"><button type="button" class="rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700" aria-label="Sửa vai trò" @click="openRole(role)"><AdminIcon name="edit" :size="17" /></button><button v-if="role.id > 4" type="button" class="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600" aria-label="Xóa vai trò" @click="deleteTarget = role"><AdminIcon name="close" :size="17" /></button></div></div>
        <h3 class="mt-4 font-bold text-slate-800">{{ role.name }}</h3><p class="mt-1 min-h-10 text-xs leading-5 text-slate-500">{{ role.description }}</p>
        <div class="mt-4 flex items-center justify-between border-t border-slate-100 pt-3"><span class="text-xs text-slate-400">Người dùng</span><span class="text-sm font-bold text-slate-700">{{ roleUserCount(role) }}</span></div>
      </article>
      <div v-if="!roleTotal" class="rounded-2xl border border-dashed border-slate-300 p-8 text-center text-sm text-slate-500">Chưa có vai trò nào.</div>
    </div>

    <article class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div class="border-b border-slate-100 p-5"><h3 class="font-bold text-slate-800">Ma trận quyền hạn</h3><p class="mt-1 text-xs text-slate-500">Bật hoặc tắt quyền trực tiếp cho từng vai trò.</p></div>
      <div class="overflow-x-auto"><table class="w-full min-w-[720px] text-left text-sm">
        <thead class="bg-slate-50 text-xs font-semibold text-slate-500"><tr><th class="px-5 py-4">Chức năng</th><th v-for="role in adminData.roles" :key="role.id" class="px-4 py-4 text-center">{{ role.name }}</th></tr></thead>
        <tbody class="divide-y divide-slate-100">
          <tr v-for="permission in permissionList" :key="permission.key">
            <td class="px-5 py-4"><p class="font-semibold text-slate-700">{{ permission.label }}</p><p class="mt-0.5 text-xs text-slate-400">{{ permission.description }}</p></td>
            <td v-for="role in adminData.roles" :key="role.id" class="px-4 py-4 text-center"><label class="inline-flex cursor-pointer items-center justify-center"><input v-model="role.permissions[permission.key]" type="checkbox" class="peer sr-only" :aria-label="`${permission.label}: ${role.name}`" /><span class="flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 bg-white text-transparent transition peer-checked:border-emerald-500 peer-checked:bg-emerald-500 peer-checked:text-white peer-focus-visible:ring-2 peer-focus-visible:ring-blue-300"><AdminIcon name="check" :size="16" /></span></label></td>
          </tr>
        </tbody>
      </table></div>
    </article>

    <AdminModal v-model="modalOpen" :title="editingRole ? 'Chỉnh sửa vai trò' : 'Thêm vai trò'" @submit="saveRole">
      <div class="space-y-4"><label class="block text-sm font-semibold">Tên vai trò<input v-model.trim="form.name" required class="mt-1.5 h-11 w-full rounded-xl border border-slate-200 px-3 font-normal outline-none focus:border-admin-cta" placeholder="Ví dụ: Moderator" /></label><label class="block text-sm font-semibold">Mô tả<textarea v-model.trim="form.description" rows="3" class="mt-1.5 w-full rounded-xl border border-slate-200 p-3 font-normal outline-none focus:border-admin-cta" placeholder="Mô tả vai trò..." /></label></div>
    </AdminModal>
    <AdminModal :model-value="Boolean(deleteTarget)" title="Xác nhận xóa vai trò" @update:model-value="deleteTarget = null" @submit="deleteRole">
      <p class="text-sm leading-6 text-slate-600">Bạn có chắc muốn xóa vai trò <strong>{{ deleteTarget?.name }}</strong>? Thao tác này không thể hoàn tác.</p>
      <template #actions><button type="button" class="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-semibold" @click="deleteTarget = null">Hủy</button><button type="submit" class="rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700">Xóa vai trò</button></template>
    </AdminModal>
  </AdminPageShell>
</template>
