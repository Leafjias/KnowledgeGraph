<template>
  <div>
     <china-map :api="api" :api_company="api_company" :type="selectedType" />
  </div>
  <!-- 复选框 -->
  <div class="selections">
    <el-checkbox v-model="up" label="上游" size="large"/>
    <el-checkbox v-model="mid" label="中游" size="large"/>
    <el-checkbox v-model="down" label="下游" size="large"/>
  </div>
  <!-- 时间范围输入查询 -->
  <div class="in_date">
    <date-picker v-model="dateRange" @update:value="handleDatepickerChange"/>
  </div>
  <!-- 新增：下拉框选择展示类型 -->
  <div class="display_type">
    <el-select v-model="selectedType" placeholder="请选择">
      <el-option label="注册资本" value="注册资本"></el-option>
      <el-option label="重要度" value="重要度"></el-option>
      <el-option label="企业数量" value="公司数量"></el-option>
    </el-select>
  </div>
  <!-- 新增：生成图标按钮 -->
  <div class="generate_button">
    <el-button type="primary" @click="updateGraph">更新地图</el-button>
  </div>
</template>
<script>
import ChinaMap from "@/components/ChinaMap.vue";
import DatePicker from "../components/DatePicker.vue";
import moment from "moment";

export default {
  name: "FourthPage",
  components: {ChinaMap, DatePicker},
  data() {
    return {
      api: "",
      api_company: "",
      up: true,
      mid: true,
      down: true,
      dateRange: [],
      start_time: "1990-10-10",
      end_time: "2023-4-10",
      selectedType: "公司数量",
    };
  },
  methods: {
    handleDatepickerChange(value) {
      this.end_time = moment(value).format("YYYY-MM-DD");
    },
    // 新增：更新图表方法
    updateGraph() {

      const params = {
        up: this.up,
        mid: this.mid,
        down: this.down,
        start_time: this.start_time,
        end_time: this.end_time,
      };
      const queryString = Object.keys(params)
          .map((key) => key + "=" + params[key])
          .join("&");
      this.api = "http://127.0.3.1:5050/datas/location?" + queryString;
      this.api_company = `http://127.0.3.1:5050/datas?link=false&product=true&company=true&start_time=${this.start_time}&end_time=${this.end_time}`; // 新增
      console.log("new_api=", this.api);
      console.log("new_api_company=", this.api_company); // 新增
    },
  },
  mounted() {
    this.updateGraph();
  },
}
</script>
<style lang="less" scoped>
/*复选框*/
.selections {
  float: right;
  width: 300px;
  height: 40px;
 margin-right: 1000px;
}

/*时间输入框样式*/
.in_date {
  float: left;
  width: 400px;
  height: 40px;
  margin-left: 300px;
  margin-top: -30px;
}

/*新增：下拉框选择展示类型样式*/
.display_type {
  float: left;
  width: 200px;
  height: 40px;
  margin-top: -30px;
  margin-left: 30px;
}

/*新增：生成图标按钮样式*/
.generate_button {
  float: left;
  margin-left: 20px;
  margin-top: -30px;
}

.loading {
  /* 加载界面的样式 */
}
</style>