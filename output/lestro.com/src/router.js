import Vue from 'vue'
import Router from 'vue-router'
import index from './views/index.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: index
    },
    {
      path: '/allProjects',
      name: 'allProjects',
      component: () => import('./views/allProjects.vue')
    },
    {
      path: '/project__inner',
      name: 'project__inner',
      component: () => import('./views/project__inner.vue')
    },
    {
      path: '*',
      name: 'index',
      component: () => import('./views/index.vue')
    }
  ]
})
