import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/headers/Home'
import Course from '../components/headers/Course'


Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/course',
      name: 'course',
      component: Course
    }
  ]
})
