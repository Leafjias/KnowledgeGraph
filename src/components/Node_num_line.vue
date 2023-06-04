<template>
  <div ref="chartDom" style="width: 400px; height: 610px;"></div>
</template>

<script>
import {ref, onMounted} from 'vue';
import * as echarts from 'echarts';

export default {
  setup() {
    const chartDom = ref(null);
    let chartInstance = null;

    onMounted(() => {
      chartInstance = echarts.init(chartDom.value);

      const option = {
        legend: {},
        tooltip: {
          trigger: 'axis',
          showContent: false
        },
        dataset: {
          source: [
            ['product', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000',
              '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
              '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'],
            ['环节', '77', '77', '77', '77', '77', '77', '77', '77', '77', '77', '77',
              '77', '77', '77', '77', '77', '77', '77', '77', '77', '77',
              '77', '77', '77', '77', '77', '77', '77', '77', '77', '77'],
            ['产品', '170', '170', '170', '170', '170', '170', '170', '170', '170', '170', '170'
              , '170', '170', '170', '170', '170', '170', '170', '170', '170', '170', '170'
              , '170', '170', '170', '170', '170', '170', '170', '170', '170', '170', '170'],
            ['公司', '17', '18', '19', '25', '38', '53', '65', '83', '113', '135', '155'
              , '175', '198', '226', '243', '250', '259', '270', '281', '286', '294', '300'
              , '306', '311', '312', '316', '319', '320', '320', '320', '320', '320', '320'],
            ['环节与公司', '15', '16', '16', '29', '35', '47', '84', '113', '151', '187', '216'
              , '248', '284', '321', '335', '343', '355', '368', '382', '389', '402', '406'
              , '424', '433', '433', '439', '439', '445', '446', '446', '446', '446', '446'],
            ['公司与供货商', '0', '0', '0', '0', '2', '4', '6', '14', '24', '30', '34'
              , '42', '50', '82', '82', '98', '102', '104', '118', '120', '138', '182'
              , '192', '192', '222', '222', '230', '230', '230', '230', '230', '230', '230'],
            ['公司与产品', '7', '7', '7', '18', '21', '25', '51', '62', '84', '96', '102'
              , '130', '164', '187', '199', '202', '216', '227', '232', '232', '235', '235'
              , '238', '241', '241', '242', '242', '242', '242', '242', '242', '242', '242'],
          ]
    },
      xAxis: {
        type: 'category'
      }
    ,
      yAxis: {
        gridIndex: 0
      }
    ,
      grid: {
        top: '55%' //表格纵
      }
    ,
      series: [
           {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'line',
        smooth: true,
        seriesLayoutBy: 'row',
        emphasis: { focus: 'series' }
      },
      {
        type: 'pie',
        id: 'pie',
        radius: '40%',//圆饼大小
        center: ['48%', '30%'],//横坐标，纵坐标
        emphasis: {
          focus: 'self'
        },
        label: {
          formatter: '{b}: {@2012} ({d}%)'
        },
        encode: {
          itemName: 'product',
          value: '2012',
          tooltip: '2012'
        }
      }
      ]
    }
      ;

      chartInstance.setOption(option);

      chartInstance.on('updateAxisPointer', function (event) {
        const xAxisInfo = event.axesInfo[0];
        if (xAxisInfo) {
          const dimension = xAxisInfo.value + 1;
          chartInstance.setOption({
            series: {
              id: 'pie',
              label: {
                formatter: '{b}: {@[' + dimension + ']} ({d}%)'
              },
              encode: {
                value: dimension,
                tooltip: dimension
              }
            }
          });
        }
      });
    });

    return {chartDom};
  },
};
</script>
