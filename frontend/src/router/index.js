import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/',
    redirect: { name: 'Login' },
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
