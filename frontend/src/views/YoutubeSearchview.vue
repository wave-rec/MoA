<template>
  <div class="youtube-search-view">
    <div class="layout-inner">
      <!-- 검색 결과가 없을 때 → 카드 그리드 표시 -->
      <div v-if="!searchQuery" class="term-selection">
        <h2 class="selection-title">
          <span class="icon">💡</span>
          궁금한 금융 용어를 선택해보세요
        </h2>
        <p class="selection-subtitle">
          초보자도 쉽게 이해할 수 있는 금융 지식을 영상으로 배워보세요
        </p>

        <!-- 카테고리별 탭 -->
        <div class="category-tabs">
          <button
            v-for="cat in categories"
            :key="cat"
            :class="['category-tab', { active: selectedCategory === cat }]"
            @click="selectedCategory = cat"
          >
            {{ CATEGORY_COLORS[cat].icon }} {{ cat }}
          </button>
        </div>

        <!-- 용어 카드 그리드 -->
        <div class="term-grid">
          <div
            v-for="term in filteredTerms"
            :key="term.title"
            class="term-card"
            @click="selectTerm(term.query)"
            :style="{
              borderColor: CATEGORY_COLORS[term.category].text,
            }"
          >
            <div class="term-emoji">{{ term.emoji }}</div>
            <h3 class="term-title">{{ term.title }}</h3>
            <p class="term-description">{{ term.description }}</p>
            <div
              class="term-badge"
              :style="{
                background: CATEGORY_COLORS[term.category].bg,
                color: CATEGORY_COLORS[term.category].text,
              }"
            >
              {{ term.category }}
            </div>
          </div>
        </div>
      </div>

      <!-- 검색 결과 화면 (기존 코드) -->
      <div v-else>
        <h2 class="search-title">
          <span class="keyword">"{{ searchQuery }}"</span> 검색 결과
        </h2>

        <div v-if="loading && videos.length === 0" class="loading-container">
          <div class="spinner"></div>
          <p>영상을 불러오는 중입니다...</p>
        </div>

        <div v-else class="video-grid">
          <div
            v-for="video in videos"
            :key="video.id.videoId"
            class="video-card"
            @click="openVideoModal(video.id.videoId)"
          >
            <div class="thumbnail-wrapper">
              <img
                :src="video.snippet.thumbnails.high.url"
                :alt="video.snippet.title"
                class="thumbnail"
              />
              <div class="play-overlay">
                <span class="play-icon">▶</span>
              </div>
            </div>
            <div class="video-info">
              <h3 class="video-title" v-html="video.snippet.title"></h3>
              <p class="channel-name">{{ video.snippet.channelTitle }}</p>
              <p class="publish-date">{{ formatDate(video.snippet.publishedAt) }}</p>
            </div>
          </div>

          <p v-if="videos.length === 0 && !loading" class="no-result">검색 결과가 없습니다.</p>
        </div>

        <div v-if="loading && videos.length > 0" class="more-loading">
          <div class="spinner-small"></div>
          <p>영상을 더 불러오는 중...</p>
        </div>

        <p v-if="isEnd && videos.length > 0" class="no-more">마지막 영상입니다.</p>
      </div>
    </div>

    <!-- 영상 재생 모달 -->
    <Transition name="fade">
      <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <button class="close-btn" @click="closeModal">&times;</button>
          <div class="video-container">
            <iframe
              v-if="selectedVideoId"
              :src="`https://www.youtube.com/embed/${selectedVideoId}?autoplay=1`"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { FINANCIAL_TERMS, CATEGORY_COLORS } from '@/constants/financialTerms'

const route = useRoute()
const router = useRouter()
const searchQuery = ref(route.query.q || '')
const videos = ref([])
const loading = ref(false)
const nextPageToken = ref('')
const isEnd = ref(false)

// 모달 관련 상태
const isModalOpen = ref(false)
const selectedVideoId = ref('')

// 카테고리 필터링
const selectedCategory = ref('기본개념')
const categories = Object.keys(CATEGORY_COLORS)

const filteredTerms = computed(() => {
  return FINANCIAL_TERMS.filter((term) => term.category === selectedCategory.value)
})

