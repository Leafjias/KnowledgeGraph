<template>
  <svg width="1000" height="550" id="svg1"></svg>
</template>

<script>
import {watchEffect, onMounted, onUnmounted} from "vue";
import * as d3 from 'd3';
import axios from "axios";

export default {
  name: 'ForceGraph',
  props: {
    url: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      nodes: [],
      links: [],
      colors: ['#aaaaff', '#f1662b', '#FFC0CB', "#0290c4"], // 颜色分组
      link_colors: ['#cd2626', '#63aa40', '#0021ff',
        '#d13ebb', '#f6038c', '#e1d70d', '#1bcc61'],//线的颜色
      statistics: {
        环节: 0,
        公司: 0,
        产品: 0,
        环节与环节: 0,
        环节与公司: 0,
        环节与产品: 0,
        公司与公司: 0,
        公司与产品: 0,
        产品与产品: 0
      },
    }
  },
  mounted() {
    onMounted(() => {
      this.initGraph();
    });
    watchEffect(() => {
      if (this.url) {
        this.loadData();
      }
    });
    onUnmounted(() => {
      this.clearData();
    });
  },
  methods: {
    clearData() {
      this.nodes = [];
      this.links = [];
    },
    async loadData() {
      try {
        this.clearData();
        const response = await axios.get(this.url);
        const companies = response.data.results.公司;
        const products = response.data.results.产品;
        const sectors = response.data.results.环节;
        const news = response.data.results.新闻;
        const ss = response.data.results.环节与环节;
        const sc = response.data.results.环节与公司;
        const sp = response.data.results.环节与产品;
        const cc = response.data.results.公司与供应商;
        const cp = response.data.results.公司与产品;
        const pp = response.data.results.产品与产品;
        const cn = response.data.results.公司与新闻;

        // 更新统计信息
        this.statistics.环节 = sectors.length;
        this.statistics.公司 = companies.length;
        this.statistics.产品 = products.length;
        this.statistics.环节与环节 = ss.length;
        this.statistics.环节与公司 = sc.length;
        this.statistics.环节与产品 = sp.length;
        this.statistics.公司与公司 = cc.length;
        this.statistics.公司与产品 = cp.length;
        this.statistics.产品与产品 = pp.length;
        //console.log(this.statistics);
        // 向父组件发送统计信息
        this.$emit('update-statistics', this.statistics);
        // console.log(companies);
        for (const item of products) {
          if (item.name === undefined || item.id === undefined) {
            //console.error('Undefined product:', item);
          } else {
            this.nodes.push({
              name: item.name,
              id: item.id,
              group: 2 //结点颜色代号
            })
            //console.log(item.name);
          }
        }
        for (const item of companies) {
          const dateString = item.成立日期 + "/" + item.首发上市日;
          const parts = dateString.split("/");
          const dateObj = new Date(parts[0], parts[1] - 1, parts[2]);//月份需要减1，因为JS中的月份从0开始计数
          const dateObj1 = new Date(parts[3], parts[4] - 1, parts[5]);
          if (item.name === undefined || item.id === undefined) {
            //console.error('Undefined company:', item);
          } else {
            this.nodes.push({
              name: item.name,
              id: item.id,
              group: 1, //结点颜色代号
              city: item.city,
              fullname: item.fullname,
              code: item.code,
              where: item.所属地区,
              web: item.公司网址,
              date: dateObj,
              date1: dateObj1
            })
          }
        }
        for (const item of sectors) {
          if (item.name === undefined || item.id === undefined) {
            //console.error('Undefined link:', item);
          } else {
            this.nodes.push({
              name: item.name,
              id: item.id,
              group: 0 //结点颜色代号
            })
          }
        }
        for (const item of news) {
          if (item.name === undefined || item.id === undefined) {
            //console.error('Undefined product:', item);
          } else {
            this.nodes.push({
              name: item.name,
              id: item.id,
              group: 3 //结点颜色代号
            })
            //console.log(item.name);
          }
        }
        for (const item of ss) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 0
            })
          }
        }
        for (const item of sc) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 1
            })
          }
        }
        for (const item of sp) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 2
            })
          }
        }
        for (const item of cc) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 3
            })
          }
        }
        for (const item of cp) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 4
            })
          }
        }
        for (const item of pp) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 5
            })
          }
        }
        for (const item of cn) {
          if (item.id_from === undefined || item.id_to === undefined) {
            //console.error('Undefined ss:', item);
          } else {
            this.links.push({
              source: item.id_from,
              target: item.id_to,
              type: item.rel,
              group: 6
            })
          }
        }
        //console.log('links:', this.links);
        //console.log('nodes:', this.nodes);
        this.drawGraph();
      } catch (error) {
        //console.error(error)
      }
    },
    initGraph() {
      // 调用 loadData 方法加载数据
      this.loadData();
    },
    drawGraph() {
      // 在这里先清除之前的图形
      d3.select("#svg1").selectAll("*").remove();
      const svg = d3.select("#svg1"), //选择svg1
          width = svg.attr("width"), //设定宽度
          height = svg.attr("height"); //设定高度

      const defs = svg.append('defs');

// 箭头定义
      defs.append('marker')
          .data(this.links)
          .attr('id', 'arrow')
          .attr('viewBox', '0 -5 10 10')
          .attr('refX', 3) // 修改 refX 值使箭头更靠近线条端点
          .attr('refY', 0)
          .attr('markerWidth', 3) // 减小箭头宽度
          .attr('markerHeight', 3) // 减小箭头高度
          .attr('orient', 'auto')
          .append('path')
          .attr('d', 'M0,-4L8,0L0,4') // 修改箭头形状，使其更细长
          .attr('fill', d => getLinkStyle(d).stroke);


      //利用d3.forceSimulation()定义d3力导向图，力模拟
      const simulation = d3.forceSimulation()
          //让互相之间有link的节点保持一个特定的距离在保持一定距离的前提下，若超出该范围，就会多增加一个力
          .force("link", d3.forceLink().id(function (d) {
                return d.id;
              })
                  .distance(80) // link 之间的距离
                  .strength(0.1) // link 之间的相互作用力量
          )
          //粒子之间两两作用的力，如果为正就互相吸引，为负就互相排斥，要设置strength规定力的大小
          .force("charge", d3.forceManyBody().strength(-25))
          .force("center", d3.forceCenter(width / 2, height / 2))//指向某一个中心的力，会尽可能让粒子向中心靠近或重合
          .force("collision", d3.forceCollide(45)) // 碰撞检测，避免结点重叠
      // ***********很重要！！！！！在此处保存Vue组件的 this 引用
      const vm = this;
      //simulation中ticked数据初始化并生成图形
      //通过tick事件来更新节点的状态的，状态包括位置，速度，加速度等
      simulation.nodes(this.nodes).on("tick", ticked); //必须放前面，不然初始化不了位置坐标
      simulation.force("link").links(this.links).distance(d => { // 每一边的长度
        let distance = 8
        switch (d.group) {
          case 0:
            distance += 30;
            break;
          case 1:
            distance += 25;
            break;
          case 2:
            distance += 21;
            break;
          case 3:
            distance += 18;
            break;
          case 4:
            distance += 15;
            break;
          case 5:
            distance += 12;
            break;
          default:
            distance += 9;
            break;
        }
        return distance * 2
      });

      function ticked() {
        // 更新贝塞尔曲线的路径
        link.attr('d', function (d) {
          const dx = d.target.x - d.source.x;
          const dy = d.target.y - d.source.y;
          const dr = Math.sqrt(dx * dx + dy * dy);
          const mx = (d.source.x + d.target.x) / 2;
          const my = (d.source.y + d.target.y) / 2;
          const qx = mx + dy / dr * 30; // 30 控制曲线的弯曲程度
          const qy = my - dx / dr * 30;
          //return `M${d.source.x},${d.source.y}Q${qx},${qy} ${d.target.x},${d.target.y}`;
          const r = d.target.r || (d.target.group === 0 ? 16 : d.target.group === 1 ? 12 : d.target.group === 2 ? 8 : 9);
          //const r = d.target.r || 16; // 获取终点半径，如果没有设置则默认为 9
          const tr = r + 4; // 曲线终点距离目标节点边缘的距离
          const tx = d.target.x + tr * (d.source.x - d.target.x) / dr;
          const ty = d.target.y + tr * (d.source.y - d.target.y) / dr;
          return `M${d.source.x},${d.source.y}Q${qx},${qy} ${tx},${ty}`;
        });



        linktext.attr("x", d => {
          const dx = d.target.x - d.source.x;
          const dy = d.target.y - d.source.y;
          const dr = Math.sqrt(dx * dx + dy * dy);
          const mx = (d.source.x + d.target.x) / 2;
          const qx = mx + dy / dr * 30; // 30 控制曲线的弯曲程度
          return (d.source.x + qx) / 2;
        })
            .attr("y", d => {
              const dx = d.target.x - d.source.x;
              const dy = d.target.y - d.source.y;
              const dr = Math.sqrt(dx * dx + dy * dy);
              const my = (d.source.y + d.target.y) / 2;
              const qy = my - dx / dr * 30;
              return (d.source.y + qy) / 2;
            });
        node.attr("cx", d => d.x)
            .attr("cy", d => d.y)

        text.attr("x", d => d.x)
            .attr("y", d => d.y)

      }

      // g用于绘制所有边,selectALL选中所有的line,并绑定数据data(links),enter().append("line")添加元素
      // 使用<path>元素而非<line>元素
      const link = svg.append('g')
          .attr("class", "links")
          .selectAll("path")
          .data(this.links)
          .enter().append("path")
          .attr('stroke', d => getLinkStyle(d).stroke)
          .attr('stroke-width', d => getLinkStyle(d).strokeWidth) //根据关系类型设置线宽
          .attr('stroke-dasharray', d => getLinkStyle(d).strokeDasharray) //根据关系类型设置线样式
          .attr('fill', 'none') // 设置填充为无
          .attr('marker-end', 'url(#arrow)'); // 在曲线中间添加箭头


      //边上的文字，即实体之间的关系
      const linktext = svg.append('g')
          .attr("class", "linktexts")
          .selectAll("text")
          .data(this.links)
          .enter().append("text")
          .style("display", "block")
          .style('text-anchor', 'middle')
          .style('fill', '#444')
          .attr("font-size", 6)
          .text(function (d) {
            return d.type; //绑定关系连线上的文字
          });
      //圆
      const node = svg.append('g')
          .attr("class", "nodes")
          .selectAll("circle")  //选中所有的圆
          .data(this.nodes) //修改为指定结点集
          .enter().append("circle")
          .attr("r", function (d) {
            let size = 9
            switch (d.group) {
              case 0:
                size = 9
                break;
              case 1:
                size = 7;
                break;
              case 2:
                size = 5;
                break;
              default:
                size = 4;
                break;
            }
            return size * 2//结点圆的直径
          })
          .attr('fill', function (d) { // 填充的颜色
            return vm.colors[d.group]; //颜色的this和tick绑定的this不同，用tick前需保存
          })
          .attr('stroke', '#000') // 添加黑色轮廓
          .attr('stroke-width', '1') // 调整轮廓宽度
          //.attr('stroke', 'none')    // 没有描边
          .attr('name', function (d) {
            return d.name;    //圆的名字
          })
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));
      // 文本
      const text = svg.append('g')
          .attr("class", "texts")
          .selectAll("text")
          .data(this.nodes)
          .enter().append("text")
          .attr("font-size", function (d) {
            let size
            switch (d.group) {
              case 0:
                size = 8;
                break;
              case 1:
                size = 7;
                break;
              case 2:
                size = 6;
                break;
              default:
                size = 5;
                break;
            }
            return size//结点圆的直径
          })
          .attr("fill", '#444') //文本用黑色
          .attr('name', function (d) {
            return d.name;//文字内容绑定
          })
          .attr('text-anchor', 'middle') //文本居中
          .text(function (d) {
            if (d.name.length <= 4) return d.name;
            else return d.name.substring(0, 3) + '..';
          })
          .call(d3.drag()
              .on("start", dragstarted)
              .on("drag", dragged)
              .on("end", dragended));

      //选择线条样式的函数
      function getLinkStyle(d) {
        switch (d.type) {
          case '上游':
            return {strokeWidth: 4, strokeDasharray: '5,5', stroke: '#FF6F00'}; // 较粗的橙色虚线
          case '属于':
            return {strokeWidth: 3, strokeDasharray: '', stroke: '#3F51B5'}; // 紫色实线
          case '构成':
            return {strokeWidth: 3, strokeDasharray: '', stroke: '#2196F3'}; // 蓝色实线
          case '提炼':
            return {strokeWidth: 2, strokeDasharray: '', stroke: '#9C27B0'}; // 紫罗兰实线
          case '发展趋势':
            return {strokeWidth: 2, strokeDasharray: '2,2', stroke: '#009688'}; // 绿色虚线
          case '相关产品':
            return {strokeWidth: 2, strokeDasharray: '', stroke: '#4CAF50'}; // 绿色实线
          case '主营产品':
            return {strokeWidth: 2, strokeDasharray: '', stroke: '#FFC107'}; // 红黄色实线
          case '产品小类':
            return {strokeWidth: 1, strokeDasharray: '', stroke: '#795548'}; // 棕色实线
          case '供应商':
            return {strokeWidth: 1, strokeDasharray: '1,1', stroke: '#E91E63'}; // 粉红色虚线
          case '客户':
            return {strokeWidth: 1, strokeDasharray: '1,1', stroke: '#CDDC39'}; // 绿黄色虚线
          case '上游材料':
            return {strokeWidth: 1, strokeDasharray: '', stroke: '#FF5722'}; // 橙红色实线
          case '下游产品':
            return {strokeWidth: 1, strokeDasharray: '', stroke: '#607D8B'}; // 蓝灰色实线
          case '关联':
            return {strokeWidth: 1, strokeDasharray: '1,1', stroke: '#9E9E9E'}; // 灰色虚线
          default:
            return {strokeWidth: 1, strokeDasharray: '', stroke: '#000000'}; // 黑色实线
        }


      }

      //d3v4版本事件需要d3.event这样表达(缩放和拖拽同理)，v7不需要，
      //鼠标选中边上文字拖动即可实现全局拖动
      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      //拖拽中的回调函数，参数还是为node节点，这里不断的更新节点的固定坐标根据鼠标事件的坐标
      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      //拖拽结束回调函数，参数也是node节点，判断事件状态动画系数设置为0结束动画，并设置固定坐标都为null。
      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      // 给node加title, 当鼠标悬浮在圆圈上的时候，显示结点名称
      node.append('title').text(function (d) {
        return d.name;
      });
      text.append('title').text(function (d) {
        return d.name;
      });

      //处理缩放可缩放范围：8倍
      svg.call(d3.zoom().scaleExtent([1 / 8, 8]).on("zoom", () => {
        link.attr("transform", d3.event.transform);
        node.attr("transform", d3.event.transform);
        text.attr("transform", d3.event.transform);
        linktext.attr('transform', d3.event.transform);
      }));
      svg.on('click', () => {
        this.$emit('clickNode', null); // 点击空白区域时取消选择的节点
      });
      // 添加节点点击事件监听器
      node.on('click', (d) => {
        this.$emit('clickNode', d); // 触发父组件的showNodeInfo方法
      });
      // 添加节点点击事件监听器
      text.on('click', (d) => {
        this.$emit('clickNode', d); // 触发父组件的showNodeInfo方法
      });
    },
  }
}
</script>
