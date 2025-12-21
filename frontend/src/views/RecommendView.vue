<template>
  <main class="recommend">
    <h1 class="title">어떤 상품을 찾고 계신가요?</h1>

    <!-- 카드 1: 예금/적금 + 은행 -->
    <section class="card card-bank">
      <div class="type-tabs" role="tablist">
        <button class="tab" :class="{ active: type === 'deposit' }" @click="type = 'deposit'">
          예금
        </button>
        <button class="tab" :class="{ active: type === 'savings' }" @click="type = 'savings'">
          적금
        </button>
      </div>

      <div class="bank-row">
        <button
          v-for="b in displayBanks"
          :key="b"
          class="bank-btn"
          :class="{ selected: selectedBank === b }"
          @click="selectBank(b)"
          type="button"
        >
          <span class="bank-circle">
            <span class="bank-initial">{{ bankInitial(b) }}</span>
          </span>
          <span class="bank-name">{{ shortBankName(b) }}</span>
        </button>

        <button class="bank-btn" type="button" @click="toggleAllBanks">
          <span class="bank-circle">
            <span class="bank-initial">≡</span>
          </span>
          <span class="bank-name">전체보기</span>
        </button>
      </div>

      <div v-if="showAllBanks" class="all-banks">
        <button
          v-for="b in banks"
          :key="b"
          class="pill"
          :class="{ selected: selectedBank === b }"
          @click="selectBank(b)"
          type="button"
        >
          {{ b }}
        </button>

        <button v-if="selectedBank" class="pill ghost" @click="clearBank" type="button">
          선택 해제
        </button>
      </div>
    </section>

    <!-- 카드 2: 조건 -->
    <section class="card card-filter">
      <!-- 매칭 상품 개수 표시 -->
      <div v-if="matchingCount !== null && targetAmount >= 1000000" class="match-info">
        <span v-if="countLoading" class="match-loading">
          <span class="spinner-small"></span> 확인 중...
        </span>
        <span v-else-if="matchingCount > 0" class="match-success">
          ✓ 현재 조건에 맞는 상품 <strong>{{ matchingCount }}개</strong>
        </span>
        <span v-else class="match-warning">
          ⚠️ 조건에 맞는 상품이 없습니다. 다른 조건을 선택해보세요.
        </span>
      </div>

      <!-- 기간 -->
      <div class="row">
        <div class="label">기간</div>
        <div class="control">
          <button
            v-for="month in monthOptions"
            :key="month"
            class="pill"
            :class="{ selected: targetMonths === month }"
            @click="targetMonths = month"
            type="button"
          >
            {{ month }}개월
          </button>
        </div>
      </div>

      <!-- 금액 -->
      <div class="row">
        <div class="label">금액</div>
        <div class="control">
          <input
            class="input"
            type="text"
            v-model="amountDisplay"
            @input="updateAmount"
            @keyup.enter="checkMatchingCount"
            placeholder="100만원 이상"
          />
          <button class="mini" type="button" @click="checkMatchingCount" :disabled="countLoading">
            확인
          </button>
        </div>
      </div>

      <!-- 비대면 -->
      <div class="row">
        <div class="label">비대면</div>
        <div class="control">
          <button
            class="pill"
            :class="{ selected: isNonFaceToFace === true }"
            @click="isNonFaceToFace = true"
            type="button"
          >
            비대면
          </button>
          <button
            class="pill"
            :class="{ selected: isNonFaceToFace === false }"
            @click="isNonFaceToFace = false"
            type="button"
          >
            방문
          </button>
          <button
            class="pill ghost"
            :class="{ selected: isNonFaceToFace === null }"
            @click="isNonFaceToFace = null"
            type="button"
          >
            선택안함
          </button>
        </div>
      </div>

      <!-- 예금자 보호 -->
      <div class="row">
        <div class="label">예금자 보호</div>
        <div class="control">
          <button
            class="pill"
            :class="{ selected: isDepositProtected === true }"
            @click="isDepositProtected = true"
            type="button"
          >
            보호
          </button>
          <button
            class="pill"
            :class="{ selected: isDepositProtected === false }"
            @click="isDepositProtected = false"
            type="button"
          >
            미보호
          </button>
          <button
            class="pill ghost"
            :class="{ selected: isDepositProtected === null }"
            @click="isDepositProtected = null"
            type="button"
          >
            선택안함
          </button>
        </div>
      </div>

      <div class="actions">
        <button
          class="search"
          @click="recommend"
          :disabled="loading || (matchingCount === 0 && matchingCount !== null)"
          type="button"
        >
          {{ loading ? '조회중...' : '검색하기' }}
        </button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
    </section>

    <!-- 카드 3: 결과 -->
    <section class="card card-result">
      <div class="result-header">
        <div>
          <h2 class="hello">
            안녕하세요 <span class="name">{{ userName }}님!</span>
          </h2>
          <p class="desc">
            검색 결과 조건에 맞는 <span class="highlight">{{ results.length }}건</span>의
            {{ productLabel }}을 발견했습니다.
          </p>
        </div>
        <div class="result-controls" v-if="results.length">
          <select v-model="sortOption" class="control-select" @change="applySorting">
            <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="results.length" class="list">
        <article
          v-for="(item, idx) in results"
          :key="item.product_id"
          class="result-item"
          @click="goToDetail(item.product_id)"
        >
          <div class="rank">{{ idx + 1 }}</div>
          <div class="item-content">
            <div class="item-left">
              <div class="bank-icon">💳</div>
              <div class="info">
                <div class="bank">{{ item.bank_name }}</div>
                <div class="prod">{{ item.name }}</div>
              </div>
            </div>
            <div class="rates">
              <div class="max">최고 {{ formatRate(item.max_rate) }}%</div>
              <div class="base">기본 {{ formatRate(item.base_rate) }}%</div>
            </div>
          </div>
        </article>
      </div>

      <div v-else-if="searched && results.length === 0" class="empty-container">
        <span class="empty-icon">🔍</span>
        <span class="empty-title">조건에 맞는 상품이 없습니다</span>
        <span class="empty-subtitle">다른 조건을 선택해주세요</span>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'
