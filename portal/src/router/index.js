import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/search-services',
      name: 'services',
      component: () => import('../views/ServicesView.vue')
    },
    {
      path: '/service/:id',
      name: 'service',
      component: () => import('../views/ServiceShowView.vue'),
      props: {
        id: Number
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/sign-up',
      name: 'sign-up',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/create-order/:id',
      name: 'create-order',
      component: () => import('../views/CreateOrderView.vue')
    },
    {
      path: '/service-orders',
      name: 'service-orders',
      component: () => import('../views/IndexOrdersView.vue')
    },
    {
      path: '/service-order/:id',
      name: 'cervice-order',
      component: () => import('../views/ShowOrderView.vue')
    },
    {
      path: '/stadistics',
      name: 'stadistics',
      component: () => import('../views/StadisticsView.vue')
    }
  ]
})

export default router
