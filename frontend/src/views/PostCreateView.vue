<template>
  <div class="post-create">
    <div class="top-space"></div>

    <h2 class="title">게시글 작성</h2>

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

      <!-- 작성 가이드 -->
      <div class="form-row align-top">
        <label>작성 가이드</label>

        <div class="guide-box">
          <p class="guide-title">
            아래 버튼을 누르면 글 구조가 자동으로 들어가요
          </p>

          <!-- ✅ 가이드 미리보기 -->
          <ul class="guide-preview">
            <li v-for="guide in guides" :key="guide">
              • {{ guide }}
            </li>
          </ul>

          <!-- 버튼 -->
          <div class="guide-actions">
            <button
              type="button"
              class="guide-btn"
              @click="insertAllGuides"
            >
              가이드 전체 입력
            </button>
          </div>
        </div>
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
      <div class="form-row align-top">
        <label>글 내용</label>
        <textarea
          ref="contentTextarea"
          v-model="content"
          placeholder="선택한 항목을 중심으로 자유롭게 작성해주세요."
        ></textarea>
      </div>

      <!-- 사진 -->
      <div class="form-row align-top">
        <label>사진</label>

        <div class="image-upload-box">
          <input
            type="file"
            accept="image/*"
            multiple
            @change="onImageChange"
          />

          <div v-if="previewImages.length" class="preview-list">
            <div
              v-for="(img, idx) in previewImages"
              :key="idx"
              class="preview-item"
            >
              <img :src="img" class="preview-img" />
              <button
                class="remove-btn"
                @click.prevent="removeImage(idx)"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 등록 버튼 -->
      <button class="submit-btn" @click="submitPost">
        글 올리기
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

/* 상태 */
const selectedCategory = ref('예금')
const title = ref('')
const content = ref('')
const contentTextarea = ref(null)

/* 이미지 */
const images = ref([])
const previewImages = ref([])

/* 카테고리 매핑 */
const categoryMap = {
  예금: 'DEPOSIT',
  적금: 'SAVINGS',
  기타: 'ETC',
}

/* 가이드 */
const guideMap = {
  예금: [
    '왜 이 예금을 선택했나요?',
    '실제 금리는 만족스러웠나요?',
    '가입 과정은 어땠나요?',
    '아쉬운 점이나 주의할 점',
    '이런 분께 추천해요',
  ],
  적금: [
    '적금 가입 목적은 무엇이었나요?',
    '월 납입 부담은 어땠나요?',
    '이자 체감은 어땠나요?',
    '중도해지 시 불편한 점',
    '이런 분께 추천해요',
  ],
  기타: [
    '공유하고 싶은 금융 이야기',
    '궁금한 점이나 고민',
  ],
}

const guides = computed(() => guideMap[selectedCategory.value] || [])

/* ✅ 가이드 전체 입력 */
const insertAllGuides = () => {
  const guideText = guides.value
    .map(g => `- ${g}`)
    .join('\n\n')

  content.value = content.value
    ? `${guideText}\n\n${content.value}`
    : guideText

  requestAnimationFrame(() => {
    contentTextarea.value?.focus()
  })
}

/* 이미지 */
const onImageChange = (e) => {
  const files = Array.from(e.target.files)
  images.value = files
  previewImages.value = files.map(file =>
    URL.createObjectURL(file)
  )
}

const removeImage = (idx) => {
  images.value.splice(idx, 1)
  previewImages.value.splice(idx, 1)
}

/* 글 작성 */
const submitPost = async () => {
  if (!authStore.isLogin) {
    alert('로그인이 필요합니다.')
    router.push({ name: 'login' })
    return
  }

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  formData.append('category', categoryMap[selectedCategory.value])

  images.value.forEach(img => {
    formData.append('images', img)
  })

  const res = await api.post('/api/v1/posts/', formData)
  router.push(`/posts/${res.data.id}`)
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

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.form-row.align-top {
  align-items: flex-start;
}

.form-row label {
  width: 120px;
  font-weight: 600;
  color: #6393f2;
  padding-top: 10px;
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

/* 가이드 */
.guide-box {
  flex: 1;
  background: #f7f9ff;
  border: 1px dashed #c7d3ff;
  border-radius: 10px;
  padding: 16px;
}

.guide-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
}

/* 가이드 미리보기 */
.guide-preview {
  margin: 10px 0 16px;
  padding-left: 0;
  list-style: none;
  font-size: 14px;
  color: #4b5563;
}

.guide-preview li {
  margin-bottom: 6px;
}

.guide-actions {
  display: flex;
  justify-content: flex-start;
}

.guide-btn {
  background: #eef2ff;
  border: 1px solid #c7d3ff;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
}

/* 이미지 */
.preview-list {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.preview-item {
  position: relative;
}

.preview-img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid #d6e0ff;
}

.remove-btn {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #2f3a5f;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  cursor: pointer;
}

/* 버튼 */
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
  background-position: right 10px center;
  padding-right: 48px;
}
</style>
