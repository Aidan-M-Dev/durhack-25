import { createRouter, createWebHistory } from 'vue-router'
import ModulePage from '../pages/module/ModulePage.vue'
import SearchPage from '../pages/search/SearchPage.vue'

const routes = [
  {
    path: '/',
    name: 'search',
    component: SearchPage
  },
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
