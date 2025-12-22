<template>
  <div class="post-create">

    <!-- 상단 여백 -->
    <div class="top-space"></div>

    <h2 class="title">게시글 수정</h2>

    <div class="form">

      <!-- 카테고리 -->
      <div class="form-row">
        <label>카테고리</label>
        <select v-model="selectedCategory">
          <option>예금</option>
          <option>적금</option>
          <option>기타</option>
        </select>
      </div>

      <!-- 제목 -->
      <div class="form-row">
        <label>글 제목</label>
        <input
          type="text"
          v-model="title"
          placeholder="제목을 입력하세요."
        />
      </div>

      <!-- 내용 -->
      <div class="form-row">
        <label>글 내용</label>
        <textarea
          v-model="content"
          placeholder="내용을 입력하세요."
        ></textarea>
      </div>

      <!-- 버튼 -->
      <button class="submit-btn" @click="submitEdit">
        수정 완료
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const postId = route.params.id

const selectedCategory = ref('예금')
const title = ref('')
const content = ref('')

const categoryMap = {
  예금: 'DEPOSIT',
  적금: 'SAVINGS',
  기타: 'ETC',
}

const reverseCategoryMap = {
  DEPOSIT: '예금',
  SAVINGS: '적금',
  ETC: '기타',
}

/* 기존 게시글 불러오기 */
const fetchPost = async () => {
  const res = await api.get(`/api/v1/posts/${postId}/`)
  title.value = res.data.title
  content.value = res.data.content
  selectedCategory.value = reverseCategoryMap[res.data.category]
}

/* 수정 요청 */
const submitEdit = async () => {
  if (!authStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  try {
    await api.patch(`/api/v1/posts/${postId}/`, {
      title: title.value,
      content: content.value,
      category: categoryMap[selectedCategory.value],
    })

    alert('게시글이 수정되었습니다.')
    router.push(`/posts/${postId}`)
  } catch (e) {
    console.error('게시글 수정 실패', e)
    alert('수정 권한이 없습니다.')
  }
}

onMounted(() => {
  fetchPost()
})
</script>

<style scoped>
.post-create {
  max-width: 900px;
  margin: 0 auto;
  padding-bottom: 30px;
}

.top-space {
  height: 40px;
}

.title {
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 40px;
}

.form {
  width: 100%;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.form-row label {
  width: 100px;
  font-weight: 600;
  color: #6393F2;
}

.form-row input,
.form-row select,
.form-row textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #d6e0ff;
  border-radius: 6px;
}

.form-row textarea {
  height: 200px;
  resize: none;
}

.submit-btn {
  margin-top: 20px;
  margin-left: auto;
  display: block;
  background: #2f3a5f;
  color: white;
  border: none;
  border-radius: 18px;
  padding: 10px 22px;
  cursor: pointer;
}

/* select 화살표 커스텀 */
select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23333' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 48px;
}
</style>
