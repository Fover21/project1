<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :router="true">
      <el-menu-item index="/">首页</el-menu-item>
      <el-menu-item index="/course">免费课程</el-menu-item>
      <el-menu-item index="3">学位课程</el-menu-item>
      <el-menu-item index="4">智能题库</el-menu-item>
      <el-menu-item index="5">公开课</el-menu-item>
      <el-menu-item index="6">内部教材</el-menu-item>
      <el-menu-item index="7">老男孩教育</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
  export default {
    name: "MyHeader",
    data() {
      return {
        activeIndex: '1',
      };
    },
  }
</script>

<style scoped>

  .el-menu {
    display: flex;
    align-items: center;
    justify-content: center;
  }

</style>
