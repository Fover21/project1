<template>
  <div id="app">

    <MyHeader></MyHeader>
    <router-view></router-view>
    <MyFooter></MyFooter>
  </div>
</template>

<script>
  import MyHeader from "./components/MyHeader"
  import MyFooter from "./components/MyFooter"
export default {
  name: 'App',
  components: {
    MyHeader,
    MyFooter,
  }
}
</script>

<style>
  body {
    margin: 0;
    padding: 0;
  }
</style>
