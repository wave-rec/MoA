<template>
  <div>
    <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const props = defineProps({
  data: Array,
  asset: String,
})

const chartRef = ref(null)
const chartInstance = ref(null)
const errorMsg = ref('')

const drawChart = () => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  if (!props.data.length) {
    errorMsg.value = '선택된 조건에 해당하는 데이터가 없습니다.'
    return
  }

  errorMsg.value = ''

  chartInstance.value = new Chart(chartRef.value, {
    type: 'line',
    data: {
      labels: props.data.map(d => d.date),
      datasets: [
        {
          label: props.asset === 'gold' ? 'Gold Price' : 'Silver Price',
          data: props.data.map(d => d.price),
          borderColor: '#6393F2',
          backgroundColor: 'rgba(99,147,242,0.15)',
          tension: 0.3,
        },
      ],
    },
    options: {
        responsive: true,
        scales: {
            y: {
            beginAtZero: false,
            },
        },
    },
  })
}

watch(() => props.data, drawChart)

onMounted(drawChart)
</script>

<style scoped>
.error {
  color: red;
  margin-bottom: 10px;
}
</style>
