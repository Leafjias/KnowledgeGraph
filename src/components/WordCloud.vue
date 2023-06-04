<template>
  <div ref="chartRef" className="word-cloud"></div>
</template>

<script>
import 'echarts-wordcloud';
import * as echarts from 'echarts';

export default {
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      options: {
        // 标题样式
        title: {
          text: '公司新闻词云',
          x: "center",
          y: "3%",
          textStyle: {
            fontSize: 20,
            color: "#222"
          },
        },
        // 这里设置提示框 (鼠标悬浮效果)
        tooltip: {
          // 数据项图形触发
          trigger: 'item',
          // 提示框浮层的背景颜色。 (鼠标悬浮后的提示框背景颜色)
          backgroundColor: "white",
          // 字符串模板(地图): {a}（系列名称），{b}（区域名称），{c}（合并数值）,{d}（无）
          formatter: '关键词：{b}<br/>词频：{c}'
        },
        series: [
          {
            type: "wordCloud",
            shape: "circle",
            left: "center",
            top: "17%",
            gridSize: 7,
            sizeRange: [12, 30],
            rotationRange: [-30, 30],
            rotationStep: 30,
            textStyle: {
              color: function () {
                return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                );
              },
            },
            data: [],
          },
        ],
      },
    };
  },
  mounted() {
    this.myEcharts = echarts.init(this.$refs["chartRef"]);
    this.updateChart();
  },
  watch: {
    data() {
      this.updateChart();
    },
  },
  methods: {
    updateChart() {
      this.myEcharts.setOption({
        ...this.options,
        series: [
          {
            ...this.options.series[0],
            data: this.data,
          },
        ],
      });
    },
  },
};
</script>
<style lang='less' scoped>
.word-cloud {
  height: 320px;
  width: 520px;
}
</style>
