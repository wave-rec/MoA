<template>
  <div class="main-view">
    <!-- 메인 컨텐츠 영역 -->
    <div class="main-content">
      <!-- 왼쪽: 히어로 슬라이드 -->
      <section class="hero-section">
        <div class="slider-container">
          <transition name="slide-fade" mode="out-in">
            <div :key="currentSlide" class="slide" @click="goToRecommend">
              <img :src="slides[currentSlide].image" alt="메인 슬라이드" class="slide-image-full" />
            </div>
          </transition>

          <!-- 슬라이드 인디케이터 -->
          <div class="slider-dots">
            <button
              v-for="(slide, index) in slides"
              :key="index"
              class="dot"
              :class="{ active: currentSlide === index }"
              @click.stop="goToSlide(index)"
            ></button>
          </div>
        </div>

        <!-- 은행 찾기 배너 -->
        <div class="bank-finder-banner" @click="goToBanks">
          <img src="/assets/main/bank-finder.png" alt="은행 찾기" class="banner-image-full" />
        </div>
      </section>

      <!-- 오른쪽: 금은시세 + 게시판 -->
      <aside class="sidebar">
        <!-- 금은시세 카드 -->
        <div class="exchange-card" @click="goToExchange">
          <img src="/assets/main/squirrel.png" alt="금은시세" class="card-image-full" />
        </div>

        <!-- 게시판 카드 -->
        <div class="board-card">
          <div class="board-header">
            <h3>게시판</h3>
            <button class="more-btn" @click="goToPosts">더보기 +</button>
          </div>

          <div v-if="postsLoading" class="board-loading">
            <div class="spinner-small"></div>
            <p>게시글을 불러오는 중...</p>
          </div>

          <div v-else-if="posts.length > 0" class="board-list">
            <div v-for="post in posts" :key="post.id" class="board-item" @click="goToPost(post.id)">
              <span class="post-category" :class="`category-${post.category}`">
                {{ getCategoryLabel(post.category) }}
              </span>
              <p class="post-title">{{ truncate(post.title, 20) }}</p>
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
            </div>
          </div>

          <div v-else class="board-empty">
            <p>게시글이 없습니다.</p>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()

// 슬라이드 데이터
const slides = [
  {
    image: '/assets/main/slide-1.png',
  },
  {
    image: '/assets/main/slide-2.png',
  },
  {
    image: '/assets/main/slide-3.png',
  },
]

const currentSlide = ref(0)
let slideTimer = null

// 자동 슬라이드
const startAutoSlide = () => {
  slideTimer = setInterval(() => {
    currentSlide.value = (currentSlide.value + 1) % slides.length
  }, 5000)
}

const stopAutoSlide = () => {
  if (slideTimer) {
    clearInterval(slideTimer)
  }
}

const goToSlide = (index) => {
  currentSlide.value = index
  stopAutoSlide()
  startAutoSlide()
}

// 게시판 데이터
const posts = ref([])
const postsLoading = ref(false)

const fetchPosts = async () => {
  postsLoading.value = true
  try {
    const res = await apiClient.get('/api/v1/posts/')

    let fetchedPosts = []

    // 배열인 경우
    if (Array.isArray(res.data)) {
      fetchedPosts = res.data.slice(0, 10)
    }
    // results 안에 있는 경우
    else if (res.data && res.data.results && Array.isArray(res.data.results)) {
      fetchedPosts = res.data.results.slice(0, 10)
    }
    // 그 외
    else {
      console.warn('예상치 못한 응답 형태:', res.data)
      fetchedPosts = []
    }

    posts.value = fetchedPosts
  } catch (e) {
    console.error('게시글 조회 오류:', e)
    posts.value = []
  } finally {
    postsLoading.value = false
  }
}

// 카테고리 라벨
const getCategoryLabel = (category) => {
  const labels = {
    DEPOSIT: '예금',
    SAVINGS: '적금',
    ETC: '기타',
  }
  return labels[category] || '기타'
}

