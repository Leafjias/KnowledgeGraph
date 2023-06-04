<template>
  <div class="check_box">
    <el-checkbox v-model="isProduct" label="产品" size="large"/>
    <el-checkbox v-model="isLink" label="产业链环节" size="large"/>
  </div>
  <div class="search">
    <get-search @onSubmit="handleInputSubmit"/>
  </div>
  <div class="indicator">
    <div class="list_color" v-for="(name, index) in names" :key="index">
      <span :style="{ backgroundColor: colors[index] }">{{ name }}</span>
    </div>
  </div>
  <svg class="s1">
<!--    <text-->
<!--        x="50%"-->
<!--        y="10%"-->
<!--        dominant-baseline="middle"-->
<!--        text-anchor="middle"-->
<!--        font-size="16"-->
<!--    >-->
<!--      生成包含搜索节点的一条完整产业链-->
<!--    </text>-->
    <force-graph1 :url="api1" :product="isProduct" :link="isLink" :name="search_input"/>
  </svg>
</template>

<script>
import GetSearch from "../components/GetSearch.vue";
import ForceGraph1 from "../components/ForceGraph_Position.vue";

export default {
  name: "PositionPage",
  components: {ForceGraph1, GetSearch},
  data() {
    return {
      api1:
          "http://127.0.3.1:5050/datas?link=true&product=true&company=true&start_time=1900-10-10&end_time=2024-10-10",
      names: ["环节", "公司", "产品"],
      colors: ["#aaaaff", "#f1662b", "#FFC0CB"],
      search_input: "",
      isProduct: false,
      isLink: false,
    };
  },
  watch: {
    search_input: function () {
      this.handleInputSubmit(this.search_input);
    },
  },
  methods: {
    handleInputSubmit(inputString) {
      this.search_input = inputString;
      console.log(this.api1);
    },
  },
};
</script>
<style lang="less" scoped>
.check_box {
  display: inline-block;
  margin-left: 40px;
  width: 200px;
}
.search {
  display: inline-block;
  margin-left: 60px;
}

/*节点说明*/
.indicator {
  display: inline-block;
  margin-left: 290px;
  margin-top: 20px;
  .list_color {
    display: inline-block;
    margin-left: 40px;
    text-align: center;
    color: #f7f7f7;
    font-size: 16px;

    span {
      float: left;
      width: 50px;
      height: 22px;
    }
  }
}

.s1 {
  display: inline-block;
  background-color: #f7f7f7;
  margin-top: 20px;
  margin-left: 30px;
  width: 1250px;
  height: 570px;
}
</style>