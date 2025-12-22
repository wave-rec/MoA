<template>
  <div class="liked-page">
    <h2 class="title">가입한 상품</h2>

    <!-- 가입한 상품 없음 -->
    <div v-if="products.length === 0" class="empty">
      가입한 상품이 없습니다.
    </div>

    <!-- 가입한 상품 카드 -->
    <div
      v-for="product in products"
      :key="product.id"
      class="product-card"
      @click="goDetail(product.id)"
    >
      <!-- 왼쪽 : 은행 로고 + 이름 -->
      <div class="left">
        <img
          :src="getBankLogo(product.bank_name)"
          class="bank-logo"
          alt="bank logo"
        />
        <div class="info">
          <h3 class="bank-name">{{ product.bank_name }}</h3>
          <p class="product-name">{{ product.name }}</p>
        </div>
      </div>

      <!-- 오른쪽 : 금리 + 취소 -->
      <div class="right">
        <div class="rate-box">
          <div class="max-rate">최고 {{ product.max_rate }}%</div>
          <div class="base-rate">기본 {{ product.base_rate }}%</div>
        </div>

        <button
          class="cancel-btn"
          @click.stop="cancelSubscription(product.id)"
        >
          가입 취소
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

/* =========================
   상태
========================= */
const products = ref([])
const router = useRouter()

/* =========================
   가입 상품 조회
========================= */
const fetchSubscribedProducts = async () => {
  try {
    const res = await api.get('/products/subscriptions/')
    products.value = res.data
  } catch (err) {
    console.error('가입 상품 조회 실패', err)
  }
}

/* =========================
   상세 페이지 이동
========================= */
const goDetail = (productId) => {
  router.push(`/products/${productId}`)
}

/* =========================
   가입 취소
========================= */
const cancelSubscription = async (productId) => {
  if (!confirm('정말 이 상품 가입을 취소하시겠습니까?')) return

  try {
    await api.delete(`/products/${productId}/subscribe/`)
    products.value = products.value.filter(p => p.id !== productId)
    alert('가입이 취소되었습니다.')
  } catch (err) {
    console.error('가입 취소 실패', err)
    alert('가입 취소 중 오류가 발생했습니다.')
  }
}

/* =========================
   은행 로고 매핑
========================= */
const logoMap = {
  국민: 'kb.png',
  신한: 'shinhan.png',
  우리: 'woori.png',
  하나: 'hana.png',
  카카오: 'kakao.png',
  토스: 'toss.png',
  케이: 'k.png',

  한국스탠다드차타드: 'sc.png',
  제일: 'sc.png',

  중소기업: 'ibk.png',
  기업: 'ibk.png',
  한국산업: 'kdb.png',
  산업: 'kdb.png',

  수협: 'sh.png',
  농협: 'nh.png',

  경남: 'busan.png',
  부산: 'busan.png',
  광주: 'kjb.png',
  전북: 'jb.png',
  제주: 'jj.png',
  아이엠: 'iam.png',
  대구: 'daegu.png',
}

const getBankLogo = (bankName) => {
  if (!bankName) return '/assets/banks/default.png'

  // "주식회사", 공백 제거
  const normalized = bankName
    .replace('주식회사', '')
    .replace(/\s/g, '')

  for (const key in logoMap) {
    if (normalized.includes(key)) {
      return `/assets/banks/${logoMap[key]}`
    }
  }

  return '/assets/banks/default.png'
}

/* =========================
   마운트 시 호출
========================= */
onMounted(fetchSubscribedProducts)
</script>

<style scoped>
.liked-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.title {
  font-size: 26px;
  font-weight: bold;
  margin-bottom: 30px;
}

.empty {
  color: #888;
  font-size: 16px;
  margin-top: 20px;
}

/* 카드 */
.product-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 22px 26px;
  border-radius: 18px;
  border: 2px solid #6c8cff;
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #fff;
}

.product-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

/* 왼쪽 */
.left {
  display: flex;
  align-items: center;
  gap: 18px;
}

.bank-logo {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.bank-name {
  font-size: 18px;
  font-weight: bold;
}

.product-name {
  font-size: 14px;
  color: #555;
}

/* 오른쪽 */
.right {
  text-align: right;
}

.rate-box {
  margin-bottom: 10px;
}

.max-rate {
  font-size: 18px;
  font-weight: bold;
  color: #4a5cff;
}

.base-rate {
  font-size: 14px;
  color: #888;
}

/* 취소 버튼 */
.cancel-btn {
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid #ff6b6b;
  background: #fff;
  color: #ff6b6b;
  font-size: 13px;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #ff6b6b;
  color: #fff;
}
</style>
