<template>
  <main class="product-detail">
    <!-- 로딩 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>상품 정보를 불러오는 중...</p>
    </div>

    <!-- 에러 -->
    <div v-else-if="error" class="error-container">
      <p class="error">{{ error }}</p>
      <button @click="$router.back()" class="back-btn">돌아가기</button>
    </div>

    <!-- 상품 상세 -->
    <div v-else-if="product" class="detail-container">
      <!-- 상품 헤더 카드 -->
      <div class="product-header-card">
        <div class="header-content">
          <div class="bank-logo">
            <img :src="getBankLogo(product.bank_name)" :alt="product.bank_name" />
          </div>
          <div class="product-info">
            <h2 class="bank-name">{{ product.bank_name }}</h2>
            <h1 class="product-name">{{ product.name }}</h1>
            <div class="tags">
              <span class="tag tag-primary">{{ productTypeLabel }}</span>
              <span v-if="product.is_non_face_to_face" class="tag tag-secondary">비대면가능</span>
            </div>
          </div>
          <div class="rate-highlight">
            <div class="max-rate">
              최고 금리 <span class="rate-number">{{ formatRate(product.max_rate) }}%</span>
            </div>
            <div class="base-rate-info">
              기본 금리 {{ formatRate(product.base_rate) }}% ({{ targetMonths }}개월 기준)
            </div>
          </div>
        </div>
      </div>

      <!-- AI 한줄평 카드 -->
      <div class="ai-summary-card">
        <div class="ai-header">
          <div class="ai-icon">🤖</div>
          <h3 class="ai-title">AI 한줄평</h3>
          <span class="ai-badge">Beta</span>
        </div>

        <div v-if="aiLoading" class="ai-loading">
          <div class="ai-spinner"></div>
          <p>AI가 상품을 분석하고 있습니다...</p>
        </div>

        <div v-else-if="aiError" class="ai-error">
          <p>{{ aiError }}</p>
          <button @click="fetchAIAnalysis" class="retry-btn">다시 시도</button>
        </div>

        <div v-else class="ai-content">
          <p class="ai-summary">{{ aiSummary }}</p>
          <button class="ai-detail-btn" @click="showAIDetailModal = true">상세 분석 보기</button>
        </div>
      </div>

      <!-- 예상 수령액 & 우대조건 -->
      <div class="info-cards-row">
        <!-- 예상 수령액 -->
        <div class="expected-amount-card">
          <h3 class="card-title">예상 수령액</h3>
          <div class="amount-info">
            <div class="amount-row">
              <span class="amount-label">기본금리 적용 시</span>
              <span class="amount-value">{{ formatAmount(expectedAmount.base) }}원</span>
            </div>
            <div class="amount-row">
              <span class="amount-label">최고금리 적용 시</span>
              <span class="amount-value">{{ formatAmount(expectedAmount.max) }}원</span>
            </div>
          </div>
          <div class="maturity-badge">
            <span class="badge-label">목표 달성률</span>
            <span class="badge-value">{{ maturityRate }}%</span>
          </div>
        </div>

        <!-- 우대조건 -->
        <div class="preferential-card">
          <h3 class="card-title">우대조건</h3>
          <div v-if="product.prefer_condition_text" class="preferential-list">
            <div
              v-for="(condition, idx) in parsePreferentialConditions(product.prefer_condition_text)"
              :key="idx"
              class="preferential-item"
            >
              <span class="preferential-text">{{ condition.text }}</span>
              <span class="preferential-rate">{{ condition.rate }}</span>
            </div>
          </div>
          <p v-else class="no-preferential">우대조건 정보가 없습니다.</p>
        </div>
      </div>

      <!-- 금리 정보 테이블 -->
      <div class="rate-table-card">
        <h3 class="card-title">금리 정보</h3>
        <table class="rate-table">
          <thead>
            <tr>
              <th>기간</th>
              <th>기본금리</th>
              <th>최고금리</th>
              <th>금리 방식</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="rate in sortedRates" :key="rate.save_terms_months">
              <td>{{ rate.save_terms_months }}개월</td>
              <td>{{ formatRate(rate.base_rate) }}%</td>
              <td class="highlight-rate">{{ formatRate(rate.max_rate) }}%</td>
              <td>{{ rate.rate_type || '복리' }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="!product.rates || product.rates.length === 0" class="no-data">
          금리 정보가 없습니다.
        </p>
      </div>

      <!-- 가입 버튼 -->
      <div class="action-section">
        <button
          v-if="authStore.isLogin"
          @click="handleSubscribe"
          :disabled="subscribing"
          class="subscribe-btn"
        >
          {{ subscribing ? '처리 중...' : '이 상품 가입하기' }}
        </button>
        <p v-else class="login-required">
          상품 가입은 로그인 후 이용 가능합니다.
          <router-link to="/login" class="login-link">로그인하기</router-link>
        </p>
      </div>
    </div>

    <!-- AI 상세 분석 모달 -->
    <div v-if="showAIDetailModal" class="modal-overlay" @click="showAIDetailModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>AI 상세 분석</h3>
          <button class="modal-close" @click="showAIDetailModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div class="ai-analysis-section">
            <h4>📊 종합 분석</h4>
            <p>{{ aiDetailedAnalysis }}</p>
          </div>

          <div class="ai-analysis-section">
            <h4>💡 추천 이유</h4>
            <ul class="ai-reasons">
              <li v-for="(reason, idx) in aiReasons" :key="idx">{{ reason }}</li>
            </ul>
          </div>

          <div class="ai-analysis-section">
            <h4>⚠️ 주의사항</h4>
            <p>{{ aiWarning }}</p>
          </div>

          <p class="ai-disclaimer">* AI 분석 결과는 참고용이며, 실제 금융 상담을 권장합니다.</p>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import apiClient from '@/api/client'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const product = ref(null)
const loading = ref(true)
const error = ref('')
const subscribing = ref(false)
const showAIDetailModal = ref(false)

// AI 관련 상태
const aiLoading = ref(false)
const aiError = ref('')
const aiSummary = ref('')
const aiDetailedAnalysis = ref('')
const aiReasons = ref([])
const aiWarning = ref('')

// 추천 페이지에서 전달받은 값
const targetAmount = ref(Number(route.query.amount) || 1000000)
const targetMonths = ref(Number(route.query.months) || 12)

const productTypeLabel = computed(() => {
  return product.value?.type === 'DEPOSIT' ? '예금' : '적금'
})

const sortedRates = computed(() => {
  if (!product.value?.rates) return []
  return [...product.value.rates].sort((a, b) => a.save_terms_months - b.save_terms_months)
})

// 예상 수령액 계산
const expectedAmount = computed(() => {
  if (!product.value) return { base: 0, max: 0 }

  const principal = targetAmount.value
  const months = targetMonths.value
  const baseRate = product.value.base_rate / 100 / 12
  const maxRate = product.value.max_rate / 100 / 12

  // 복리 계산 (월복리)
  const baseAmount = Math.round(principal * Math.pow(1 + baseRate, months))
  const maxAmount = Math.round(principal * Math.pow(1 + maxRate, months))

  return {
    base: baseAmount,
    max: maxAmount,
  }
})

// 목표 달성률 계산
const maturityRate = computed(() => {
  const rate = (expectedAmount.value.max / targetAmount.value) * 100
  return Math.round(rate)
})

const formatRate = (rate) => {
  if (rate === null || rate === undefined) return '-'
  return Number(rate).toFixed(2)
}

const formatAmount = (amount) => {
  return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 은행 로고 매핑
const getBankLogo = (bankName) => {
  if (!bankName) return '/assets/banks/default.png'

  const logoMap = {
    국민: 'kb.png',
    신한: 'shinhan.png',
    우리: 'woori.png',
    하나: 'hana.png',
    카카오: 'kakao.png',
    토스: 'toss.png',
    케이: 'kbank.png',
    한국스탠다드차타드: 'sc.png',
    제일: 'sc.png',

    중소기업: 'ibk.png',
    기업: 'ibk.png',
    한국산업: 'kdb.png',
    산업: 'kdb.png',
    수협: 'sh.png',
    농협: 'nh.png',

    경남: 'busan.png',
    광주: 'kjb.png',
    부산: 'busan.png',
    전북: 'jb.png',
    제주: 'jj.png',
    아이엠: 'iam.png',
    대구: 'daegu.png',
  }

  const key = Object.keys(logoMap).find((k) => bankName.includes(k))

  return key ? `/assets/banks/${logoMap[key]}` : '/assets/banks/default.png'
}

// 우대조건 파싱
const parsePreferentialConditions = (text) => {
  if (!text) return []

  const conditions = text
    .split(/[①-⑩\n]/)
    .map((c) => c.trim())
    .filter((c) => c.length > 0)

  return conditions.map((condition) => {
    const match = condition.match(/(.+?)(\+?\d+\.?\d*%)/)

    if (match) {
      return {
        text: match[1].trim(),
        rate: match[2].includes('+') ? match[2] : `+${match[2]}`,
      }
    }

    return {
      text: condition,
      rate: '',
    }
  })
}

// 백엔드 AI 분석 API 호출
const fetchAIAnalysis = async () => {
  aiLoading.value = true
  aiError.value = ''

  try {
    const productId = route.params.id

    // 백엔드 API 호출
    const res = await apiClient.post(`/products/${productId}/ai-analysis/`, {
      amount: targetAmount.value,
      months: targetMonths.value,
    })

    // 응답 데이터 설정
    const data = res.data
    aiSummary.value = data.summary || '이 상품은 고객님께 적합한 금융 상품입니다.'
    aiDetailedAnalysis.value =
      data.detailed_analysis || '상품 조건을 확인하시고 가입을 고려해보세요.'
    aiReasons.value = data.reasons || ['경쟁력 있는 금리', '안정적인 운영', '편리한 가입']
    aiWarning.value = data.warning || '약관을 꼼꼼히 확인하시기 바랍니다.'
  } catch (e) {
    console.error('AI 분석 조회 오류:', e)
    const status = e?.response?.status

    if (status === 404) {
      aiError.value = '상품을 찾을 수 없습니다.'
    } else if (status === 500) {
      aiError.value = 'AI 분석 서비스에 일시적인 문제가 발생했습니다.'
    } else {
      aiError.value = e?.response?.data?.detail || 'AI 분석을 불러오는데 실패했습니다.'
    }
  } finally {
    aiLoading.value = false
  }
}

const fetchProductDetail = async () => {
  loading.value = true
  error.value = ''

  try {
    const productId = route.params.id
    const res = await apiClient.get(`/products/${productId}/`)
    product.value = res.data

    await fetchAIAnalysis()
  } catch (e) {
    console.error('상품 조회 오류:', e)
    const status = e?.response?.status
    if (status === 404) {
      error.value = '존재하지 않는 상품입니다.'
    } else {
      error.value = '상품 정보를 불러오는 중 오류가 발생했습니다.'
    }
  } finally {
    loading.value = false
  }
}

const handleSubscribe = async () => {
  if (subscribing.value) return

  subscribing.value = true

  try {
    const productId = route.params.id
    await apiClient.post(`/products/${productId}/subscribe/`)

    alert('상품 가입이 완료되었습니다!\n마이페이지에서 확인하실 수 있습니다.')
    router.push('/mypage')
  } catch (e) {
    console.error('가입 오류:', e)
    const status = e?.response?.status

    if (status === 401) {
      alert('로그인이 필요합니다.')
      router.push('/login')
    } else if (status === 400) {
      alert(e?.response?.data?.detail || '이미 가입한 상품입니다.')
    } else {
      alert('가입 중 오류가 발생했습니다.')
    }
  } finally {
    subscribing.value = false
  }
}

onMounted(() => {
  fetchProductDetail()
})
</script>

<style scoped>
.product-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  background: #f8f9fa;
}

.loading {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #6393f2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-container {
  text-align: center;
  padding: 60px 20px;
}

.error {
  color: #ef4444;
  font-size: 16px;
  margin-bottom: 20px;
}

.back-btn {
  padding: 10px 20px;
  background: #f3f4f6;
  border: none;
  border-radius: 8px;
  color: #4a5568;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e5e7eb;
}

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 상품 헤더 카드 */
.product-header-card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.bank-logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #4a5568;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.bank-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
}

