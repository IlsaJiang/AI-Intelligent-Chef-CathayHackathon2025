import { createRouter, createWebHistory } from 'vue-router'
import pinia from '@/stores'
import { useAuthStore } from '@/stores/auth'
import Home from '@/pages/Home.vue'
import Menu from '@/pages/Menu.vue'
import DishDetail from '@/pages/DishDetail.vue'
import Survey from '@/pages/Survey.vue'
import Preselect from '@/pages/Preselect.vue'
import MyFeedback from '@/pages/MyFeedback.vue'

const routes = [
  { path: '/', component: Home, meta: { requiresAuth: true } },
  { path: '/menu', component: Menu, meta: { requiresAuth: true } },
  { path: '/dish/:id', component: DishDetail, meta: { requiresAuth: true } },
  { path: '/survey', component: Survey, meta: { requiresAuth: true } },
  { path: '/my-feedback', component: MyFeedback, meta: { requiresAuth: true } },
  { path: '/preselect', component: Preselect, meta: { requiresAuth: true } },
  { path: '/chef', component: () => import('@/pages/AIChef.vue'), meta: { requiresAuth: false } },
  { path: '/ar', component: () => import('@/pages/ArView.vue'), meta: { requiresAuth: true } },
  { path: '/auth', component: () => import('@/pages/Auth.vue'), meta: { requiresAuth: false } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore(pinia)
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth !== false)

  if (requiresAuth) {
    const ok = await authStore.ensureSession()
    if (!ok) {
      next({ path: '/auth', query: { redirect: to.fullPath } })
      return
    }
  }

  if (to.path === '/auth' && authStore.isAuthenticated) {
    const REWARD_KEY = 'cx_reward'
    const hasReward = localStorage.getItem(REWARD_KEY) !== null || sessionStorage.getItem(REWARD_KEY) !== null
    if (!hasReward) {
      next({ path: (typeof to.query.redirect === 'string' && to.query.redirect) || '/' })
      return
    }
  }

  next()
})

export default router
