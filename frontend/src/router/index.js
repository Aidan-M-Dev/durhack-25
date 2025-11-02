import { createRouter, createWebHistory } from 'vue-router'
import ModulePage from '../pages/module/ModulePage.vue'

const routes = [
  {
    path: '/module/:moduleName',
    name: 'module',
    component: ModulePage,
    props: true
  },
  {
    path: '/',
    redirect: '/module/CS101'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
