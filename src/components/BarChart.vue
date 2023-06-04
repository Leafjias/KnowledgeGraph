<template>
  <div ref="chartRef" class="stacked-line-chart"></div>
</template>

<script>
import {onMounted, ref, watchEffect} from "vue";
import * as echarts from "echarts";

export default {
  name: "StackedLineChart",
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
    const chartRef = ref(null);
    let myChart = null;

    onMounted(() => {
      myChart = echarts.init(chartRef.value);
      renderChart();
    });

    watchEffect(() => {
      console.log('props.data:', props.data);
      if (props.data.length && myChart) {
        renderChart();
      }
    });

    function renderChart() {
      // 清除图表的当前状态
      myChart.clear();

      // 映射数据到各个系列
      const seriesData = props.data.map(product => {
        return {
          name: product.name,
          type: 'bar',
          stack: '总量',
          data: ['上游', '中游', '下游'].map(type => product[type])
        };
      });

      const option = {
        title: {
          text: props.title,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function (params) {
            // 只显示有值的提示框
            let result = params[0].axisValueLabel + '<br>';
            params.forEach(param => {
              if (param.value > 0) {
                result += `${param.marker} ${param.seriesName}: ${param.value}<br>`;
              }
            });
            return result;
          },
        },
        legend: {
          show: false, // 隐藏图例
        },
        grid: {
          bottom: '8%', // 调整图表在 div 内的位置
          containLabel: true // 是否包含坐标轴标签，默认为 false
        },
        xAxis: {
          type: 'category',
          data: ['上游', '中游', '下游']
        },
        yAxis: {},
        series: seriesData
      };

      // 将配置项应用到图表实例
      myChart.setOption(option);
    }

    return {
      chartRef,
    };
  },
};
</script>

<style scoped>
.stacked-line-chart {
  width: 480px;
  height: 290px;
}
</style>