import { fetchBanks } from '@/api/products'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const type = ref('deposit')
const targetAmount = ref(1000000)
const targetMonths = ref(12)
const amountDisplay = ref('1,000,000')

const monthOptions = [1, 3, 6, 12, 24, 36]

const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)

const matchingCount = ref(null)
const countLoading = ref(false)

const sortOption = ref('max_rate')
const sortOptions = [
  { value: 'max_rate', label: '최고금리순' },
  { value: 'base_rate', label: '기본금리순' },
]

const banks = ref([])
const selectedBank = ref('')
const showAllBanks = ref(false)

const userName = ref('회원')

const isNonFaceToFace = ref(null)
const isDepositProtected = ref(null)

const displayBanks = computed(() => banks.value.slice(0, 5))
const productLabel = computed(() => (type.value === 'deposit' ? '예금' : '적금'))

const checkMatchingCount = async () => {
  console.log('[개수 체크] 시작 - 금액:', targetAmount.value)

  if (targetAmount.value < 1000000) {
    console.log('[개수 체크] 금액 부족 (100만원 미만)')
    matchingCount.value = null
    return
  }

  countLoading.value = true

  try {
    const payload = {
      type: type.value,
      target_amount: targetAmount.value,
      target_months: targetMonths.value,
      limit: 20,
    }

    if (selectedBank.value) {
      payload.bank_name = selectedBank.value
    }

    if (isNonFaceToFace.value !== null) {
      payload.is_non_face_to_face = isNonFaceToFace.value
    }

    if (isDepositProtected.value !== null) {
      payload.is_deposit_protected = isDepositProtected.value
    }

    console.log('[개수 체크] 요청 payload:', payload)

    const res = await apiClient.post('/products/recommend/', payload)
    matchingCount.value = res.data.results?.length || 0

    console.log('[개수 체크] 결과:', matchingCount.value, '개')
  } catch (e) {
    console.error('[개수 체크] 오류:', e)
    console.error('[개수 체크] 응답:', e?.response?.data)
    matchingCount.value = null
  } finally {
    countLoading.value = false
  }
}

watch(type, () => {
  selectedBank.value = ''
  isNonFaceToFace.value = null
  isDepositProtected.value = null
  showAllBanks.value = false
  targetMonths.value = 12
  targetAmount.value = 1000000
  amountDisplay.value = '1,000,000'
  results.value = []
  searched.value = false
  error.value = ''
  matchingCount.value = null

  checkMatchingCount()
})

watch([targetMonths, selectedBank, isNonFaceToFace, isDepositProtected], () => {
  checkMatchingCount()
})

let amountTimer = null
watch(targetAmount, (newVal) => {
  if (newVal >= 1000000) {
    clearTimeout(amountTimer)
    amountTimer = setTimeout(() => {
      checkMatchingCount()
    }, 500)
  } else {
    matchingCount.value = null
  }
})

