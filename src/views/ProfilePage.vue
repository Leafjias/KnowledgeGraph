<template>
  <div class="search">
    <get-search @onSubmit="handleInputSubmit" />
  </div>
  <!--结点颜色含义放置框：框内为各类结点对应颜色-->
  <div class="indicator">
    <div class="list_color" v-for="(name, index) in names" :key="index">
    <span :style="{ backgroundColor: colors[index]}">{{ name }}</span>
  </div>
  </div>
  <!--图谱可视化区域:社群图-->
  <svg class="s1">
    <text x="50%" y="10%" dominant-baseline="middle" text-anchor="middle" font-size="16">结点社群图谱</text>
    <force-graph :url="api1" />
  </svg>
  <!--结点信息-->
  <div class="info">
    <div v-for="(item, index) in infoData" :key="index">
      <h2>{{ item.name }}</h2>
      <p><strong>公司全称：</strong>{{ item['fullname'] }}</p>
      <p><strong>公司网址：</strong><a :href="'http://'+item['公司网址']" target="_blank">{{ item['公司网址'] }}</a></p>
      <p><strong>注册资本：</strong>{{ item['注册资本万元'] }}万元</p>
      <p><strong>成立日期：</strong>{{ item['成立日期'] }}</p>
      <p><strong>所属地区：</strong>{{ item['所属地区'] }}</p>
      <p><strong>首发上市日：</strong>{{ item['首发上市日'] }}</p>
      <p><strong>上市地点：</strong>{{ item['上市地点'] }}</p>
      <p><strong>上市首日开盘价：</strong>{{ item['上市首日开盘价'] }}</p>
      <p><strong>主营业务：</strong>{{ item['主营业务'] }}</p>
      <p><strong>经营范围：</strong>{{ item['经营范围'] }}</p>
      <p><strong>公司简介：</strong>{{ item['公司简介'] }}</p>
    </div>
  </div>
  <!--圆饼图-->
  <div class="pie_chart">
      <pie-chart
          ref="chartDom"
          :data="chartData"
          :title="search_input"
      ></pie-chart>
  </div>
  <div class="K-linegraph">
    <line-chart :company="search_input"></line-chart>
  </div>
  <div class="wordcloud">
    <WordCloud :data="wordCloudData"/>
  </div>
</template>

<script>
import GetSearch from "../components/GetSearch.vue";
import ForceGraph from "../components/ForceGraph.vue";
// import ForceGraph1 from "../components/ForceGraph_pagerank.vue";
import PieChart from "../components/PieChart.vue";
import axios from "axios";
import WordCloud from "../components/WordCloud.vue";
import LineChart from "../components/LineChart.vue"; // 导入 LineChart 组件
// 提取到文件顶部的共享方法
async function fetchDataFromServer(value, type) {
  try {
    const response = await axios.get(
      `http://127.0.3.1:5050/datas/find/?value=${encodeURIComponent(value)}&type=${type}`
    );
    return response.data.results;
  } catch (error) {
    //console.log(error);
    return null;
  }
}
export default {
  name: "SecondPage",
  components:{ForceGraph, WordCloud, GetSearch, PieChart,LineChart},//, ForceGraph1
  data() {
    return {
      //http://127.0.3.1:5050/
      api1: 'http://127.0.3.1:5050/datas/community?', //后端接口
      //api2:'http://127.0.3.1:5050/datas?link=true&product=false&company=false&start_time=1990-10-10&end_time=2020-10-10',
      names: ['环节', '公司', '产品'], //名称
      colors: ["#aaaaff",'#f1662b', '#FFC0CB'],
      search_input: '',
      selectedType: "company",
      chartData: [],
      wordCloudData: [],
      infoData: [],
      options:[{value: 'company', label: '公司',},{value: 'link', label: '环节',},{value: 'product', label: '产品',}],
    }
  },
  watch: {
    search_input:function () {
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
      this.getChartData(this.selectedType, this.search_input).then(chartData => {
        this.chartData = chartData;
      });
      this.getInfoData(this.selectedType, this.search_input).then(infoData => {
        this.infoData = infoData;
      });
    },
    async getChartData(type, name) {
      try {
        const results = await fetchDataFromServer(name, type);
        const companyProducts = results.公司与产品;
        const worldCloudData = results.词云;//获取词云
        this.wordCloudData = worldCloudData;//赋值词云
        return this.processData(companyProducts);
      } catch (error) {
        //console.log(error);
        return [];
      }
    },
    async getInfoData(type, name) {
      try {
        const results = await fetchDataFromServer(name, type);
        const companyInfo = results.查找的结点;
        //console.log("结点信息", companyInfo);
        return companyInfo;
      } catch (error) {
        //console.log(error);
        return [];
      }
    },
    processData(data) {
      const result = [];
      const totalWeight = data.reduce(
          (acc, p) => acc + parseFloat(p.weight),
          0
      );
      for (const item of data) {
        result.push({
          name: item.to,
          value: item.weight / totalWeight,
        });
      }
      return result;
    },
  }
}
</script>

<style lang="less" scoped>
.search {
  display: inline-block;
  margin-left: 150px;
}
/*节点说明*/
.indicator {
  display: inline-block;
  margin-left: 250px;
  margin-top: 20px;
  .list_color{
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
  position: absolute;
  background-color: #f7f7f7;
  margin-top: 65px;
  margin-left: -950px;
  width: 820px;
  height: 570px;
}
.info {
  position: absolute;
  width:460px;
  margin-left: 850px;
  margin-top: 10px;
  height:260px;
  background-color: #f7f7f7;
  font-size: 12px;
  border-radius: 5px;
  line-height: 1.5em;
  border: 1px solid #ccc;
  text-indent: 2em;
  overflow-y: scroll;
}
.pie_chart {
  position: absolute;
  width:460px;
  height:320px;
  margin-top: 280px;
  margin-left: 850px;
  //background-color: #f7f7f7;
}
.K-linegraph {
  position: absolute;
  width: 750px;
  height: 480px;
  margin-left: 10px;
  margin-top: 615px;
  background-color: #f7f7f7;
}
.wordcloud {
  position: absolute;
  margin-left: 780px;
  height: 320px;
  width: 530px;
  margin-top: 775px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f7f7f7;
}
</style>