<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="title">MoA 회원가입</h2>

      <form @submit.prevent="handleSignup" class="form">
        <!-- 이메일 -->
        <div class="field">
          <input
            type="email"
            placeholder="이메일"
            v-model="email"
            @blur="validateEmail"
          />
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>

        <!-- 비밀번호 -->
        <div class="field">
          <input
            type="password"
            placeholder="비밀번호 (8자 이상)"
            v-model="password"
            @blur="validatePassword"
          />
          <p v-if="errors.password" class="error">{{ errors.password }}</p>
        </div>

        <!-- 이름 -->
        <div class="field">
          <input
            type="text"
            placeholder="이름"
            v-model="name"
            @blur="validateName"
          />
          <p v-if="errors.name" class="error">{{ errors.name }}</p>
        </div>

        <!-- 나이 -->
        <div class="field">
          <input
            type="number"
            placeholder="나이"
            v-model="age"
            @blur="validateAge"
          />
          <p v-if="errors.age" class="error">{{ errors.age }}</p>
        </div>

        <button class="primary-btn" type="submit">
          회원가입
        </button>
      </form>

      <p class="link-text" @click="goLogin">
        로그인 하러가기
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { signup, login } from '@/api/auth'

const router = useRouter()

const email = ref('')
const password = ref('')
const name = ref('')
const age = ref('')

const errors = reactive({
  email: '',
  password: '',
  name: '',
  age: '',
})

const validateEmail = () => {
  errors.email = email.value ? '' : '이메일을 입력해주세요'
}

const validatePassword = () => {
  if (!password.value) {
    errors.password = '비밀번호를 입력해주세요'
  } else if (password.value.length < 8) {
    errors.password = '비밀번호는 8자 이상입니다'
  } else {
    errors.password = ''
  }
}

const validateName = () => {
  errors.name = name.value ? '' : '이름을 입력해주세요'
}

const validateAge = () => {
  errors.age = age.value ? '' : '나이를 입력해주세요'
}

const handleSignup = async () => {
  validateEmail()
  validatePassword()
  validateName()
  validateAge()

  if (
    errors.email ||
    errors.password ||
    errors.name ||
    errors.age
  ) return

  try {
    await signup({
      email: email.value,
      password: password.value,
      name: name.value,
      age: age.value,
    })

    // 🔥 회원가입 후 자동 로그인
    const res = await login({
      email: email.value,
      password: password.value,
    })

    localStorage.setItem('access_token', res.data.access)
    router.push('/')
  } catch {
    alert('회원가입 실패')
  }
}

const goLogin = () => router.push('/login')
</script>

<style scoped>
/* 로그인과 100% 동일 */
.auth-page {
  min-height: calc(100vh - 80px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-card {
  width: 420px;
  padding: 48px;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06);
  background: #ffffff;
  text-align: center;
}

.title {
  margin-bottom: 36px;
  font-size: 26px;
  font-weight: 700;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.field {
  display: flex;
  flex-direction: column;
}

.field input {
  height: 52px;
  padding: 0 18px;
  border-radius: 12px;
  border: 1px solid #d1d5db;
  font-size: 15px;
}

.field input:focus {
  outline: none;
  border-color: #6393f2;
}

.error {
  margin-top: 6px;
  font-size: 13px;
  color: #ef4444;
}

.primary-btn {
  height: 52px;
  border-radius: 12px;
  border: none;
  background-color: #6393f2;
  color: #ffffff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.primary-btn:hover {
  background-color: #4f7fe0;
}

.link-text {
  margin-top: 22px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
}

.link-text:hover {
  color: #6393f2;
}
</style>
