<template>
  <div class="post-detail">

    <!-- 게시글 -->
    <section v-if="post" class="post-box">
      <span class="category">{{ post.category_display }}</span>

      <div class="post-header">
        <h2 class="title">{{ post.title }}</h2>

        <!-- 게시글 수정 / 삭제 -->
        <div v-if="isMyPost" class="post-actions">
          <button class="action-btn" @click="goEditPost">수정</button>
          <button class="action-btn danger" @click="deletePost">삭제</button>
        </div>
      </div>

      <div class="meta">
        <span class="author">{{ post.user_name }}</span>
        <span class="date">{{ formatDate(post.created_at) }}</span>
      </div>

      <!-- 글 내용 -->
      <p class="content">{{ post.content }}</p>

      <!-- 사진 출력 -->
      <div v-if="post.images && post.images.length">
        <img
          v-for="img in post.images"
          :key="img.id"
          :src="getImageUrl(img.image)"
          style="display:block; max-width:100%; margin-top:12px;"
        />
      </div>
    </section>

    <!-- 댓글 -->
    <section v-if="post" class="comment-section">

      <!-- 댓글 작성 -->
      <div class="comment-form">
        <textarea
          v-model="newComment"
          class="comment-textarea"
          placeholder="댓글을 입력하세요"
          @keydown.enter.exact.prevent="submitComment"
        ></textarea>

        <div class="comment-actions">
          <button class="primary-btn" @click="submitComment">댓글 작성</button>
        </div>
      </div>

      <h3 class="comment-title">댓글 {{ safeComments.length }}</h3>

      <ul class="comment-list">
        <li v-for="comment in safeComments" :key="comment.id">

          <!-- 댓글 헤더 -->
          <div class="comment-header">
            <div class="comment-info">
              <strong>{{ comment.user_name }}</strong>
              <span class="comment-date">
                {{ formatDate(comment.created_at) }}
              </span>
            </div>

            <!-- 댓글 수정 / 삭제 -->
            <div v-if="isMyComment(comment)" class="comment-actions">
              <button class="action-btn" @click="startEditComment(comment)">수정</button>
              <button class="action-btn danger" @click="deleteComment(comment.id)">삭제</button>
            </div>
          </div>

          <!-- 댓글 내용 -->
          <p v-if="editingId !== comment.id" class="comment-content">
            {{ comment.content }}
          </p>

          <!-- 댓글 수정 모드 -->
          <div v-else class="edit-box">
            <textarea v-model="editContent" class="edit-textarea"></textarea>

            <div class="comment-actions">
              <button class="action-btn" @click="confirmEditComment(comment.id)">완료</button>
              <button class="action-btn danger" @click="cancelEdit">취소</button>
            </div>
          </div>

        </li>
      </ul>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const postId = route.params.id

const post = ref(null)
const comments = ref([])
const newComment = ref('')

const editingId = ref(null)
const editContent = ref('')

const formatDate = (utcString) => {
  if (!utcString) return ''
  const date = new Date(utcString)
  return date.toLocaleString('ko-KR', {
    timeZone: 'Asia/Seoul',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const safeComments = computed(() =>
  Array.isArray(comments.value) ? comments.value : []
)

const isMyPost = computed(() =>
  authStore.isLogin && post.value?.user_id === authStore.user?.id
)

const isMyComment = (comment) =>
  authStore.isLogin && comment.user_name === authStore.user?.name

/* 이미지 URL */
const getImageUrl = (path) => {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${api.defaults.baseURL}${path}`
}

/* 게시글 */
const fetchPost = async () => {
  const res = await api.get(`/api/v1/posts/${postId}/`)
  post.value = res.data
}

const deletePost = async () => {
  if (!confirm('게시글을 삭제할까요?')) return
  await api.delete(`/api/v1/posts/${postId}/`)
  router.push('/posts')
}

const goEditPost = () => {
  router.push(`/posts/${postId}/edit`)
}

/* 댓글 */
const fetchComments = async () => {
  const res = await api.get(`/api/v1/posts/${postId}/comments/`)
  comments.value = res.data
}

const submitComment = async () => {
  if (!authStore.isLogin) {
    router.push({
      path: '/login',
      query: { redirect: route.fullPath },
    })
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

const deleteComment = async (id) => {
  if (!confirm('댓글을 삭제할까요?')) return
  await api.delete(`/api/v1/comments/${id}/`)
  comments.value = comments.value.filter(c => c.id !== id)
}

const startEditComment = (comment) => {
  editingId.value = comment.id
  editContent.value = comment.content
}

const cancelEdit = () => {
  editingId.value = null
  editContent.value = ''
}

const confirmEditComment = async (id) => {
  const res = await api.patch(`/api/v1/comments/${id}/`, {
    content: editContent.value,
  })
  const idx = comments.value.findIndex(c => c.id === id)
  comments.value[idx] = res.data
  cancelEdit()
}

onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>

<style scoped>
.post-detail {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
}

/* ================= 게시글 ================= */
.post-box {
  border-bottom: 2px solid #e6edff;
  padding-bottom: 40px;
}

.category {
  background: #dbeafe;
  color: #6393f2;
  padding: 4px 14px;
  border-radius: 999px;
  font-size: 13px;
  display: inline-block;
  margin-bottom: 12px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.post-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  background: none;
  border: none;
  color: #6393f2;
  font-size: 13px;
  cursor: pointer;
}

.action-btn.danger {
  color: #ef4444;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;  
  font-size: 13px;
  color: #777;
}

.content {
  line-height: 1.7;
  white-space: pre-wrap;
}

/* ================= 댓글 영역 ================= */
.comment-section {
  margin-top: 60px; /* 게시글이랑 충분히 띄움 */
}

.comment-title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}

/* 댓글 작성 */
.comment-form {
  margin-bottom: 50px; /* 댓글 목록과 간격 */
}

.comment-info {
  display: flex;
  align-items: center;
  gap: 8px;  
}

.comment-textarea {
  width: 100%;
  height: 130px;
  border: 1px solid #d6e0ff;
  border-radius: 12px;
  padding: 16px;
  font-size: 14px;
  box-sizing: border-box;
  resize: vertical;
  margin-top: 10px; 
}

.comment-textarea:focus {
  outline: none;
  border-color: #6393f2;
}

.comment-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 14px; 
}

.primary-btn {
  background: #6393f2;
  color: white;
  border: none;
  border-radius: 18px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 13px;
}

/* ================= 댓글 목록 ================= */
.comment-list li {
  border-bottom: 1px solid #eef2ff;
  padding: 24px 0;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 댓글 작성자 + 날짜 (게시글 meta와 통일) */
.comment-meta {
  font-size: 13px;
  color: #777;
}

.comment-meta strong {
  font-weight: 600;
  color: #111;
  margin-right: 6px;
}

.comment-actions {
  display: flex;
  gap: 12px;
}

.comment-actions .action-btn {
  font-size: 12px;
}

/* 댓글 내용 */
.comment-content {
  margin-top: 10px;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* ================= 댓글 수정 ================= */
.edit-box {
  margin-top: 12px; /* 글자랑 textarea 분리 */
}

.edit-textarea {
  width: 100%;
  height: 110px;
  border: 1px solid #d6e0ff;
  border-radius: 12px;
  padding: 14px;
  font-size: 14px;
  box-sizing: border-box;
  resize: vertical;
  margin-top: 8px;
}

.edit-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

</style>
