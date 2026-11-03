import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import RegisterView from '../views/RegisterView.vue'
import AppHeader from '../components/common/AppHeader.vue'
import AppFooter from '../components/common/Footer.vue'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { title: 'Trang chủ' },
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
