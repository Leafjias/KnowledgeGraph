<template>
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
    <!--    <text x="50%" y="10%" dominant-baseline="middle" text-anchor="middle" font-size="16">-->
    <!--      展示查询结点和与它直接相连的结点-->
    <!--    </text>-->
    <!--    计算个事件的个数-->
    <force-graph1 :url="api1" :time="this.time" @visible-nodes-count="handleVisibleNodesCount"
                  @stock-price-data-updated="handleStockPriceDataUpdated"/>
  </svg>
  <div class="chart">
    <div class="chart_pie">
      <PieChart :data="pieChartData" :title="this.time" :centerNumber="riskScore"/>

    </div>
    <div class="chart_line">
      <lineecharts :stock-price-data="lineChartData" text="股价" color="#456ef4"></lineecharts>
    </div>
  </div>
  <!-- 时间轴 -->
  <div class="timeline">
    <el-slider v-model="sliderYear" :min="1593561600000" :max="1680240000000" :step="2592000000"
               @change="updateTime" :format-tooltip="formatTooltip"></el-slider>
  </div>
</template>
<script>
import GetSearch from "../components/GetSearch.vue";
import ForceGraph1 from "../components/ForceGraph_Con.vue";
import PieChart from "../components/PieChart_sorce.vue"
import lineecharts from "../components/news-LineChart.vue"

export default {
  name: "ConnectionPage",
  components: {ForceGraph1, GetSearch, PieChart, lineecharts},//, ForceGraph1
  data() {
    return {
      //http://127.0.3.1:5050/
      api1: 'http://127.0.3.1:5050/datas/find/?', //后端接口
      //api2:'http://127.0.3.1:5050/datas?link=true&product=false&company=false&start_time=1990-10-10&end_time=2020-10-10',
      names: ['消极', '积极', '中立', '环节', '公司', '产品'], //名称
      colors: ["#f50606", "#00f839", "#002bff",
        "#aaaaff", '#f1662b', '#FFC0CB'],
      search_input: '',
      selectedType: "company",
      options: [{value: 'company', label: '公司',}, {value: 'link', label: '环节',}, {
        value: 'product',
        label: '产品',
      }],
      time: "",
      timeValue: 0,
      sliderYear: 1990,
      pieChartData: [],
      lineChartData: [],
      riskScore: 0, // 新增的 riskScore 变量
    }
  },
  watch: {
    search_input: function () {
      this.handleChange();
    },
    selectedType: function () {
      this.handleChange();
    },
    lineChartData: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.calculateRiskScore();
      }
    },
    pieChartData: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.calculateRiskScore();
      }
    }
  },
  methods: {
    calculateRiskScore() {
      // 检查股票价格数据和情绪数据是否足够
      if (this.lineChartData.length <= 1) {
        console.log("数据不足，无法计算风险评分。");
        return;
      }

      // 计算整体回报率
      const firstPrice = this.lineChartData[0].price; // 第一天的股票价格
      const lastPrice = this.lineChartData[this.lineChartData.length - 1].price; // 最后一天的股票价格
      const overallReturnRate = (lastPrice - firstPrice) / firstPrice; // 计算整体回报率
      // 将回报率转换为0到1之间的分数
      const returnRateScore = (overallReturnRate + 1) / 2;
      if (this.pieChartData.length === 0) {
        const riskScore = (returnRateScore + 1/3) * 50;
        this.riskScore = riskScore;
        console.log(`风险评分: ${riskScore}`);
      } else {
        // 计算情绪评分
        const positiveSentimentCount = this.pieChartData.find(item => item.name === 'Group 积极').value; // 积极情绪的数量
        const totalSentimentCount = this.pieChartData.reduce((sum, item) => sum + item.value, 0); // 总的情绪数量
        const sentimentScore = positiveSentimentCount / totalSentimentCount; // 计算情绪评分
        // 计算总体风险评分
        const riskScore = (returnRateScore + sentimentScore) * 50;
        this.riskScore = riskScore;
        console.log(`风险评分: ${riskScore}`);
      }


    },
    handleInputSubmit(inputString) {
      this.search_input = inputString;
      this.handleChange();
    },
    handleStockPriceDataUpdated(stockPriceData) {
      console.log("收到了")
      // 更新父组件中的数据，以便将其传递给折线图组件
      this.lineChartData = stockPriceData;
      console.log("股价", this.lineChartData)
    },

    handleVisibleNodesCount(visibleNodesByGroup) {
      console.log("Visible nodes count:", visibleNodesByGroup);
      // 您可以在这里根据需要使用 visibleNodesByGroup 数据
      // 将接收到的数据转换为适用于 PieChart 组件的格式
      const total = parseInt(visibleNodesByGroup['消极']) + parseInt(visibleNodesByGroup['中立']) + parseInt(visibleNodesByGroup['积极']);

      const newData = Object.entries(visibleNodesByGroup).map(([group, count]) => {
        return {
          name: `Group ${group}`,
          //value: total > 0 ? parseFloat(count) / parseFloat(total) : 0, // 将 count 和 total 转换为浮点数
          value: parseFloat(count), // 将 count 和 total 转换为浮点数
        };
      });
      console.log("情绪")
      console.log("total:", total);
      console.log("newData:", newData);
      // 更新 pieChartData
      this.pieChartData = newData;
    },

    formatTooltip(value) {
      const date = new Date(value);
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      this.time = `${year}-${month}`;
      return `${year}-${month}`;
    },
    handleChange() {
      const params = {
        type: this.selectedType,
        value: this.search_input,
      };
      const queryString = Object.keys(params)
          .map((key) => key + "=" + params[key])
          .join("&");
      this.api1 = "http://127.0.3.1:5050/datas/find/?" + queryString;
      console.log(this.api1);
    },
    updateTime() {
      const currentYear = this.sliderYear;
      const currentDate = new Date(currentYear, 0, 1);

      if (!isNaN(currentDate.valueOf())) {
        //this.time = currentDate.toISOString();
        console.log("this time", this.time);
      }
    },
  }
}
</script>
<style lang="less" scoped>
.select_box {
  display: inline-block;
  margin-left: 100px;
  width: 75px;
}

.search {
  display: inline-block;
  margin-left: 5px;
}

/*节点说明*/
.indicator {
  display: inline-block;
  margin-left: 100px;
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
  margin-top: 10px;
  margin-left: 30px;
  width: 800px;
  height: 580px;
}

.chart {
  display: inline-block;
  margin-left: 10px;
  width: 470px;
  height: 570px;

  .chart_pie {
    display: inline-block;
    //background-color: #f7f7f7;
    width: 470px;
    height: 285px;
  }

  .chart_line {
    display: inline-block;
    background-color: #f7f7f7;
    width: 470px;
    height: 280px;
  }
}

.timeline {
  display: inline-block;
  float: left;
  margin-top: -20px;
  margin-left: 30px;
  width: 800px;

  input[type="range"] {
    width: 100%;
  }
}
</style>