<template>
  <div>

    <div>

      <div>
        <h1>课程概述</h1>
        <p>
        {{course_detail.summary}}
      </p>
      </div>
      <div>
      <h1>可以根据不同的学习情况购买不一样的学习套餐哦！</h1>
      <p v-for="(price, index) in course_detail.price_policy" :key="index" @click="choicePrice(price.id)">{{price.valid_period}} 贝利
        {{price.price}}</p>
      <button>购买</button>
      <button @click="addShoppingCar">加入购物车</button>
    </div>


    <div>
      <h1>为什么学习这门课程</h1>
      <p>{{course_detail.why_study}}</p>
    </div>


    <div>

      <h1>你将获得的服务</h1>
      <p>{{course_detail.service}}</p>
    </div>


    <div>
      <h1>我将学到哪些内容？</h1>
      <p>{{course_detail.what_to_study_brief}}</p>
    </div>

    <div>
      <h1>大纲</h1>
      <div><span>{{course_detail.outline}}</span></div>
    </div>

      <div>
        <h1>此项目如何有助于我的职业生涯？</h1>
        <p>{{course_detail.career_improvement}}</p>
      </div>
      <div>
        <h1>课程先修要？</h1>
        <p>{{course_detail.prerequisite}}</p>
      </div>

       <div>
        <h1>推荐课程</h1>
        <p>{{course_detail.recommend_courses}}</p>
      </div>

      <div>
        <h1>课程讲师简介</h1>
        <p>{{course_detail.teachers}}</p>
      </div>

    </div>
</div>


</template>

<script>
  export default {
    name: "Brief",
    data() {
      return {
        course_detail: {},
        currentPrice: '',
      }
    },
    methods: {
      choicePrice: function (price_id) {
        this.currentPrice = price_id;
      },
      addShoppingCar: function () {
        // 加入购物车的请求在这里发
      }
    },
    mounted() {
      let course_id = this.$route.params.id;
      // 发送请求获取课程详细的所有数据
      let that = this;
      that.$axios.request({
        url: 'http://127.0.0.1:8000/api/course/detail/' + course_id,
        type: 'get',
      }).then(function (data) {
        if (data.status == 200) {
          let course_detail = data.data;
          console.log(course_detail);
          that.course_detail = course_detail;
          let headerInfo = {
            id: course_detail.id,
            title: course_detail.title,
            level: course_detail.level,
            study_num: course_detail.study_num,
            hours: course_detail.hours,
            video_brief_link: course_detail.video_brief_link,
            course_slogan: course_detail.course_slogan,
          };
          // 向仓库提价修改数据的事件
          that.$store.commit("detailHeaderHandler", headerInfo)
        }
      })
    }
  }
</script>

<style scoped>

</style>
