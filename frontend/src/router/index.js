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
import ExpertLayout from '../layout/ExpertLayout.vue'
import ExpertDashboard from '../views/expert/ExpertDashboard.vue'
import ExpertWorkspace from '../views/expert/ExpertWorkspace.vue'
import StudentWorkspace from '../views/student/StudentWorkspace.vue'
import StudentResults from '../views/student/StudentResults.vue'
import NewsPage from '../views/news/NewsPage.vue'
import NewsDetailPage from '../views/news/NewsDetailPage.vue'

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
    path: '/news',
    name: 'News',
    component: NewsPage,
    meta: { title: 'Tin tức & Cập nhật' },
  },
  {
    path: '/news/:slug',
    name: 'NewsDetail',
    component: NewsDetailPage,
    meta: { title: 'Bài viết' },
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
    path: '/expert',
    component: ExpertLayout,
    redirect: { name: 'ExpertDashboard' },
    children: [
      { path: 'dashboard', name: 'ExpertDashboard', component: ExpertDashboard, meta: { title: 'Tổng quan', role: 'Expert' } },
      { path: 'topics', name: 'ExpertTopics', component: ExpertWorkspace, meta: { title: 'Quản lý chủ đề', expertSection: 'topics', role: 'Expert' } },
      { path: 'vocabulary', name: 'ExpertVocabulary', component: ExpertWorkspace, meta: { title: 'Quản lý từ vựng', expertSection: 'vocabulary', role: 'Expert' } },
      { path: 'learning-paths', name: 'ExpertPaths', component: ExpertWorkspace, meta: { title: 'Lộ trình học tập', expertSection: 'paths', role: 'Expert' } },
      { path: 'progress', name: 'ExpertProgress', component: ExpertWorkspace, meta: { title: 'Tiến độ học tập', expertSection: 'progress', role: 'Expert' } },
      { path: 'students', name: 'ExpertStudents', component: ExpertWorkspace, meta: { title: 'Theo dõi học viên', expertSection: 'students', role: 'Expert' } },
      { path: 'resources', name: 'ExpertResources', component: ExpertWorkspace, meta: { title: 'Kho học liệu', expertSection: 'resources', role: 'Expert' } },
      { path: 'messages', name: 'ExpertMessages', component: ExpertWorkspace, meta: { title: 'Tin nhắn', expertSection: 'messages', role: 'Expert' } },
      { path: 'profile', name: 'ExpertProfile', component: ExpertWorkspace, meta: { title: 'Hồ sơ cá nhân', expertSection: 'profile', role: 'Expert' } },
      { path: 'settings', name: 'ExpertSettings', component: ExpertWorkspace, meta: { title: 'Cài đặt', expertSection: 'settings', role: 'Expert' } },
    ],
  },
  {
    path: '/student',
    component: () => import('../layout/StudentLayout.vue'),
    redirect: { name: 'StudentDashboard' },
    children: [
      { path: 'dashboard', name: 'StudentDashboard', component: () => import('../views/student/StudentDashboard.vue'), meta: { title: 'Tổng quan', role: 'Student' } },
      { path: 'topics', name: 'StudentTopics', component: () => import('../views/student/StudentTopics.vue'), meta: { title: 'Chủ đề học tập', role: 'Student' } },
      { path: 'topics/:topicSlug', name: 'StudentTopicDetail', component: () => import('../views/student/StudentTopicDetail.vue'), meta: { title: 'Chi tiết chủ đề', role: 'Student' } },
      { path: 'topics/:topicSlug/practice/:wordId', name: 'StudentPronunciationPractice', component: () => import('../views/student/StudentPronunciation.vue'), meta: { title: 'Luyện phát âm', role: 'Student' } },
      { path: 'pronunciation', name: 'StudentPronunciation', component: () => import('../views/student/StudentTopics.vue'), meta: { title: 'Luyện phát âm', role: 'Student' } },
      { path: 'results', name: 'StudentResults', component: StudentResults, meta: { title: 'Kết quả học tập', role: 'Student' } },
      { path: 'achievements', name: 'StudentAchievements', component: StudentWorkspace, meta: { title: 'Thành tích', studentSection: 'achievements', role: 'Student' } },
      { path: 'messages', name: 'StudentMessages', component: () => import('../views/student/StudentMessages.vue'), meta: { title: 'Tin nhắn', studentSection: 'messages', role: 'Student' } },
      { path: 'profile', name: 'StudentProfile', component: () => import('../views/student/StudentProfile.vue'), meta: { title: 'Hồ sơ cá nhân', studentSection: 'profile', role: 'Student' } },
    ],
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
