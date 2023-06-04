<template>
  <div>
    <el-container>
      <!--侧边菜单栏-->
      <el-aside width="200px">
        <common-aside />
      </el-aside>
      <el-container>
        <!--顶部导航栏-->
        <el-header>
          <common-header />
        </el-header>
        <el-main>
          <!-- 子路由出口 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import CommonAside from "../components/CommonAside.vue"
import CommonHeader from "../components/CommonHeader.vue";
export default {
  name: "MainPage",
  components:{
    CommonAside,
    CommonHeader
  }
}
</script>

<style>
  .el-header{
    padding: 0;
  }
  .el-main{
    padding: 0;
    position: absolute;
    left: 200px;
    right: 0;
    top:70px;
    bottom: 0;
    overflow-y: scroll;/*固定左侧和顶部，使main溢出部分滚轮滑动显示*/
  }
</style>