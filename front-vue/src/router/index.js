import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/components/login'
import mainPage from '@/components/mainPage'
import tempItemPage from '@/components/tempItemPage'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      component: Login
    },
    {
      path: '/mainPage',
      component: mainPage,
      props: true,
      children: [
        { path: 'shortItem', component: tempItemPage, props: true },
        { path: 'baselineItem', component: tempItemPage, props: true },
        { path: 'contrlBroad', component: tempItemPage, props: true }
      ]
    }
  ]
})
