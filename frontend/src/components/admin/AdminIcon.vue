<script setup>
import {
  BadgeCheck,
  Bell,
  BookOpen,
  Check,
  ChevronRight,
  Clock,
  Eye,
  LayoutDashboard,
  Lock,
  LockOpen,
  LogOut,
  Menu,
  Pencil,
  Plus,
  Search,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  Users,
  X,
} from '@lucide/vue'

defineProps({
  name: { type: String, required: true },
  size: { type: Number, default: 20 },
})

const icons = {
  dashboard: LayoutDashboard,
  users: Users,
  roles: ShieldCheck,
  verify: BadgeCheck,
  lessons: BookOpen,
  bell: Bell,
  settings: Settings,
  logout: LogOut,
  search: Search,
  plus: Plus,
  edit: Pencil,
  eye: Eye,
  lock: Lock,
  unlock: LockOpen,
  check: Check,
  close: X,
  menu: Menu,
  arrow: ChevronRight,
  filter: SlidersHorizontal,
  clock: Clock,
}
</script>

<template>
  <component :is="icons[name] || Clock" :size="size" :stroke-width="1.8" aria-hidden="true" />
</template>
