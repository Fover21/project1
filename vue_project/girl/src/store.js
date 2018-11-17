import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex);

export default new Vuex.Store({
  // this.$store.state.name    拿数据
  state: {
    name: '1',
  },
  // 对state中的数据进行处理
  // this.$store.getters.new_name    拿数据
  getters: {
    new_name: function (state) {
      return state.name + 'xxx';
    },
    new_new_name: function (state, getters) {
      return getters.new_name + '000';
    },
  },
  mutations: {
    change_data: function (state, data) {
      // 自己处理change_data事件的
      state.name = data;
    }
  }
})