onMounted(async () => {
  try {
    const res = await fetchBanks()
    banks.value = res.data.banks ?? []
  } catch (e) {
    console.error('은행 목록 조회 실패:', e)
  }

  checkMatchingCount()
})

const selectBank = (b) => {
  selectedBank.value = selectedBank.value === b ? '' : b
  showAllBanks.value = false
}

const toggleAllBanks = () => (showAllBanks.value = !showAllBanks.value)
const clearBank = () => (selectedBank.value = '')

const bankInitial = (name) => name?.[0] ?? '?'
const shortBankName = (name) =>
  name?.replace('주식회사 ', '').replace('농협은행주식회사', '농협') ?? name

const formatNumber = (num) => num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')

const formatRate = (rate) => {
  if (rate === null || rate === undefined) return '-'
  return Number(rate).toFixed(2)
}

const updateAmount = (e) => {
  const value = e.target.value.replace(/,/g, '')
  if (!isNaN(value) && value !== '') {
    targetAmount.value = parseInt(value)
    amountDisplay.value = formatNumber(value)
  } else if (value === '') {
    targetAmount.value = 0
    amountDisplay.value = ''
  }
}

const applySorting = () => {
  if (sortOption.value === 'max_rate') {
    results.value.sort((a, b) => (b.max_rate || 0) - (a.max_rate || 0))
  } else if (sortOption.value === 'base_rate') {
    results.value.sort((a, b) => (b.base_rate || 0) - (a.base_rate || 0))
  }
}

const goToDetail = (productId) => {
  router.push({
    path: `/products/${productId}`,
    query: {
      amount: targetAmount.value,
      months: targetMonths.value,
    },
  })
}

