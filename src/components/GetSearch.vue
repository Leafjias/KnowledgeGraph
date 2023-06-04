<template>
  <div>
    <input placeholder="请输入内容" type="text" v-model="inputValue">
    <el-button type="primary" @click="handleSubmit"><el-icon><Search/></el-icon>Search</el-button>
  </div>
</template>

<script>
import {Search} from "@element-plus/icons-vue"
export default {
  name: "GetSearch",
  components: {
      Search,
  },
  data(){
    return {
      inputValue: '',
    }
  },
  methods:{
    handleSubmit() {
      this.$emit('onSubmit', this.inputValue)
    }
  }
}
</script>
<style lang="less" scoped>
input {
  border: none;
  border-radius: 4px;
  outline: none;/*去除边框*/
  width: 200px;
  height: 30px;
  background-color: #ccc;
  opacity:0.4;    /*透明度*/
}
</style>
