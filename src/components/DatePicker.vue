<template>
  <el-form-item label="时间选择:">
    <el-date-picker
      v-model="date1"
      type="date"
      end-placeholder="截止日期"
      @change="handleChange"
    />
    <el-button @click="year_add">Time Hop</el-button>
  </el-form-item>
</template>
<script setup>
import { ref, defineEmits } from 'vue'

const emits = defineEmits(['update:value'])
const date1 = ref(new Date(2020, 1, 1))
function year_add() {
  //console.log(date1);
  const year = date1.value.getFullYear() + 1
  const month = date1.value.getMonth()
  const day = date1.value.getDate()
  date1.value = new Date(year, month, day)
  emits('update:value', date1.value)
  //console.log(date1);
}
function handleChange() {
  emits('update:value', date1.value)
}
</script>
