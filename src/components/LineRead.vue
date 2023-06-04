<template>
  <div ref="chart" :style="{ width: chartWidth, height: chartHeight }"></div>
</template>

<script>
import axios from "axios";
export default {
  name: "LineRead",
  props: {
    chartWidth: {
      type: String,
      default: "800px",
    },
    chartHeight: {
      type: String,
      default: "500px",
    },
    company: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      stockData: {},
      newsData: [],
      specialPoints: [],
    };
  },
  mounted() {
    this.getCompanyData(this.company);
  },
  watch: {
    company(newVal) {
      this.getCompanyData(newVal);
    },
  },
  methods: {
    async getCompanyData(companyName = "") {
      try {
        const response = await axios.get(
          `http://127.0.3.1:5050/datas/find/?value=${encodeURIComponent(companyName)}&type=company`
        );
        const results = response.data.results;
        this.stockData = results["股价信息"];
        this.newsData = results["新闻"].map((newsItem) => ({
          id: newsItem.id,
          name: newsItem.name,
          type: newsItem.type,
          作者: newsItem.作者,
          影响: newsItem.影响,
          时间: newsItem.时间,
        }));
        this.processSpecialPoints();
        this.$emit("chart-data-ready", {
          stockData: this.stockData,
          newsData: this.newsData,
          specialPoints: this.specialPoints,
        });
      } catch (error) {
        console.log(error);
        this.stockData = {};
        this.newsData = [];
      }
    },
    processSpecialPoints() {
      this.specialPoints = []; // 初始化为空数组
      for (const newsItem of this.newsData) {
        const newsDate = newsItem.时间.replace(/-/g, "");
        if (Object.prototype.hasOwnProperty.call(this.stockData, newsDate)) {
          const stockPrice = this.stockData[newsDate];
          const specialPoint = {
            date: newsItem.时间,
            price: stockPrice,
          };
          this.specialPoints.push(specialPoint);
        }
      }
    },
  },
};
</script>