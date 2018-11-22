<template>
  <div class="course">
    <div class="container clearfix">
      <ul class="coursebox">
        <li :class="{active: index==currentIndex}" v-for="(item, index) in categoryList" :key="item.id"
            @click="clickCategory(index, item.id)">{{item.title}}
        </li>
      </ul>
    </div>
      <div class="courseList">
     <div class="detail" v-for='(item, index)  in courseList' :key="item.id" @click="detailHandler(item.id)">
        <div class="head">
          <img :src="item.course_img" alt=" " class="backImg">
          <b class="mask" :style="{background: colors[index]}"></b>
          <p>{{item.title}}</p>
        </div>
       <div class="content">
         <p>{{item.brief}}</p>
         <div class="content-detail">
                  <div>
                          <span>{{item.study_num}}人学习</span>
                           <span>{{item.level}}</span>
                           <span class="span3" v-if = 'item.is_free'>
                              <span class="s">{{item.price}}</span>
                              <span  class="t">免费</span>
                        </span>
                        <span class="span4" v-else>{{item.price}}</span>
                  </div>

                </div>
       </div>
     </div>
    </div>
  </div>



</template>

<script>
  export default {
    name: "Course",
    data() {
      return {
        categoryList: [],
        currentIndex: 0,
        courseList: [],
        colors:['#4AB2BF','#1895C6','#4C87E0','#A361D9','#F7AE6A','#FF14A0','#61F0E1','#6282A7','#27998E','#3C74CC','#A463DA','#F0A257','#DD4B7A','#59C6BD','#617FA1','#1B92C3','#30A297','#3B73CB','#9E57CA','#A463DA','#1895C6','#A361D9','#FF14A0']
      }
    },
    methods: {
      clickCategory: function (index, id) {
        this.currentIndex = index;
        // 点击每个分类获取分类好的所有课程
        this.get_course(id);
      },
      get_course: function (id) {
        let that = this;
        this.$axios.request({
          url: 'http://127.0.0.1:8000/api/course/?category_id=' + id,
          method: 'get',
        }).then(function (data) {
          if (data.status == 200) {
            that.courseList = data.data
          }
        })
      },
      detailHandler: function (course_id) {
        this.$router.push({name: 'detail', params: {id: course_id}})
      },
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

    mounted() {
      let that = this;
      this.$axios.request({
        url: "http://127.0.0.1:8000/api/course/category",
        method: 'get',
        // data:
        // headers

      }).then(function (data) {
        // success do something~~
        if (data.status == 200) {
          that.categoryList = data.data;
          that.categoryList.unshift({id: 0, title: '全部'})
        }
      }).catch(function (data) {
        // fail do something~~
      });
      // 单纯的发get请求
      // this.$axios.get("url", {}).then()
      this.get_course(0)
    }

  }
</script>

<style scoped>
  .course {
    width: 100%;
    height: 1000px;
    background: #f3f3f3;
  }

  .coursebox {
    padding: 24px 0;
    font-size: 16px;
    color: #666;
    letter-spacing: .41px;
    font-family: PingFangSC-Regular;
    overflow: hidden;
  }

  ul li {
    float: left;
    margin-right: 24px;
    cursor: pointer;
  }

  ul li.active {
    color: #00b4e4;
  }

  .head img {
    width: 100px;
    height: 100px;
  }

  .courseList{
	width: 100%;
	height: auto;
	overflow: hidden;
}
.detail{
	float: left;
	width: 248px;
	height: auto;
	margin-right: 16px;
	margin-bottom: 30px;
	position: relative;
	padding: 0 20px;
	background: #fff;
   	 box-shadow: 0 2px 6px 0 #e8e8e8;
   	 transition: all .2s linear;
   	 cursor: pointer;
}
.detail:hover{
	box-shadow: 0 8px 15px rgba(0,0,0,.15);
    	transform: translate3d(0,-3px,0);
}
.detail:nth-of-type(4n){
	margin-right: 0;
}
.head{
	width: 100%;

    	height: 144px;
}
.detail .head img{
	   width: 100%;
	    height: 144px;
	    position: absolute;
	    left: 0;
	    top: 0;
}
.detail .head b{
     width: 100%;
    height: 144px;
    position: absolute;
    left: 0;
    top: 0;
    opacity: .9;
    background: #56CBC4;
}
.detail .head p{
	position: absolute;
	width: 248px;
	height:144px;
	left: 0;
	top: 0;
	text-align: center;
	font-family: PingFangSC-Medium;
	font-size: 24px;
	color: #fff;
	overflow: hidden;
	display: flex;
	align-items:center;
	padding: 0 20px;
	justify-content: space-around;
}
.content{
    width: 248px;

    height: 118px;
    padding-top: 30px;

}
.content p{
     width: 100%;
    height: 40px;
    font-size: 14px;
    color: #666;
    cursor: pointer;
    letter-spacing: .6px;
    margin-bottom: 20px;
    font-family: PingFangSC-Regular;
    overflow: hidden;
}
.content-detail{
	width: 100%;
	height: 40px;
	line-height: 40px;
	position: relative;

}
.content-detail .span3{
	position: absolute;
	right: 0;

}
.content-detail .span3 .s{
	text-decoration: line-through;
}
.content-detail .span4{
	/*margin-left: 100px;*/
	position: absolute;
	right: 0;
	color: #FC0107;
}
.content-detail .span3 .t{
	color: #000;
	margin-left: 5px;
	text-decoration: none !important;
	color: #FC0107;
}
</style>