.bank-name {
  font-size: 16px;
  font-weight: 700;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.product-name {
  font-size: 24px;
  font-weight: 900;
  color: #111827;
  margin: 0 0 12px 0;
}

.tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.tag-primary {
  background: #6393f2;
  color: white;
}

.tag-secondary {
  background: #e0f2fe;
  color: #0284c7;
}

.rate-highlight {
  text-align: right;
}

.max-rate {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 4px;
}

.rate-number {
  font-size: 28px;
  font-weight: 900;
  color: #6393f2;
  display: block;
}

.base-rate-info {
  font-size: 12px;
  color: #9ca3af;
}

/* AI 한줄평 카드 */
.ai-summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  color: white;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.ai-icon {
  font-size: 32px;
}

.ai-title {
  font-size: 20px;
  font-weight: 800;
  color: white;
  margin: 0;
  flex: 1;
}

.ai-badge {
  background: rgba(255, 255, 255, 0.3);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
}

.ai-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
}

.ai-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.ai-loading p {
  margin: 0;
  opacity: 0.9;
}

.ai-error {
  text-align: center;
  padding: 20px;
}

.ai-error p {
  margin: 0 0 12px 0;
  opacity: 0.9;
}

.retry-btn {
  background: rgba(255, 255, 255, 0.3);
  border: none;
  padding: 8px 16px;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: rgba(255, 255, 255, 0.4);
}

