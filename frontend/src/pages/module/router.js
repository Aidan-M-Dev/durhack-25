import { createRouter, createWebHistory } from 'vue-router'
import ModulePage from './ModulePage.vue'

const routes = [
  {
    path: '/module/:moduleName',
    name: 'module',
    component: ModulePage,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
