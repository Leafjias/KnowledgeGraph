<template>
  <el-menu default-active="1-4-1"
           class="el-menu-vertical-demo"
           background-color="#545c64"
           text-color="#fff"
           active-text-color="#ffd04b"
           :collapse="isCollapse">
    <h3>产业链全景信息系统</h3>
    <el-sub-menu index="1"><!--@相当于v-on，绑定一个事件-->
      <template #title>
        <el-icon><FullScreen /></el-icon>
        <span>产业链全景</span>
      </template>
      <el-menu-item-group>
        <el-menu-item @click="this.$router.push('/graph')" index="1-1">全景展示</el-menu-item>
        <el-menu-item @click="this.$router.push('/dynamic')" index="1-2">动态演化</el-menu-item>
        <el-menu-item @click="this.$router.push('/map')" index="1-3">地图分布</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
    <el-sub-menu index="2"><!--@相当于v-on，绑定一个事件-->
      <template #title>
        <el-icon><Search /></el-icon>
        <span>结点查找</span>
      </template>
      <el-menu-item-group>
        <el-menu-item @click="this.$router.push('/profile')" index="2-1">企业画像</el-menu-item>
        <el-menu-item @click="this.$router.push('/position')" index="2-2">产业链定位</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
    <el-sub-menu index="3"><!--@相当于v-on，绑定一个事件-->
      <template #title>
        <el-icon><Search /></el-icon>
        <span>关系查找</span>
      </template>
      <el-menu-item-group>
        <el-menu-item @click="this.$router.push('/connection')" index="3-1">联系探索</el-menu-item>
        <el-menu-item @click="this.$router.push('/association')" index="3-2">跨界关联</el-menu-item>
        <el-menu-item @click="this.$router.push('/path')" index="3-3">路径分析</el-menu-item>
      </el-menu-item-group>
    </el-sub-menu>
  </el-menu>
</template>
<style lang="less" scoped>
/*scoped表示只作用在该界面组件*/
  .el-menu {
    height: 100vh;/*填满页面*/
    border-right: none;
    h3 {
      color: #fff;
      background-color: #545c64;
      text-align: center;
      line-height: 48px;
      font-size: 20px;
      font-weight: 400;
    }
  }
</style>
<script>
  //首先是导入图标们，要用哪个就导入哪个
  import {Search,FullScreen,} from "@element-plus/icons";
  //其次是写入components中
  export default {
    components: {
      Search,
      FullScreen,
    },
    data() {
      return {
        isCollapse: false,
      };
    },
    methods: { //类似于函数的实现

    }
  }
</script>