// 용어 선택 → 유튜브 검색
const selectTerm = (query) => {
  router.push({ name: 'YoutubeSearch', query: { q: query } })
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`
}

// 모달 열기/닫기 로직
const openVideoModal = (videoId) => {
  selectedVideoId.value = videoId
  isModalOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  isModalOpen.value = false
  selectedVideoId.value = ''
  document.body.style.overflow = 'auto'
}

// 유튜브 API 호출 함수
const fetchVideos = async (isMore = false) => {
  const query = route.query.q
  if (!query || loading.value || (isMore && isEnd.value)) return

  loading.value = true
  searchQuery.value = query

  try {
    const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
    const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        key: API_KEY,
        part: 'snippet',
        q: query,
        type: 'video',
        maxResults: 12,
        pageToken: isMore ? nextPageToken.value : '',
      },
    })

    if (isMore) {
      videos.value.push(...response.data.items)
    } else {
      videos.value = response.data.items
    }

    nextPageToken.value = response.data.nextPageToken || ''
    isEnd.value = !nextPageToken.value
  } catch (error) {
    console.error('유튜브 API 호출 에러:', error)
  } finally {
    loading.value = false
  }
}

// 무한 스크롤 핸들러
const handleScroll = () => {
  const scrollHeight = document.documentElement.scrollHeight
  const scrollTop = document.documentElement.scrollTop
  const clientHeight = document.documentElement.clientHeight

  if (scrollTop + clientHeight >= scrollHeight - 100) {
    if (!loading.value && nextPageToken.value) {
      fetchVideos(true)
    }
  }
}

onMounted(() => {
  if (route.query.q) {
    fetchVideos()
  }
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(
  () => route.query.q,
  (newQuery) => {
    searchQuery.value = newQuery || ''
    if (newQuery) {
      videos.value = []
      nextPageToken.value = ''
      isEnd.value = false
      fetchVideos()
    }
  },
)
</script>

<style scoped>
.youtube-search-view {
  padding: 40px 0;
  min-height: 100vh;
}

/* 용어 선택 화면 */
.term-selection {
  max-width: 1200px;
  margin: 0 auto;
}

.selection-title {
  font-size: 32px;
  font-weight: 900;
  color: #111827;
  text-align: center;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.selection-title .icon {
  font-size: 36px;
}

.selection-subtitle {
  text-align: center;
  color: #6b7280;
  font-size: 16px;
  margin-bottom: 40px;
}

/* 카테고리 탭 */
.category-tabs {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.category-tab {
  padding: 12px 24px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s;
}

.category-tab:hover {
  border-color: #6393f2;
  color: #6393f2;
  transform: translateY(-2px);
}

.category-tab.active {
  background: #6393f2;
  border-color: #6393f2;
  color: white;
}

/* 용어 카드 그리드 */
.term-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.term-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 16px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.term-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.term-emoji {
  font-size: 40px;
  margin-bottom: 12px;
}

.term-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.term-description {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 16px;
}

.term-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

/* 검색 결과 화면 */
.search-title {
  font-size: 24px;
  margin-bottom: 30px;
  color: #111827;
}

.keyword {
  color: #6393f2;
  font-weight: 700;
}

.loading-container,
.more-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 0;
  color: #6b7280;
}

.spinner,
.spinner-small {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #6393f2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner {
  width: 40px;
  height: 40px;
  margin-bottom: 16px;
}
.spinner-small {
  width: 24px;
  height: 24px;
  border-width: 3px;
  margin-bottom: 8px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 32px 24px;
}

.video-card {
  cursor: pointer;
}

.thumbnail-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 12px;
  background-color: #f3f4f6;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.video-card:hover .play-overlay {
  opacity: 1;
}
.video-card:hover .thumbnail {
  transform: scale(1.05);
}

.play-icon {
  color: white;
  font-size: 40px;
}

.video-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
  color: #111827;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel-name {
  font-size: 14px;
  color: #4b5563;
}
.publish-date {
  font-size: 13px;
  color: #9ca3af;
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.modal-content {
  position: relative;
  width: 90%;
  max-width: 900px;
  background: #000;
  border-radius: 16px;
  overflow: visible;
}

.video-container {
  width: 100%;
  aspect-ratio: 16 / 9;
}

.video-container iframe {
  width: 100%;
  height: 100%;
  border-radius: 16px;
}

.close-btn {
  position: absolute;
  top: -45px;
  right: -10px;
  background: none;
  border: none;
  color: white;
  font-size: 40px;
  cursor: pointer;
}

/* 애니메이션 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.no-more,
.no-result {
  text-align: center;
  padding: 40px 0;
  color: #9ca3af;
}

/* 반응형 */
@media (max-width: 768px) {
  .selection-title {
    font-size: 24px;
  }

  .category-tabs {
    gap: 8px;
  }

  .category-tab {
    padding: 8px 16px;
    font-size: 13px;
  }

  .term-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
