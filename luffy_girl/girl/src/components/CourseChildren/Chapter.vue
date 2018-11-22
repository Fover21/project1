<template>

  <div>
    <h1>这里是课程章节</h1>

    <p>{{course_chapter}}</p>
  </div>

</template>

<script>
    export default {
      name: "Chapter",
      data() {
        return {
          course_chapter: {}
        }
      },
      mounted() {
        // 发送请求获取课程详细的所有数据
        let that = this;
        that.$axios.request({
          url: 'http://127.0.0.1:8000/api/course/course_chapter',
          type: 'get',
        }).then(function (data) {
            that.course_chapter = data.data;
        })
      }
    }
</script>

<style scoped>

</style>
