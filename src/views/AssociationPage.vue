<template>
  <div class="check_box">
    <el-checkbox v-model="isProduct" label="产品" size="large"/>
    <el-checkbox v-model="isLink" label="产业链环节" size="large"/>
    <el-checkbox v-model="isCompany" label="企业" size="large"/>
  </div>
  <div class="select_box">
    <el-select v-model="selectedType">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"/>
    </el-select>
  </div>
  <div class="search">
    <get-search @onSubmit="handleInputSubmit"/>
  </div>
  <!--结点颜色含义放置框：框内为各类结点对应颜色-->
  <div class="indicator">
    <div class="list_color" v-for="(name, index) in names" :key="index">
      <span :style="{ backgroundColor: colors[index]}">{{ name }}</span>
    </div>
  </div>
  <!--图谱可视化区域:社群图-->
  <svg class="s1">
    <text x="50%" y="10%" dominant-baseline="middle" text-anchor="middle" font-size="16"></text>
    <force-graph1 :url="api1" :company="isCompany" :link="isLink" :product="isProduct" :name="search_input"/>
  </svg>
</template>

<script>
import GetSearch from "../components/GetSearch.vue";
//import ForceGraph from "../components/ForceGraph.vue";
import ForceGraph1 from "../components/ForceGraph_pagerank_Ass.vue";

export default {
  name: "AssociationPage",
  components: {ForceGraph1, GetSearch},//, ForceGraph1
  data() {
    return {
      //http://127.0.3.1:5050/
      api1: 'http://127.0.3.1:5050/datas/community?', //后端接口
      names: ['环节', '公司', '产品'], //名称
      colors: ["#aaaaff", '#f1662b', '#FFC0CB'],
      search_input: '',
      selectedType: "company",
      options: [{value: 'company', label: '公司',}, {value: 'link', label: '环节',}, {
        value: 'product',
        label: '产品',
      }],
      isProduct: false,
      isLink: false,
      isCompany: false,
    }
  },
  watch: {
    search_input: function () {
      this.handleChange();
    },
    selectedType: function () {
      this.handleChange();
    },
  },
  methods: {
    handleInputSubmit(inputString) {
      this.search_input = inputString;
      this.handleChange();
    },
    handleChange() {
      const params = {
        type: this.selectedType,
        name: this.search_input,
      };
      const queryString = Object.keys(params)
          .map((key) => key + "=" + params[key])
          .join("&");
      this.api1 = "http://127.0.3.1:5050/datas/community?" + queryString;
      console.log(this.api1);
    },
  }
}
</script>

<style lang="less" scoped>

.check_box {
  display: inline-block;
  margin-left: 40px;
  width: 300px;
}
.select_box {
  display: inline-block;
  margin-left: 40px;
  width: 75px;
}
.search {
  display: inline-block;
  margin-left: 5px;
}

/*节点说明*/
.indicator {
  display: inline-block;
  margin-left: 130px;
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