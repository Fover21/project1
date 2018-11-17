// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from "./store"
import axios from 'axios'

// 使用element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI);

// 全局的（一个一个比较麻烦）
// axios.request({
//   url: XXX,
//   method: "get"
// });

// 通过使用原型链 这样所有的组件都可以通过$axios去访问了
Vue.prototype.$axios = axios;


Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
});
