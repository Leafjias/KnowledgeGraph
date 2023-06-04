<template>
  <!-- 使用 ref 定义一个 DOM 引用，绑定 id 属性，并设置样式类名 -->
  <div ref="chartRef" :id="id" class="pie-chart"></div>
</template>

<script>
import { onMounted, ref, watchEffect } from "vue";
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
  },
  setup(props) {
    // 定义一个 ref 用于存储 DOM 节点的引用
    const chartRef = ref(null);
    // 初始化图表实例为空
    let myChart = null;

    // 组件挂载后的回调函数
    onMounted(() => {
      // 初始化图表实例
      myChart = echarts.init(chartRef.value);
      // 渲染图表
      renderChart();
    });

    // 监听 props.data 的变化，如果有数据且图表实例存在，则重新渲染图表
    watchEffect(() => {
      if (props.data.length && myChart) {
        renderChart();
      }
    });

    // 渲染图表的函数
    function renderChart() {
      console.log('props.data:', props.data);

      // 定义图表配置项
      const option = {
        title: {
          text: props.title,
          left: "center",
        },
        // 添加 tooltip 配置以在鼠标悬停时显示信息
        tooltip: {
          trigger: "item",
          formatter: "{a} <br/>{b}:({d}%)",
        },
        series: [
          {
            name: "产品占比",
            type: "pie",
            top: "5%",

            data: props.data.map((item) => ({
              value: item.value,
              name: item.name,
            })),
          },
        ],
      };
      // 将配置项应用到图表实例
      myChart.setOption(option);
    }

    // 返回 chartRef 以供模板使用
    return {
      chartRef,
    };
  },
};
</script>
<style lang="less" scoped>
.pie-chart {
  width: 480px;
  height: 280px;
}
</style>