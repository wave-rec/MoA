<template>
  <div class="my-posts">
    <h2>내가 쓴 게시글</h2>

    <!-- 게시글 없을 때 -->
    <p v-if="posts.length === 0" class="empty">
      아직 작성한 게시글이 없습니다.
    </p>

    <!-- 게시글 목록 -->
    <ul v-else class="post-list">
      <li
        v-for="post in posts"
        :key="post.id"
        class="post-item"
        @click="goDetail(post.id)"
      >
        <h4>{{ post.title }}</h4>
        <span>{{ formatDate(post.created_at) }}</span>
      </li>
    </ul>

    <!-- 마이페이지로 돌아가기 -->
    <button class="back-btn" @click="goMyPage">
      마이페이지로 돌아가기
    </button>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePostStore } from '@/stores/posts'

/* store & router */
const postStore = usePostStore()
const router = useRouter()

/* 마운트 시 내가 쓴 게시글 조회 */
onMounted(() => {
  postStore.fetchMyPosts()
})

/* 내가 쓴 게시글 */
const posts = computed(() => postStore.myPosts)

/* 게시글 상세 이동 */
const goDetail = (id) => {
  router.push(`/posts/${id}`)
}

/* 마이페이지 이동 */
const goMyPage = () => {
  router.push({ name: 'mypage' })
}

/* 날짜 포맷 */
const formatDate = (date) => {
  return date?.slice(0, 10)
}
</script>

<style scoped>
.my-posts {
  max-width: 800px;
  margin: 60px auto;
  padding: 0 20px;
}

.my-posts h2 {
  font-size: 22px;
  margin-bottom: 30px;
}

/* 리스트 */
.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.post-item {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  cursor: pointer;
  transition: background 0.2s;
}

.post-item:hover {
  background: #f9fafb;
}

.post-item h4 {
  font-size: 16px;
  margin-bottom: 6px;
}

.post-item span {
  font-size: 13px;
  color: #9ca3af;
}

/* 빈 상태 */
.empty {
  color: #6b7280;
  margin: 40px 0;
}

/* 뒤로 가기 */
.back-btn {
  margin-top: 40px;
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: white;
  cursor: pointer;
}

.back-btn:hover {
  background: #f3f4f6;
}
</style>
