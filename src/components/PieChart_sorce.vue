<template>
  <!-- 使用 ref 定义一个 DOM 引用，绑定 id 属性，并设置样式类名 -->
  <div ref="chartRef" :id="id" class="pie-chart"></div>
</template>

<script>
import {onMounted, ref, watchEffect} from "vue";
import * as echarts from "echarts";

export default {
  name: "PieChart",
  props: {
    id: {
      type: String,
      default: "",
    },
    title: {
      type: String,
      required: true,
    },
    data: {
      type: Array,
      required: true,
    },
    centerNumber: {
      type: Number,
      required: false,
      default: 0,
    },
  },
  setup(props) {
    const chartRef = ref(null);
    let myChart = null;

    onMounted(() => {
      myChart = echarts.init(chartRef.value);
      renderChart();
    });

    watchEffect(() => {
      if (props.data.length && myChart) {
        renderChart();
      }
    });

    watchEffect(() => {
      if (props.centerNumber !== undefined && myChart) {
        renderChart();
      }
    });

    function renderChart() {
      const option = {
        title: {
          text: props.title + "舆情统计",
          left: "center",
        },
        tooltip: {
          trigger: "item",
          formatter: (params) => {
            const {name, percent, value} = params;
            return `${name}: ${value} (${percent}%)`;
          },
        },
        color: ["#2ECC71", "#E74C3C", "#3498DB"],
        graphic: [
          {
            type: "text",
            left: "center",
            top: "35%",
            style: {
              text: Math.floor(props.centerNumber).toString(),
              textAlign: "center",
              fill: "#333333",
              font: 'normal bolder 1em "Microsoft YaHei"',
              fontSize: 28,
            },
          },
          {
            type: "text",
            left: "center",
            top: "45%",
            style: {
              text: getRiskLevel(props.centerNumber),
              textAlign: "center",
              fill: "#333333",
              font: 'normal 1em "Microsoft YaHei"',
              fontSize: 16,
            },
          },
        ],
        series: [
          {
            name: "情绪占比",
            type: "pie",
            center: ["50%", "35%"],
            radius: ["35%", "60%"],
            top: "10%",
            data: props.data.map((item) => ({
              value: item.value,
              name: item.name,
            })),
          },
        ],
      };
      myChart.setOption(option);
    }

    function getRiskLevel(centerNumber) {
      if (centerNumber >= 0 && centerNumber <= 20) {
        return "高风险";
      } else if (centerNumber >= 21 && centerNumber <= 40) {
        return "中等风险";
      } else if (centerNumber >= 41 && centerNumber <= 60) {
        return "中高风险";
      } else if (centerNumber >= 61 && centerNumber <= 80) {
        return "中低风险";
      } else if (
          centerNumber >= 81 && centerNumber <= 100) {
        return "低风险";
      } else {
        return "";
      }
    }

    return {
      chartRef,
    };
  },
};
</script>

<style lang="less" scoped>
.pie-chart {
  width: 450px;
  height: 285px;
}
</style>
