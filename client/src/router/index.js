import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChapterView from '../views/ChapterView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/chapter/:id', name: 'chapter', component: ChapterView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router