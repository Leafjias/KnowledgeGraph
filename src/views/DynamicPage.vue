<template>
  <!--复选框-->
  <div class="selections">
    <el-checkbox v-model="sector" label="环节" size="large"/>
    <el-checkbox v-model="product" label="产品" size="large"/>
    <el-checkbox v-model="company" label="公司" size="large"/>
  </div>
  <!--新增：下拉框选择展示类型-->
  <div class="display_type">
    <el-select v-model="displayMode" placeholder="请选择">
      <el-option label="普通模式" value="normal"></el-option>
      <el-option label="重要度模式" value="importance"></el-option>
    </el-select>
  </div>
  <!--结点颜色含义放置框：框内为各类结点对应颜色-->
  <div class="indicator">
    <div class="list_color" v-for="(name, index) in names" :key="index">
      <span :style="{ backgroundColor: colors[index] }">{{ name }}</span>
    </div>
  </div>
  <!--图谱可视化区域-->
  <svg>
    <force-graph v-if="displayMode === 'normal'" :url="api1" :time="time" v-on:clickNode="showNodeInfo"
                 @update-statistics="handleStatisticsUpdate"/>
    <ForceGraph_pagerank v-if="displayMode === 'importance'" :url="api1" v-on:clickNode="showNodeInfo"
                         @update-statistics="handleStatisticsUpdate"/>
  </svg>
  <!--  图-->
  <div class="chart-container">
    <Node_num_line></Node_num_line>
  </div>
  <!-- 时间轴 -->
  <div class="timeline">
    <el-slider v-model="sliderYear" :min="1990" :max="2023" show-input step="1" @change="updateTime"></el-slider>
  </div>
  <!--生成图标按钮-->
  <div class="generate_button">
    <el-button type="primary" @click="updateGraph">更新图谱</el-button>
  </div>


</template>
<script>
import ForceGraph_pagerank from "../components/ForceGraph_pagerank_D.vue";
import ForceGraph from "../components/ForceGraph_D.vue";
import moment from "moment";
import Node_num_line from "@/components/Node_num_line.vue";


let bool_input = false;
export default {
  name: "HomePage",
  components: {ForceGraph, ForceGraph_pagerank, Node_num_line},
  data() {
    return {
      api1: "http://127.0.3.1:5050/datas?link=true&product=false&company=false&start_time=1900-10-10&end_time=2020-10-10",
      names: ["环节", "公司", "产品"],
      colors: ["#aaaaff", '#f1662b', '#FFC0CB'],
      sector: true,
      company: false,
      product: true,
      selectedNode: null,
      displayMode: "normal",
      nodeStatistics: {},
      timeValue: 0,
      sliderYear: 1990,
      time: ''
    };
  },
  methods: {
    //更新结点状态信息
    handleStatisticsUpdate(statistics) {
      this.nodeStatistics = statistics;
    },
    handleInputSubmit(inputString) {
      if (inputString != "") bool_input = true;
      else bool_input = false;
      this.search_input = inputString;
      if (bool_input == true) {
        const params = {
          search_input: this.search_input,
        };
        const queryString = Object.keys(params)
            .map((key) => params[key])
            .join("&");
        this.api1 = "http://127.0.3.1:5050/datas/community?name=" + queryString;
        console.log("new_api1=", this.api1);
      }
    },
    updateTime() {
      const currentYear = this.sliderYear;
      const currentDate = new Date(currentYear, 0, 1);

      if (!isNaN(currentDate.valueOf())) {
        this.time = currentDate.toISOString();
        console.log(this, this.time);
      }
    },


    // 新增：更新图表方法
    updateGraph() {
      if (bool_input == false) {
        const params = {
          link: this.sector,
          product: this.product,
          company: this.company,
          start_time: "1900-1-1",
          end_time: "2024-1-1",
        };
        const queryString = Object.keys(params)
            .map((key) => key + "=" + params[key])
            .join("&");
        this.api1 = "http://127.0.3.1:5050/datas?" + queryString;
        console.log("new_api1=", this.api1);
      }
    },
    //展示结点信息
    showNodeInfo(node) {
      if (!node) {
        return;
      }
      this.selectedNode = node;
      console.log('clicked node:', node);
    },
  },
  computed: {
    selectedNodeInfo() {
      const node = this.selectedNode;
      //console.log('结点信息:', node);
      if (node) {
        if (node.group == 1) {
          return `
          <div>结点id: ${node.id}</div>
          <div>结点名称: ${node.name}</div>
          <div>公司代码: ${node.code}</div>
          <div>公司全称: ${node.fullname}</div>
          <div>所在城市: ${node.city}</div>
          <div>公司所在地: ${node.where}</div>
          <div>公司网址: ${node.web}</div>
          <div>成立日期: ${moment(node.date).format("YYYY-MM-DD")}</div>
          <div>首发上市日: ${moment(node.date1).format("YYYY-MM-DD")}</div> `;
        } else {
          return `
          <div>结点id: ${node.id}</div>
          <div>结点名称: ${node.name}</div>`;
        }
      }
      return '';
    },
    sliderTimeValue: {
      get() {
        const startYear = 1900;
        const endYear = 2023;
        const currentYear = new Date(this.time).getFullYear();
        return ((currentYear - startYear) / (endYear - startYear)) * 100;
      },
      set(value) {
        this.timeValue = value;
      },
    },
  },


};
</script>

<style lang="less" scoped>
svg {
  width: 910px;
  height: 570px;
  background-color: #eee;
  margin-left: 10px;
  margin-top: 10px;
}

/*节点说明*/
.indicator {
  display: inline-block;
  margin-left: 50px;
  margin-top: 10px;

  .list_color {
    display: inline-block;
    margin-left: 40px;
    text-align: center;
    color: #eeeeee;
    font-size: 16px;

    span {
      float: left;
      width: 50px;
      height: 22px;
    }
  }
}

/*复选框*/
.selections {
  display: inline-block;
  width: 300px;
  margin-left: 100px;
}

/*新增：生成图标按钮样式*/
.generate_button {
  display: inline-block;
  margin-left: 30px;
}

.chart-container {
  margin-right: 100px;
  float: right;
  text-align: left;
  font-size: 13px; //字号
  text-indent: 20px; //缩进
  color: #9f1414;
  //background-color: #407e96;
  width: 300px;
  height: 320px;
  //.chart_pie {
  //  display: inline-block;
  //  //background-color: #f7f7f7;
  //  width: 470px;
  //  height: 285px;
  //}
  //
  //.chart_line {
  //  display: inline-block;
  //  background-color: #f7f7f7;
  //  width: 470px;
  //  height: 280px;
  //}
}

/*新增：下拉框选择展示类型样式*/
.display_type {
  display: inline-block;
  width: 200px;
  margin-left: 20px;
}

.timeline {
  display: inline-block;
  margin-left: 20px;
  width: 1000px;

  input[type="range"] {
    width: 100%;
  }
}

</style>