.ai-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ai-summary {
  font-size: 16px;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
  font-weight: 500;
}

.ai-detail-btn {
  align-self: flex-end;
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-detail-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

/* 정보 카드 행 */
.info-cards-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 768px) {
  .info-cards-row {
    grid-template-columns: 1fr;
  }
}

/* 예상 수령액 카드 */
.expected-amount-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-title {
  font-size: 18px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 20px 0;
}

.amount-info {
  margin-bottom: 20px;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.amount-label {
  font-size: 14px;
  color: #6b7280;
}

.amount-value {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.maturity-badge {
  background: #6393f2;
  border-radius: 16px;
  padding: 16px;
  text-align: center;
  color: white;
}

.badge-label {
  display: block;
  font-size: 14px;
  margin-bottom: 4px;
}

.badge-value {
  display: block;
  font-size: 32px;
  font-weight: 900;
}

/* 우대조건 카드 */
.preferential-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.preferential-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preferential-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9fafb;
  border-radius: 12px;
}

.preferential-text {
  font-size: 14px;
  color: #4a5568;
  flex: 1;
}

.preferential-rate {
  font-size: 14px;
  font-weight: 700;
  color: #6393f2;
}

.no-preferential {
  text-align: center;
  color: #9ca3af;
  padding: 20px;
  margin: 0;
}

/* 금리 정보 테이블 */
.rate-table-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.rate-table thead {
  background: #f9fafb;
}

.rate-table th {
  padding: 16px;
  text-align: center;
  font-size: 14px;
  font-weight: 700;
  color: #6b7280;
  border-bottom: 2px solid #e5e7eb;
}

.rate-table td {
  padding: 16px;
  text-align: center;
  font-size: 14px;
  color: #4a5568;
  border-bottom: 1px solid #f3f4f6;
}

.rate-table tr:last-child td {
  border-bottom: none;
}

.highlight-rate {
  font-weight: 700;
  color: #6393f2;
  font-size: 16px;
}

.no-data {
  text-align: center;
  color: #9ca3af;
  padding: 40px;
  margin: 0;
}

/* 가입 버튼 */
.action-section {
  background: white;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.subscribe-btn {
  width: 100%;
  padding: 18px;
  background: #6393f2;
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
}

.subscribe-btn:hover {
  background: #4f7de0;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(99, 147, 242, 0.4);
}

.subscribe-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.login-required {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.login-link {
  color: #6393f2;
  font-weight: 700;
  text-decoration: none;
  margin-left: 8px;
}

.login-link:hover {
  text-decoration: underline;
}

/* AI 모달 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #9ca3af;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #f3f4f6;
  color: #4a5568;
}

.modal-body {
  padding: 24px;
}

.ai-analysis-section {
  margin-bottom: 24px;
}

.ai-analysis-section h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin: 0 0 12px 0;
}

.ai-analysis-section p {
  line-height: 1.8;
  color: #4a5568;
  margin: 0;
}

.ai-reasons {
  list-style: none;
  padding: 0;
  margin: 0;
}

.ai-reasons li {
  padding: 8px 0;
  color: #4a5568;
  position: relative;
  padding-left: 20px;
}

.ai-reasons li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #6393f2;
  font-weight: 700;
}

.ai-disclaimer {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
  padding: 12px;
  background: #f9fafb;
  border-radius: 8px;
}
</style>
