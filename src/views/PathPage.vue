<template>
  <div class="container">
    <div class="inputs">
      <input placeholder="请输入起点" type="text" v-model="input_start">
      <input placeholder="请输入终点" type="text" v-model="input_end">
      <el-button type="primary" @click="updateGraph"><el-icon><Search/></el-icon>查询</el-button>
    </div>
    <div class="indicator">
      <div class="list_color" v-for="(name, index) in names" :key="index">
        <span :style="{ backgroundColor: colors[index] }">{{ name }}</span>
      </div>
    </div>
    <svg>
      <text x="50%" y="8%" dominant-baseline="middle" text-anchor="middle" font-size="21">结点寻径图谱</text>
      <force-graph :url="api1"/>
    </svg>
    <div class="checkboxes">
      <el-checkbox v-model="ll" label="环节与环节" size="large"/>
      <el-checkbox v-model="lc" label="环节与公司" size="large"/>
      <el-checkbox v-model="lp" label="环节与产品" size="large"/>
      <el-checkbox v-model="cc" label="公司与公司" size="large"/>
      <el-checkbox v-model="cp" label="公司与产品" size="large"/>
      <el-checkbox v-model="cn" label="公司与新闻" size="large"/>
      <el-checkbox v-model="pp" label="产品与产品" size="large"/>
    </div>
  </div>
</template>
<script>
import {Search} from "@element-plus/icons-vue";
import ForceGraph from "@/components/ForceGraph.vue";
// import {ElLoading} from "element-plus";

export default {
  name: "ThirdPage",
  components: {
    ForceGraph,
    Search,
  },
  data() {
    return {
      //http://192.168.31.146
      api1: "http://127.0.3.1:5050/datas/find_path?start=&end=&ll=True&lc=True&lp=True&cc=True&cp=True&cn=True&pp=True",
      names: ["环节", "公司", "产品", "新闻"],
      colors: ["#aaaaff", '#f1662b', '#FFC0CB', "#0290c4"],
      ll: true,
      lc: true,
      lp: true,
      cc: true,
      cp: true,
      cn: true,
      pp: true,
      input_start: "",
      input_end: "",
    };
  },
  methods: {
    updateGraph() {
      // const loading = ElLoading.service({
      //   lock: true,
      //   text: 'Loading',
      //   background: 'rgba(0, 0, 0, 0.7)',
      // })
      const params = {
        start: this.input_start,
        end: this.input_end,
        ll: this.ll,
        lc: this.lc,
        lp: this.lp,
        cc: this.cc,
        cp: this.cp,
        cn: this.cn,
        pp: this.pp,
      };
      const queryString = Object.keys(params)
          .map((key) => key + "=" + params[key])
          .join("&");
      //http://192.168.31.146
      this.api1 = "http://127.0.3.1:5050/datas/find_path?" + queryString;
      console.log("new_api1=", this.api1);
      // loading.close();
    },
  },
}
</script>

<style lang="less" scoped>
/*输入*/
.inputs {
  display: inline-block;
  margin-left: 60px;
  margin-top: 10px;
  input {
    margin-left: 30px;
    border: none;
    border-radius: 4px;
    outline: none;
    width: 160px;
    height: 30px;
    background-color: #ccc;
    opacity: 0.4;
  }
}
/*结点颜色说明*/
.indicator {
  display: inline-block;
  margin-left: 200px;
  .list_color {
    display: inline-block;
    margin-left: 40px;
    text-align: center;
    gap: 5px;
    color: #eeeeee;
    font-size: 16px;
    span {
      display: inline-block;
      width: 50px;
      height: 22px;
    }
  }
}
/*图谱展示区*/
svg {
  width: 1200px;
  height: 565px;
  background-color: #eee;
  margin-left: 40px;
  margin-top: 10px;
}
/*复选框*/
.checkboxes {
  margin-top: 5px;
  margin-left: 180px;
}
</style>