// 날짜 포맷
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}.${month}.${day}`
}

// 텍스트 자르기
const truncate = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

// 네비게이션
const goToRecommend = () => router.push({ name: 'recommend' })
const goToExchange = () => router.push({ name: 'commodity' })
const goToBanks = () => router.push({ name: 'banks' })
const goToPosts = () => router.push({ name: 'posts' })
const goToPost = (id) => router.push({ name: 'post-detail', params: { id } })

onMounted(() => {
  startAutoSlide()
  fetchPosts()
})

onUnmounted(() => {
  stopAutoSlide()
})
</script>

<style scoped>
.main-view {
  background: #fafafa;
  padding: 50px 0 40px;
}

.main-content {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 40px;
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 20px;
}

/* ========== 히어로 슬라이드 ========== */
.hero-section {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.slider-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  position: relative;
  height: 580px;
  overflow: hidden;
  cursor: pointer;
}

.slide {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide-image-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 24px;
  transform: scale(1.005);
}

/* 슬라이드 애니메이션 */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 슬라이드 인디케이터 */
.slider-dots {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #d1d5db;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  background: #6393f2;
  width: 32px;
  border-radius: 6px;
}

/* ========== 은행 찾기 배너 ========== */
.bank-finder-banner {
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(99, 147, 242, 0.2);
  overflow: hidden;
  height: 200px;
}

.bank-finder-banner:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(99, 147, 242, 0.3);
}

.banner-image-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* ========== 사이드바 ========== */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 18px;
  height: 100%;
}

/* 금은시세 카드 */
.exchange-card {
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 16px rgba(99, 147, 242, 0.3);
  min-height: 240px;
  overflow: hidden;
}

.exchange-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(99, 147, 242, 0.4);
}

.card-image-full {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transform: scale(1.005);
}

/* 게시판 카드 */
.board-card {
  background: white;
  border-radius: 18px;
  padding: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  height: 500px;
  flex: none;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.board-header h3 {
  font-size: 18px;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.more-btn {
  background: transparent;
  border: none;
  color: #6393f2;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.more-btn:hover {
  color: #4f7de0;
}

.board-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px;
  flex: 1;
  justify-content: center;
}

.spinner-small {
  width: 24px;
  height: 24px;
  border: 3px solid #e5e7eb;
  border-top-color: #6393f2;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.board-list {
  margin-top: 5px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  overflow: hidden;
  justify-content: flex-start;
}

.board-item {
  display: grid;
  grid-template-columns: 42px 1fr auto;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  height: 32px;
  border-radius: 6px;
  background: #f9fafb;
  flex: none;
}

.board-item:hover {
  background: #eff6ff;
  transform: translateX(4px);
}

.post-category {
  display: inline-block;
  padding: 3px 6px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  text-align: center;
  white-space: nowrap;
}

.category-DEPOSIT {
  background: #dbeafe;
  color: #1e40af;
}

.category-SAVINGS {
  background: #dbeafe;
  color: #1e40af;
}

.category-ETC {
  background: #dbeafe;
  color: #1e40af;
}

.post-title {
  font-size: 12.5px;
  font-weight: 600;
  color: #111827;
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.post-date {
  font-size: 11px;
  color: #9ca3af;
  white-space: nowrap;
}

.board-empty {
  text-align: center;
  padding: 40px;
  color: #9ca3af;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 반응형 */
@media (max-width: 1440px) {
  .main-view {
    padding: 20px 0 30px;
  }

  .main-content {
    max-width: 1200px;
    padding: 0 30px;
    gap: 20px;
  }

  .slider-container {
    height: 550px;
  }

  .slide {
    min-height: 550px;
  }

  .sidebar {
    gap: 18px;
  }

  .exchange-card {
    min-height: 240px;
  }

  .board-card {
    /* flex: 1로 자동 조정 */
  }
}

@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr 350px;
    gap: 20px;
    padding: 0 24px;
  }

  .slider-container {
    height: 450px;
  }

  .slide {
    min-height: 450px;
  }
}

@media (max-width: 960px) {
  .main-content {
    grid-template-columns: 1fr;
    padding: 0 16px;
  }

  .slider-container {
    height: 400px;
  }

  .slide {
    min-height: 400px;
  }

  .bank-finder-banner {
    padding: 30px;
  }

  .sidebar {
    grid-template-columns: 1fr;
  }
}
</style>
