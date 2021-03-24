import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginPage from '@/components/loginPage'
import mainPage from '@/components/mainPage'
import tempItemPage from '@/components/tempItemPage'
import ctrlPage from '@/components/ctrlPage'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [
    {
      path: '/',
      component: LoginPage
    },
    {
      name: 'mainPage',
      path: '/mainPage',
      component: mainPage,
      props: (route)=>{return route.params;},
      children: [
        { path: 'shortItem', component: tempItemPage}, 
        //{ path: 'baselineItem', component: tempItemPage},
        { path: 'contrlBroad', component: ctrlPage}
      ]
    }
  ]
})
