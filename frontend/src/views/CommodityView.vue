<template>
  <div class="commodity-page">
    <h2>현물 상품 비교</h2>

    <div class="controls">
      <div class="date-field">
        <label>시작일</label>
        <input type="date" v-model="startDate" />
      </div>

      <div class="date-field">
        <label>종료일</label>
        <input type="date" v-model="endDate" />
      </div>

      <div class="buttons">
        <button
          :class="{ active: asset === 'gold' }"
          @click="changeAsset('gold')"
        >
          금
        </button>
        <button
          :class="{ active: asset === 'silver' }"
          @click="changeAsset('silver')"
        >
          은
        </button>
      </div>
    </div>

    <div class="chart-wrapper">
      <PriceChart :data="filteredData" :asset="asset" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import * as XLSX from 'xlsx'
import PriceChart from '@/components/commodity/PriceChart.vue'

const asset = ref('gold')
const startDate = ref('')
const endDate = ref('')
const rawData = ref([])

const loadExcel = async () => {
  const file =
    asset.value === 'gold'
      ? '/assets/data/Gold_prices.xlsx'
      : '/assets/data/Silver_prices.xlsx'

  const res = await fetch(file)
  const buf = await res.arrayBuffer()
  const wb = XLSX.read(buf)
  const sheet = wb.Sheets[wb.SheetNames[0]]
  const json = XLSX.utils.sheet_to_json(sheet)

  rawData.value = json.map(row => ({
    date: XLSX.SSF.format('yyyy-mm-dd', row.Date),
    price: Number(String(row['Close/Last']).replace(/,/g, '')),
  }))
}

const filteredData = computed(() => {
  if (!startDate.value && !endDate.value) return rawData.value

  const start = startDate.value ? new Date(startDate.value) : null
  const end = endDate.value ? new Date(endDate.value) : null

  if (start && end && start > end) {
    return []
  }

  return rawData.value.filter(d => {
    const cur = new Date(d.date)
    if (start && cur < start) return false
    if (end && cur > end) return false
    return true
  })
})

const changeAsset = async (type) => {
  asset.value = type
  await loadExcel()
}

onMounted(loadExcel)
</script>

<style scoped>
/* 전체 페이지 */
.commodity-page {
  padding: 20px;
  max-width: 1200px;   
  margin: 0 auto;    
}

/* 제목 */
h2 {
  color: #6393F2;
  margin-bottom: 20px;
}

/* 필터 바 */
.controls {
  display: flex;
  align-items: flex-end;
  gap: 32px;
  margin-bottom: 28px;
}

/* 날짜 필드 */
.date-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.date-field label {
  font-size: 13px;
  font-weight: 600;
  color: #080808;
}

.date-field input[type='date'] {
  width: 180px;
  padding: 10px 12px;
  font-size: 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  outline: none;
  transition: all 0.2s ease;
}

.date-field input[type='date']:focus {
  border-color: #e0e0e0;
  box-shadow: 0 0 0 3px rgba(99, 147, 242, 0.2);
}

/* 금 / 은 버튼 */
.buttons {
  display: flex;
  gap: 10px;
  margin-left: 8px;
}

.buttons button {
  height: 42px;
  padding: 0 18px;
  border-radius: 8px;
  font-weight: 600;
  border: 1.5px solid #6393F2;
  background: white;
  color: #6393F2;
  cursor: pointer;
  transition: all 0.2s ease;
}

.buttons button:hover {
  background: rgba(99, 147, 242, 0.12);
}

.buttons .active {
  background: #6393F2;
  color: white;
}

.chart-wrapper {
  max-width: 1100px; 
  margin: 0 auto;
}
</style>
