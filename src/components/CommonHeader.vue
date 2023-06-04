<template>
  <div class="header-container">
    <div class="l-content">
<!--      <el-button size="small" ><el-icon><Menu /></el-icon></el-button>-->
<!--      &lt;!&ndash;面包屑&ndash;&gt;-->
<!--      <span class="text">首页</span>-->
    </div>
  </div>
</template>

<script>
// import {Menu,} from "@element-plus/icons";
export default {
  name: "CommonHeader",
  // components: {
  //     Menu,
  //   },
}
</script>

<style lang="less" scoped>
  .header-container{
    background-color: #40424d;
    height: 70px;
    display: flex;
    justify-content: space-between;/*主轴上两端显示*/
    align-items: center; /*纵轴居中*/
    padding: 0 20px;
    .text {
      color: #fff;
      font-size: 14px;
      margin-left: 10px;
    }
  }
</style>