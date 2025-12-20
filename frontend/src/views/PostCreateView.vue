<template>
  <div class="post-create">

    <!-- 상단 여백 -->
    <div class="top-space"></div>

    <h2 class="title">게시판 글 작성</h2>

    <div class="form">

      <!-- 카테고리 -->
      <div class="form-row">
        <label>카테고리</label>
        <select v-model="selectedCategory">
          <option>전체</option>
          <option>예금</option>
          <option>적금</option>
        </select>
      </div>

      <!-- 제목 -->
      <div class="form-row">
        <label>글 제목</label>
        <input
          type="text"
          v-model="title"
          placeholder="내용을 입력하세요."
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
      <button class="submit-btn" @click="submitPost">
        글쓰기
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()



/* 입력값 */
const selectedCategory = ref('전체')
const title = ref('')
const content = ref('')

/* 🔥 한글 → 백엔드 enum 매핑 */
const categoryMap = {
  전체: 'DEPOSIT',
  예금: 'DEPOSIT',
  적금: 'SAVINGS',
}

/* 글 작성 */
const submitPost = async () => {
  if (!authStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  // 🔽 기존 글 작성 로직 그대로
  try {
    await api.post('/api/v1/posts/', {
    title: title.value,
    content: content.value,
    category: categoryMap[selectedCategory.value],
    })

    router.push({ name: 'posts' })
  } catch (e) {
    console.error('글 작성 실패', e)
  }
}
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
select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;

  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%23333' stroke-width='2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;

  /* 🔥 여기 숫자만 조절하면 됨 */
  background-position: right 10px center;

  padding-right: 48px;
}
</style>
