<template>
<div>
  <h1>course</h1>
  {{name}}
  {{new_name}}
  <hr>
  {{try_again}}
</div>
</template>

<script>
    export default {
        name: "Course",
      data(){
          return {
            name : this.$store.state.name,
            new_name: this.$store.getters.new_new_name,
            try_again: '',
          }
      },
      // 方法执行完会改版数据但是不会刷新
      // methods: {
      //     my_click: function () {
      //       this.$store.commit("change_data", '到到')
      //     }
      // },
      // 能够监听到数据的改变能够实时跟新
      // computed: {
      //     name: function () {
      //       return  this.$store.state.name;
      //     }
      // }

      mounted(){
          let that = this;
          this.$axios.request({
            url: "http://127.0.0.1:8000/tryagain/",
            method: 'get',
            // data:
            // headers

          }).then(function (data) {
            // success do something~~
            that.try_again = data.data
          }).catch(function (data) {
            // fail do something~~
          })
          // 单纯的发get请求
          // this.$axios.get("url", {}).then()
      }

    }
</script>

<style scoped>

</style>
