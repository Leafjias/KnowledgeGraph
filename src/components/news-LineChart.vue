<template>
  <div className="line-echarts">
    <div className="line-echarts-ii" id="lineChart"></div>
  </div>
</template>

<script>
import {watch, ref, onMounted} from 'vue';

let echarts = require('echarts/lib/echarts');
require('echarts/lib/chart/line');
require('echarts/lib/component/tooltip');
require("echarts/lib/component/legend");

export default {
  name: 'LineEcharts',
  props: {
    stockPriceData: {
      type: Array,
      default: () => [],
    },
    text: {
      type: String,
      default: '股价',
    },
    color: {
      type: String,
      default: '#456ef4',
    },
  },
  setup(props) {
    const lineChart = ref(null);

    const drawLine = () => {
      if (!lineChart.value) {
        lineChart.value = echarts.init(document.getElementById('lineChart'));
      }
      lineChart.value.setOption(getEchartOption(), window.onresize = lineChart.value.resize);
    };

    const getEchartOption = () => ({
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        y: '400px',
        data: [props.text],
      },
      grid: {
        top: '20px',
        left: '1%',
        right: '2%',
        bottom: '30px',
        containLabel: true,
      },
      toolbox: {
        feature: {
          saveAsImage: {},
        },
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: props.stockPriceData.map(item => item.date),
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: props.text,
          type: 'line',
          smooth: true,
          itemStyle: {
            normal: {
              color: props.color,
              lineStyle: {
                color: props.color,
              },
            },
          },
          data: props.stockPriceData.map(item => item.price),
        },
      ],
    });

    onMounted(drawLine);

    watch(() => props.stockPriceData, () => {
      drawLine();
    });

    return {
      drawLine,
      lineChart
    };
  },
};
</script>

<style scoped lang="less">
.line-echarts {
  .line-echarts-ii {
    width: 470px;
    height: 280px;
  }
}
</style>
