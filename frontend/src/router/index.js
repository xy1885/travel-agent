import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlanView from '../views/PlanView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/plan', component: PlanView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})