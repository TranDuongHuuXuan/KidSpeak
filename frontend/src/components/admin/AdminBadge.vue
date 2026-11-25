<script setup>
import { computed } from 'vue'

const props = defineProps({ status: { type: String, required: true } })

const badgeClass = computed(() => ({
  active: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  approved: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  activated: 'bg-blue-50 text-blue-700 ring-blue-600/15',
  pending: 'bg-amber-50 text-amber-700 ring-amber-600/20',
  rejected: 'bg-rose-50 text-rose-700 ring-rose-600/15',
  Active: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  Approved: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  Sent: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  Pending: 'bg-amber-50 text-amber-700 ring-amber-600/20',
  Draft: 'bg-slate-100 text-slate-600 ring-slate-500/15',
  Locked: 'bg-rose-50 text-rose-700 ring-rose-600/15',
  Rejected: 'bg-rose-50 text-rose-700 ring-rose-600/15',
}[props.status] || 'bg-slate-100 text-slate-600 ring-slate-500/15'))

const label = computed(() => ({
  active: 'Active',
  pending: 'Pending',
  approved: 'Approved',
  rejected: 'Rejected',
  activated: 'Activated',
  Active: 'Hoạt động',
  Pending: 'Chờ xử lý',
  Approved: 'Đã phê duyệt',
  Rejected: 'Từ chối',
  Locked: 'Đã khóa',
  Draft: 'Bản nháp',
  Sent: 'Đã gửi',
}[props.status] || props.status))
</script>

<template>
  <span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset" :class="badgeClass">
    <span class="h-1.5 w-1.5 rounded-full bg-current"></span>{{ label }}
  </span>
</template>
