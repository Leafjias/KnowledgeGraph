<template>
  <!-- 主路由出口 -->
  <router-view></router-view>
</template>

<script>
  export default {
    name:'App'
  }
</script>

<style lang="less">
  html,body,h3 {
    margin: 0;
    padding: 0;
  }/*CommonAside.vue中侧边顶上文字去除padding产生的空*/
</style>
