<template>
  <div class="checkboxContainer">
    <el-checkbox v-model="selectedEffects.positive" @change="updateChart" label="积极" size="large" />
    <el-checkbox v-model="selectedEffects.negative" @change="updateChart" label="消极" size="large" />
    <el-checkbox v-model="selectedEffects.neutral" @change="updateChart" label="中立" size="large" />
  </div>
  <!-- 用于显示折线图的 div -->
  <div ref="chartContainer" :style="{width: '750px', height: '430px'}">
    <!-- 引入折线图组件，并监听 chart-data-ready 事件 -->
    <line-read :company="company" @chart-data-ready="handleChartDataReady" />
  </div>
  <!--引入文本框组件，当有选中的新闻时才显示，并监听 click 事件 -->
  <div class="textBoxContainer">
    <text-box-chart v-show="selectedNews" :news="selectedNews"></text-box-chart>
  </div>
</template>

<script>
import LineRead from "../components/LineRead.vue";
import * as echarts from "echarts";
import TextBoxChart from "../components/text-box-chart.vue"

export default {
  //Vue 组件的定义
  name: "LineChart",
  components: {LineRead, TextBoxChart},
  props: {
    company: {
      type: String,
      required: true,
    },
  },
  //用于存储当前选中的新闻：
  data() {
    return {
      currentOption: null, // 或其他初始值
      selectedNews: [],
      newsData: [],
      //myChart: null, // 添加 myChart 到 data
      specialPoints: [], // 添加 specialPoints 到 data
      selectedEffects: {
        positive: true,
        negative: true,
        neutral: true,
      },
    };
  },
  mounted() {
    //window.addEventListener("resize", this.handleResize);
    // 创建 ECharts 实例
    this.myChart = echarts.init(this.$refs.chartContainer);
    window.addEventListener("resize", () => {  //根据屏幕进行实时绘制
      this.myChart.resize();
    });
  },
  methods: {
    filterSpecialPoints(specialPoints) {
      return specialPoints.filter(point => {
        const newsItem = this.newsData.find((news) => news.时间 === point.date);
        if (!newsItem) return false;

        return (
            (this.selectedEffects.positive && newsItem.影响 === "积极") ||
            (this.selectedEffects.negative && newsItem.影响 === "消极") ||
            (this.selectedEffects.neutral && newsItem.影响 === "中立")
        );
      });
    },
    handleChartDataReady({stockData, newsData, specialPoints}) {

      this.specialPoints = specialPoints; // 设置 specialPoints
      this.newsData = newsData;
      // 提取xData
      const xData = Object.keys(stockData).map(date => date.slice(0, 4) + "-" + date.slice(4, 6) + "-" + date.slice(6));
      console.log("xData", xData)
      // 提取stockData
      const stockDataArray = Object.values(stockData).map(price => parseFloat(price));

      const specialPointsFiltered = this.filterSpecialPoints(specialPoints);
      // 修改 specialPoints 的格式
      const specialPointsFormatted = specialPointsFiltered.map(point => {
        const newsItem = this.newsData.find((news) => news.时间 === point.date);
        return {
          coord: [point.date, point.price],//该点在坐标系中的位置
          value: point.price,
          id: newsItem ? newsItem.id : null,//表示该点对应的新闻id
        };
      });


      // 在这里处理chartData，绘制折线图
      const option = {
        title: {
          text: '股价分析折线图',
          x: "center",
          y: "5%",
        },
        tooltip: {
          trigger: 'axis', // 以坐标轴为触发点显示 tooltip
          axisPointer: {
            type: 'cross', // 设置指示器类型为十字准星指示器
            label: {
              backgroundColor: '#6a7985' // 设置 tooltip背景颜色
            }
          }
        },
        xAxis: {
          type: 'category',// 设置 x 轴为类目型（即数据在 x 轴上为离散的）
          data: xData,
          axisTick: {
            alignWithLabel: true  // 坐标轴刻度标签与轴线对齐
          },
          axisLine: {
            onZero: false,  // x 轴不与y轴重合
            lineStyle: {
              color: '#999'  // 设置x轴的颜色为灰色
            }
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: '#999'
            }
          },
          axisLabel: {
            formatter: '{value}'  // 设置 y 轴的刻度标签格式
          },
          splitLine: {
            lineStyle: {
              type: 'dashed'  // 设置分隔线的类型为虚线
            }
          }
        },
        dataZoom: [{
          type: 'inside',  // 内部数据区域缩放
          zoomOnMouseWheel: 'ctrl',
          start: 0,
          end: 10
        }, {
          show: true,
          type: 'slider',
          bottom: 10,
          start: 0,
          end: 100
        }],
        series: [
          {
            name: '股价',
            data: stockDataArray,
            type: 'line',
            smooth: true,
            symbol: 'none',
            //用于鼠标放到折线图上设置折线图粗细
            emphasis: {
              lineStyle: {
                width: 2
              }
            },
            markPoint: {
              symbol: 'circle',
              //clickable: true,
              data: specialPointsFormatted,
              symbolSize: 8,
              label: {
                show: false,   // 设置标记点的标签不显示
                formatter: function (params) {
                  return params.data.value; // 显示y轴的数值
                }
              },
              itemStyle: {
                color: "#f00",   // 设置标记点的颜色为红色
              },


            },
          },
        ],
      };


      this.myChart.on("click", (params) => {
        if (params.componentType === "markPoint") {
          const matchedNews = this.newsData.filter(
              (news) =>
                  news.时间 === params.data.coord[0] &&
                  (
                      (this.selectedEffects.positive && news.影响 === "积极") ||
                      (this.selectedEffects.negative && news.影响 === "消极") ||
                      (this.selectedEffects.neutral && news.影响 === "中立")
                  )
          );
          this.selectedNews = matchedNews;
        }
      });
      this.myChart.setOption(option);
    },
    updateChart() {
      //const currentOption = this.myChart.getOption();
      const specialPointsFiltered = this.filterSpecialPoints(this.specialPoints);
      const specialPointsFormatted = specialPointsFiltered.map(point => {
        const newsItem = this.newsData.find((news) => news.时间 === point.date);
        return {
          coord: [point.date, point.price],
          value: point.price,
          id: newsItem ? newsItem.id : null,
        };
      });
      console.log("specialPoints", this.specialPoints)
      console.log("newsData", this.newsData)
      // 获取当前图表的配置
      const currentOption = this.myChart.getOption();
      // 更新 markPoint 数据
      currentOption.series[0].markPoint.data = specialPointsFormatted;
      // 更新图表
      this.myChart.setOption(currentOption, true);

    },
  },
};
</script>

<style>
.checkboxContainer {
  display: inline-block;
  margin-left: 20px;
  width: 400px;
  height: 35px;
  overflow: hidden;
}
</style>