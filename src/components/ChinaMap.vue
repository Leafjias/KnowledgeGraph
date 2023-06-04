<template>
  <div class="echarts-map-china" ref="echarts-map-china"></div>

  <div class="echarts-pie">
    <PieChart :data="options.pieChartData" :title="Pietitle"/>
  </div>
  <div class="analysis">
    <BarChart :data="options.stackedLineChartData" :title="Linetitle"></BarChart>
  </div>
</template>
<script>
import "../utils/china"
import * as echarts from 'echarts';
import axios from 'axios';
import BarChart from "../components/BarChart.vue";
import PieChart from "../components/PieChart.vue";

export default {
  components: {BarChart, PieChart},
  props: {
    api: {
      type: String,
      required: true,
    },
    api_company: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      api1: "",
      myEcharts: null,
      options: {
        title: {
          text: '上市公司地图分布',
          x: "center",
          textStyle: {
            fontSize: 19,
            color: "black"
          },
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: "white",
          formatter: ''
        },
        visualMap: {
          top: '55%',
          left: '6%',
          min: 0,
          max: 50,
          text: ['High', 'Low'],
          realtime: true,
          calculable: true,
          inRange: {
            color: ['#dfebff', '#012bfb']
          }
        },
        series: [
          {
            name: '模拟数据',
            type: 'map',
            mapType: 'china',
            roam: true,
            itemStyle: {
              normal: {
                label: {
                  show: true,
                  textStyle: {
                    color: "black"
                  }
                }
              },
              zoom: 1.5,
              emphasis: {
                label: {show: true}
              }
            },
            top: "5%",
            data: []
          }
        ],
        pieChartData: [],  // 初始化为一个空数组
        Linetitle:"",
        Pietitle:"",
        stackedLineChartData: [],  // 初始化为一个空数组
        companyData: [],  // 初始化为一个空数组
        relationData: [],  // 初始化为一个空数组
        productData: [],  // 初始化为一个空数组
      }
    };
  },

  mounted() {
    this.myEcharts = echarts.init(this.$refs["echarts-map-china"]);
    this.updateOptions();
    this.loadData();
    // 监听地图点击事件
    this.myEcharts.on('click', this.handleMapClick);
  },
  watch: {
    api: {
      handler: function () {
        this.loadData();
      },
      deep: true,
    },
    api_company: {  // 新增对 api_company 的观察
      handler: function () {
        this.loadCompanyData();
      },
      deep: true,
    },
    type: {
      handler: function () {
        this.updateOptions();
        this.loadData();
        this.loadCompanyData();
      },
      deep: true,
    },
  },
  methods: {
    updateOptions() {
      this.options.tooltip.formatter = `地区：{b}<br/>${this.type}：{c}`;
    },
    // 修改 handleMapClick 方法
    handleMapClick(params) {
      //更新饼图数据
      let provinceName = params.name;
      this.Pietitle = params.name + "省企业锂电池产业资本占比";
      let companiesInProvince = this.companyData.filter(company => company.地区.includes(provinceName));
      this.options.pieChartData = companiesInProvince.map(company => {
        let productsOfCompany = this.relationData.filter(relation => relation.from === company.name);
        return {
          name: company.name,
          value: productsOfCompany.reduce((total, product) => total + company.注册资本万元 * product.weight, 0),
        };
      });
      //更新柱状图数据
      this.Linetitle = params.name + "省锂电池产品构成";
      let productsInProvince = companiesInProvince.reduce((products, company) => {
        let productsOfCompany = this.relationData.filter(relation => relation.from === company.name).map(relation => {
          let product = this.productData.find(p => p.name === relation.to);
          return product ? {
            name: product.name,
            type: product.type,
            value: company.注册资本万元 * relation.weight,
          } : null;
        }).filter(product => product);  // 去除 null 值
        return products.concat(productsOfCompany);
      }, []);

      let groupedData = {};
      productsInProvince.forEach(product => {
        if (!groupedData[product.name]) {
          groupedData[product.name] = {'上游': 0, '中游': 0, '下游': 0};
        }
        if (product.type === 1) {
          groupedData[product.name]['上游'] += product.value;
        } else if (product.type === 2) {
          groupedData[product.name]['中游'] += product.value;
        } else if (product.type === 3) {
          groupedData[product.name]['下游'] += product.value;
        }
      });

      this.options.stackedLineChartData = Object.entries(groupedData).map(([productName, typeSums]) => {
        return {
          name: productName,
          上游: typeSums['上游'],
          中游: typeSums['中游'],
          下游: typeSums['下游']
        };
      });

      console.log(this.options.stackedLineChartData)

    },
    loadData() {
      return axios.get(this.api).then(response => {
        if (response.data.status === 'success') {
          const data = response.data.results[this.type];
          console.log(this.type);
          const maxValue = Math.max(...data.map(item => item.value));
          this.options.visualMap.max = maxValue / 2;
          this.options.series[0].data = data;
          this.myEcharts.setOption(this.options);
        } else {
          console.error('数据请求失败');
        }
      }).catch(error => {
        console.error(error);
      });
    },
    // 修改 loadCompanyData 方法
    loadCompanyData() {
      return axios.get(this.api_company).then(response => {
        if (response.data.status === 'success') {
          this.companyData = response.data.results.公司.map(company => {
            return {
              name: company.name,
              地区: company.所属地区,
              注册资本万元: company.注册资本万元,
            };
          });
          this.productData = response.data.results.产品.map(product => {
            let type = product.up ? 1 : product.mid ? 2 : product.down ? 3 : 0;
            return {
              name: product.name,
              type: type,
            };
          });
          this.relationData = response.data.results.公司与产品.map(relation => {
            return {
              from: relation.from,
              to: relation.to,
              weight: relation.weight,
            };
          });
          console.log('公司数据:', this.companyData);
          console.log('产品数据:', this.productData);
          console.log('关系数据:', this.relationData);
        } else {
          console.error('公司数据请求失败');
        }
      }).catch(error => {
        console.error(error);
      });
    },
  }
};
</script>
<style lang="less" scoped>
.echarts-map-china {
  float: left;
  //background-color: darkmagenta;
  margin-top: 20px;
  margin-left: 10px;
  margin-bottom: 6px;
  height: 600px;
  width: 800px;
}
.echarts-pie {
  float: right;
  width: 480px;
  height: 300px;
  //background-color: #1907bb;
  margin-right: 10px;
  margin-top: 20px;
}

.analysis {
  float: right;
  width: 480px;
  height: 290px;
  //background-color: #44dab7;
  margin-bottom: 6px;
  margin-right: 10px;
  margin-top: 10px;
}
</style>
