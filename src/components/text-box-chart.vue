<template>
  <div class="TextBoxChart">
     <div v-for="(newsItem, /*index*/) in news" :key="newsItem.id">
      <h3>{{ newsItem.name }}</h3>
      <p>作者: {{ newsItem.作者 }}</p>
      <p>新闻内容: {{ newsItem.影响 }}</p>
      <p>时间: {{ newsItem.时间 }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextBoxChart",
  props: {
    news:{
      //type:Object,
       type: Array,
      required:true,
    }
  },
};
</script>

<style>
.TextBoxChart {
  position: absolute;
  width: 530px;
  height: 150px;
  margin-left: 770px;
  margin-top: -470px;
  font-size: 13px;
  text-indent: 2em;
  line-height: 1.5em;
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  border-radius: 5px;
  overflow-y: scroll;
}
</style>