const recommend = async () => {
  loading.value = true
  error.value = ''
  searched.value = true

  try {
    if (!targetAmount.value || targetAmount.value < 1000000) {
      error.value = '금액은 100만원 이상부터 가능합니다.'
      results.value = []
      loading.value = false
      return
    }

    const payload = {
      type: type.value,
      target_amount: targetAmount.value,
      target_months: targetMonths.value,
      limit: 20,
    }

    if (selectedBank.value) {
      payload.bank_name = selectedBank.value
    }

    if (isNonFaceToFace.value !== null) {
      payload.is_non_face_to_face = isNonFaceToFace.value
    }

    if (isDepositProtected.value !== null) {
      payload.is_deposit_protected = isDepositProtected.value
    }

    console.log('요청 payload:', payload)

    const res = await apiClient.post('/products/recommend/', payload)

    let fetchedResults = res.data.results ?? []

    if (sortOption.value === 'max_rate') {
      fetchedResults.sort((a, b) => (b.max_rate || 0) - (a.max_rate || 0))
    } else if (sortOption.value === 'base_rate') {
      fetchedResults.sort((a, b) => (b.base_rate || 0) - (a.base_rate || 0))
    }

    results.value = fetchedResults

    console.log('추천 결과:', results.value)
  } catch (e) {
    console.error('추천 조회 오류:', e)
    const status = e?.response?.status

    if (status === 401) {
      error.value = '로그인이 필요합니다. 다시 로그인해주세요!'
    } else if (status === 400) {
      error.value = e?.response?.data?.detail ?? '입력 값을 확인해주세요.'
    } else {
      error.value = e?.response?.data?.detail ?? '추천 조회 중 오류가 발생했습니다.'
    }

    results.value = []
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.recommend {
  background: #fafafa;
  padding: 48px 0 80px;
}

.title {
  text-align: center;
  font-size: 40px;
  font-weight: 800;
  margin: 0 0 32px;
  color: #111827;
}

.card {
  width: 684px;
  margin: 0 auto 18px;
  background: #fff;
  border-radius: 20px;
  box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.08);
  padding: 22px;
}

.type-tabs {
  width: 147px;
  margin: 0 auto 16px;
  background: #fff;
  border-radius: 50px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  padding: 6px;
  display: flex;
  gap: 6px;
  justify-content: center;
}

.tab {
  border: 0;
  background: transparent;
  padding: 8px 16px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  color: #6393f2;
  transition: all 0.2s;
}

.tab.active {
  background: #6393f2;
  color: white;
}

.bank-row {
  display: flex;
  justify-content: center;
  gap: 16px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.bank-btn {
  border: 0;
  background: transparent;
  cursor: pointer;
  display: grid;
  place-items: center;
  gap: 8px;
  width: 90px;
  transition: all 0.2s;
}

.bank-circle {
  width: 80px;
  height: 80px;
  border-radius: 999px;
  border: 2px solid #e5e7eb;
  display: grid;
  place-items: center;
  background: white;
  transition: all 0.2s;
}

.bank-btn.selected .bank-circle {
  background: #eff6ff;
  border-color: #6393f2;
  border-width: 3px;
}

.bank-btn:hover .bank-circle {
  border-color: #6393f2;
  transform: translateY(-2px);
}

.bank-initial {
  font-weight: 800;
  color: #6393f2;
  font-size: 20px;
}

.bank-name {
  font-size: 12px;
  font-weight: 700;
  color: #6393f2;
}

.all-banks {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
}

.match-info {
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2px solid #bae6fd;
  border-radius: 16px;
  padding: 16px 20px;
  margin-bottom: 24px;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(99, 147, 242, 0.1);
}

.match-loading {
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2.5px solid #e5e7eb;
  border-top-color: #6393f2;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.match-success {
  color: #059669;
  display: block;
}

.match-success strong {
  color: #047857;
  font-size: 18px;
  font-weight: 900;
}

.match-warning {
  color: #dc2626;
  display: block;
}

.row {
  display: grid;
  grid-template-columns: 92px 1fr;
  align-items: start;
  gap: 12px;
  margin: 16px 0;
}

.label {
  display: inline-grid;
  place-items: center;
  height: 36px;
  border-radius: 999px;
  background: #6393f2;
  color: #fff;
  font-weight: 800;
  font-size: 13px;
}

.control {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.input {
  flex: 1;
  height: 40px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  padding: 0 12px;
  outline: none;
  font-size: 13px;
  transition: all 0.2s;
}

.input:focus {
  border-color: #6393f2;
  box-shadow: 0 0 0 3px rgba(99, 147, 242, 0.1);
}

.input::placeholder {
  color: #9ca3af;
  font-size: 12px;
}

.mini {
  height: 40px;
  padding: 0 14px;
  border-radius: 10px;
  border: 0;
  background: #6393f2;
  color: white;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.mini:hover {
  background: #4f7de0;
}

.mini:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.pill {
  border: 1px solid #e5e7eb;
  background: #fff;
  border-radius: 999px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.pill:hover {
  border-color: #6393f2;
}

.pill.selected {
  border: 2px solid #6393f2;
  background: #eff6ff;
  color: #6393f2;
}

.pill.ghost {
  border-style: dashed;
  color: #9ca3af;
}

.pill.ghost:hover {
  background: #f9fafb;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.search {
  height: 42px;
  padding: 0 24px;
  border-radius: 12px;
  border: 0;
  background: #111827;
  color: white;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
}

.search:hover:not(:disabled) {
  background: #1f2937;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.search:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.error {
  color: #ef4444;
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
}

.result-controls {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.control-select {
  height: 36px;
  padding: 0 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #4a5568;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.control-select:hover {
  border-color: #6393f2;
}

.control-select:focus {
  outline: none;
  border-color: #6393f2;
  box-shadow: 0 0 0 3px rgba(99, 147, 242, 0.1);
}

.hello {
  font-size: 28px;
  font-weight: 900;
  margin: 0 0 8px;
  color: #111827;
}

.name {
  color: #6393f2;
}

.desc {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.highlight {
  color: #6393f2;
  font-weight: 700;
}

.list {
  display: grid;
  gap: 14px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  background: #fff;
  border: 2px solid #f3f4f6;
  transition: all 0.2s;
  cursor: pointer;
}

.result-item:hover {
  border-color: #6393f2;
  box-shadow: 0 4px 12px rgba(99, 147, 242, 0.15);
  transform: translateY(-2px);
}

.rank {
  font-size: 20px;
  font-weight: 900;
  color: #d1d5db;
  min-width: 30px;
  text-align: center;
}

.item-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1;
  gap: 16px;
}

.item-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bank-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  display: grid;
  place-items: center;
  font-size: 24px;
}

.info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bank {
  font-weight: 800;
  color: #111827;
  font-size: 15px;
}

.prod {
  color: #6b7280;
  font-weight: 600;
  font-size: 13px;
}

.rates {
  text-align: right;
}

.max {
  color: #6393f2;
  font-weight: 900;
  font-size: 18px;
  margin-bottom: 2px;
}

.base {
  font-size: 12px;
  color: #9ca3af;
  font-weight: 600;
}

.empty-container {
  text-align: center;
  padding: 60px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.empty-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.empty-subtitle {
  font-size: 14px;
  color: #6b7280;
}
</style>
