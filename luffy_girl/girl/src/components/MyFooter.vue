<template>

  <div class="footer">
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" background-color="black">
      <el-menu-item index="1">关于我们</el-menu-item>
      <el-menu-item index="2">联系我们</el-menu-item>
      <el-menu-item index="3">商务合作</el-menu-item>
      <el-menu-item index="4">帮助中心</el-menu-item>
      <el-menu-item index="5">意见反馈</el-menu-item>
      <el-menu-item index="6">新手指南</el-menu-item>
    </el-menu>
  </div>

</template>

<script>
  export default {
    name: "MyFooter"
  }
</script>

<style scoped>
  .el-menu {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
  }
</style>
