import Vue from 'vue'
import Router from 'vue-router'
import Home from '../components/headers/Home'
import Course from '../components/headers/Course'
import Brief from '../components/CourseChildren/Brief'
import Chapter from '../components/CourseChildren/Chapter'
import Comment from '../components/CourseChildren/Comment'
import OftenAskQuestion from '../components/CourseChildren/OftenAskQuestion'
import CourseDetail from '../components/headers/CourseDetail'


Vue.use(Router);

export default new Router({
  mode: 'history',
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
    },
    {
      path: '/course/detail/:id',
      // 点击默认直接跳转到概要
      redirect: {name: 'brief'},
      name: 'detail',
      component: CourseDetail,
      children: [
        {
          path: 'brief',
          name: 'brief',
          component: Brief,
        },
        {
          path: 'chapter',
          name: 'chapter',
          component: Chapter,
        },
        {
          path: 'comment',
          name: 'comment',
          component: Comment,
        },
        {
          path: "often_ask_question",
          name: 'often_ask_question',
          component: OftenAskQuestion
        }
      ]
    }
  ]
})
