<template>
  <div class="post-detail">

    <!-- 상단 여백 -->
    <div class="top-space"></div>

    <!-- 게시글 로딩 -->
    <div v-if="!post" class="loading">
      게시글 불러오는 중...
    </div>

    <!-- 게시글 -->
    <section v-else class="post-box">
      <span class="category">{{ post.category }}</span>

      <h2 class="title">{{ post.title }}</h2>
            <button
        v-if="isMyPost"
        class="delete-btn"
        @click="deletePost"
        >
        삭제
        </button>


      <div class="meta">
        <span class="author">{{ post.user_name }}</span>
        <span class="date">{{ post.created_at?.slice(0, 10) }}</span>
      </div>

      <p class="content">{{ post.content }}</p>
    </section>

    <!-- 댓글 -->
    <section v-if="post" class="comment-section">

        <!-- 댓글 작성 -->
      <div class="comment-form">
        <textarea
          v-model="newComment"
          placeholder="댓글을 입력하세요"
        ></textarea>
        <button @click="submitComment">댓글 작성</button>
      </div>
      <h3>댓글 {{ safeComments.length }}</h3>

      <p v-if="safeComments.length === 0" class="no-comment">
        아직 댓글이 없습니다.
      </p>

      <ul>
        <li
          v-for="comment in safeComments"
          :key="comment.id"
        >
          <div class="comment-header">
            <strong>{{ comment.user_name }}</strong>
            <span>
              {{ comment.created_at?.slice(0,16).replace('T',' ') }}
            </span>
          </div>
          <p>{{ comment.content }}</p>
        </li>
      </ul>

    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const route = useRoute()
const authStore = useAuthStore()
const router = useRouter()
const postId = route.params.id

const post = ref(null)
const comments = ref([])
const newComment = ref('')

/* 댓글을 무조건 배열로 보정 */
const safeComments = computed(() => {
  return Array.isArray(comments.value) ? comments.value : []
})

/* 게시글 조회 */
const fetchPost = async () => {
  const res = await api.get(`/api/v1/posts/${postId}/`)
  post.value = res.data
}

/* 댓글 조회 */
const fetchComments = async () => {
  const res = await api.get(`/api/v1/posts/${postId}/comments/`)

  comments.value = Array.isArray(res.data)
    ? res.data
    : res.data.results || []
}

/* 댓글 작성 */
const submitComment = async () => {
  if (!authStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  if (!newComment.value.trim()) return

  const res = await api.post(
    `/api/v1/posts/${postId}/comments/`,
    { content: newComment.value }
  )

  comments.value.unshift(res.data)
  newComment.value = ''
}

const isMyPost = computed(() => {
  return (
    authStore.isLogin &&
    authStore.user &&
    post.value &&
    post.value.user_id === authStore.user.id
  )
})


const deletePost = async () => {
  if (!confirm('정말 삭제하시겠습니까?')) return

  try {
    await api.delete(`/api/v1/posts/${postId}/`)
    alert('삭제되었습니다.')
    router.push('/posts')
  } catch (e) {
    alert('삭제 권한이 없습니다.')
  }
}

onMounted(() => {
  fetchPost()
  fetchComments()
  
})
</script>

<style scoped>
.top-space {
  height: 30px;
}

.post-detail {
  max-width: 900px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.category {
  display: inline-block;
  background: #cfe0ff;
  color: #6393F2;
  padding: 4px 14px;
  border-radius: 16px;
  font-size: 13px;
}

.title {
  margin-top: 12px;
  font-size: 22px;
  font-weight: 700;
}

.meta {
  margin: 8px 0 20px;
  font-size: 13px;
  color: #777;
}

.content {
  line-height: 1.7;
  margin-bottom: 40px;
}

.comment-section {
  border-top: 2px solid #e6edff;
  padding-top: 30px;
}

.no-comment {
  color: #999;
  margin-bottom: 20px;
}

.comment-section ul {
  list-style: none;
  padding: 0;
}

.comment-section li {
  padding: 16px 0;
  border-bottom: 1px solid #eef2ff;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #555;
}

.comment-form {
  margin-top: 30px;
}

.comment-form textarea {
  width: 100%;
  height: 90px;
  border: 1px solid #d6e0ff;
  border-radius: 8px;
  padding: 12px;
}

.comment-form button {
  margin-top: 10px;
  margin-left: auto;
  display: block;
  background: #6393F2;
  color: white;
  border: none;
  border-radius: 18px;
  padding: 8px 20px;
  cursor: pointer;
}
.delete-btn {
  margin-left: auto;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 6px 14px;
  cursor: pointer;
}

</style>
