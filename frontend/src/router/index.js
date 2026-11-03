import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import RegisterView from '../views/RegisterView.vue'
import AppHeader from '../components/common/AppHeader.vue'
import AppFooter from '../components/common/Footer.vue'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import GuestLearningView from '../views/GuestLearningView.vue'
import AdminLayout from '../layout/AdminLayout.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'
import AdminRoles from '../views/admin/AdminRoles.vue'
import AdminVerification from '../views/admin/AdminVerification.vue'
import AdminLessons from '../views/admin/AdminLessons.vue'
import AdminNotifications from '../views/admin/AdminNotifications.vue'
import AdminSettings from '../views/admin/AdminSettings.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { title: 'Trang chủ' },
  },
  {
    path: '/about',
    name: 'About',
    component: AboutView,
    meta: { title: 'Giới thiệu & hướng dẫn' },
  },
  {
    path: '/guest-learning',
    name: 'GuestLearning',
    component: GuestLearningView,
    meta: { title: 'Khám phá bài học' },
  },
  {
    path: '/guest-learning/:topicSlug',
    name: 'GuestLearningTopic',
    component: GuestLearningView,
    meta: { title: 'Luyện phát âm' },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { title: 'Đăng nhập' },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { title: 'Đăng ký' },
  },
  {
    path: '/admin',
    component: AdminLayout,
    redirect: { name: 'AdminDashboard' },
    children: [
      { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { title: 'Tổng quan' } },
      { path: 'users', name: 'AdminUsers', component: AdminUsers, meta: { title: 'Quản lý người dùng' } },
      { path: 'roles', name: 'AdminRoles', component: AdminRoles, meta: { title: 'Quản lý phân quyền' } },
      { path: 'verification', name: 'AdminVerification', component: AdminVerification, meta: { title: 'Xác thực giáo viên' } },
      { path: 'lessons', name: 'AdminLessons', component: AdminLessons, meta: { title: 'Kiểm duyệt bài học' } },
      { path: 'notifications', name: 'AdminNotifications', component: AdminNotifications, meta: { title: 'Thông báo hệ thống' } },
      { path: 'settings', name: 'AdminSettings', component: AdminSettings, meta: { title: 'Cấu hình hệ thống' } },
    ],
  },
  {
    path: '/header-preview',
    name: 'HeaderPreview',
    component: AppHeader,
    meta: { title: 'Xem trước Header' },
  },
  {
    path: '/footer-preview',
    name: 'FooterPreview',
    component: AppFooter,
    meta: { title: 'Xem trước Footer' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
    meta: { title: 'Không tìm thấy trang' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition ?? { top: 0 }
  },
})

router.beforeEach((to) => {
  document.title = to.meta.title
    ? `${to.meta.title} | KidSpeak`
    : 'KidSpeak'
})

export default router
