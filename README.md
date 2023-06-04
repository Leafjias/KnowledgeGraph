# 产业链知识图谱前端界面

## 一、项目使用说明
```
Win+X,A进入系统管理员命令行窗口(虽然终端也能跑，但可能system rejected)
npm install element-plus --save
npm install vue-router@4
npm install @element-plus/icons-vue
npm install --save @element-plus/icons
npm install less-loader less --save-dev
npm install axios
npm install d3@4.13.0 # d3v4版本，事件处理d3.event这样表达
npm install d3 --save-dev # 下载最新版，但拖拽和缩放兼容性有点问题
npm install echarts-wordcloud -save
# 依赖安装二选一
npm install
```
### 项目知识点
元素组件库：https://element-plus.gitee.io/zh-CN

router动态路由：https://router.vuejs.org/zh/guide/

npm查看版本：http://npm.p2hp.com/

less高效CSS：https://less.bootcss.com/

Vuex响应式状态管理模式：https://vuex.vuejs.org/zh/guide/

axios网络请求数据传输：https://javasoho.com/axios/index.html

图标绘制库echarts：https://echarts.apache.org/
### 项目启动
```
npm run serve
```

### 项目打包
```
npm run build
```


### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## 二、代码说明
### 1. 代码结构
- **组件**存放在 `components` 文件夹
- **页面**存放在 `views` 文件夹
- **路由**存放在 `router` 文件夹
	- `index.js` —— 路由设置
- **依赖插件及版本说明等**在 `package.json` 
- **项目库安装使用及根目录**在 `main.js` 