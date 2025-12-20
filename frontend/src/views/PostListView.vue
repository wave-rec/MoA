<template>
  <div class="board-wrapper">
    <h2 class="board-title">게시판</h2>

    <!-- 상단 바 -->
    <div class="board-top">
      <div class="category-tabs">
        <span
          v-for="c in categories"
          :key="c.value"
          :class="['tab', { active: currentCategory === c.value }]"
          @click="selectCategory(c.value)"
        >
          {{ c.label }}
        </span>
      </div>

      <div class="right-box">
        <input class="search-input" placeholder="검색" />
        <button class="search-btn">검색</button>
        <button class="write-btn" @click="goCreate">글쓰기</button>
      </div>
    </div>

    <!-- 리스트 -->
    <div class="post-list">
      <div
        class="post-row"
        v-for="(post, index) in posts"
        :key="post.id"
        @click="goDetail(post.id)"
      >
        <span class="post-index">{{ index + 1 }}</span>
        <span class="post-category">{{ post.category }}</span>
        <span class="post-title">{{ post.title }}</span>
        <span class="post-date">{{ post.created_at?.slice(0, 10) }}</span>
      </div>
    </div>

    <!-- 페이지네이션 (UI용) -->
    <div class="pagination">
      <span>&lt;</span>
      <span class="active">1</span>
      <span>2</span>
      <span>3</span>
      <span>&gt;</span>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'

const router = useRouter()
const store = usePostStore()

const posts = computed(() => store.posts)
const currentCategory = ref(null)

const categories = [
  { label: '전체', value: null },
  { label: '예금', value: 'DEPOSIT' },
  { label: '적금', value: 'SAVINGS' },
  { label: '기타', value: 'ETC' },
]

const selectCategory = (category) => {
  currentCategory.value = category
  store.fetchPosts(category)
}

const goDetail = (id) => {
  router.push(`/posts/${id}`)
}

const goCreate = () => {
  router.push('/posts/create')
}

onMounted(() => {
  store.fetchPosts()
})
</script>

<style scoped>
/* 전체 */
.board-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 80px 20px;
}

/* 제목 */
.board-title {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 40px;
}

/* 상단 */
.board-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 3px solid #2f3a5f;
  padding-bottom: 12px;
  margin-bottom: 20px;
}

/* 카테고리 */
.category-tabs {
  display: flex;
  gap: 28px;
}

.tab {
  font-size: 15px;
  color: #9ca3af;
  cursor: pointer;
  padding-bottom: 6px;
}

.tab.active {
  color: #6393f2;
  font-weight: 600;
  border-bottom: 2px solid #6393f2;
}

/* 우측 */
.right-box {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input {
  width: 220px;
  height: 30px;
  border: none;
  background: #e5e7eb;
  padding: 0 10px;
  font-size: 13px;
}

.search-btn {
  background: #6393f2;
  border: none;
  color: white;
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 4px;
}

.write-btn {
  background: #2f3a5f;
  border: none;
  color: white;
  padding: 5px 14px;
  font-size: 12px;
  border-radius: 14px;
}

/* 리스트 */
.post-list {
  border-top: 1px solid #dbeafe;
}

.post-row {
  display: grid;
  grid-template-columns: 40px 80px 1fr 120px;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #dbeafe;
  cursor: pointer;
}

.post-row:hover {
  background: #f8fbff;
}

/* 번호 */
.post-index {
  text-align: center;
  font-size: 13px;
}

/* 카테고리 pill */
.post-category {
  background: #dbeafe;
  color: #2f3a5f;
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  width: fit-content;
}

/* 제목 */
.post-title {
  font-size: 14px;
}

/* 날짜 */
.post-date {
  font-size: 12px;
  color: #6b7280;
  text-align: right;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 40px;
  font-size: 14px;
  color: #6393f2;
}

.pagination span {
  cursor: pointer;
}

.pagination .active {
  font-weight: 700;
}
</style>
