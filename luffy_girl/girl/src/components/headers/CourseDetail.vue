<template>
  <div>
    <div>
      <h1>课程详情组件</h1>

      <div style="border: solid 1px red; height: 300px">
        {{header_info}}
      </div>

      <router-link :to="{name: 'brief'}">课程概述</router-link>
      <router-link :to="{name: 'chapter'}">课程章节</router-link>
      <router-link :to="{name: 'comment'}">课程评论</router-link>
      <router-link :to="{name: 'often_ask_question'}">常见问题</router-link>
      <router-view class="content"></router-view>
    </div>
  </div>

</template>

<script>
  export default {
    name: "CourseDetail",
    computed: {
      header_info: function () {
        return this.$store.state.detail_header
      }
    }
  }
</script>

<style scoped>
.content {
  overflow: scroll;
  margin-bottom: 100px;
}
</style>
