<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="title">MoA 로그인</h2>

      <form @submit.prevent="handleLogin" class="form">
        <div class="field">
          <input
            type="email"
            placeholder="이메일"
            v-model="email"
            @blur="validateEmail"
          />
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>

        <div class="field">
          <input
            type="password"
            placeholder="비밀번호"
            v-model="password"
            @blur="validatePassword"
          />
          <p v-if="errors.password" class="error">{{ errors.password }}</p>
        </div>

        <button class="primary-btn" type="submit">
          로그인
        </button>
      </form>

      <p class="link-text" @click="goSignup">회원가입</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()

const router = useRouter()

const email = ref('')
const password = ref('')

const errors = reactive({
  email: '',
  password: '',
})

const validateEmail = () => {
  errors.email = email.value ? '' : '이메일을 입력해주세요'
}

const validatePassword = () => {
  errors.password = password.value ? '' : '비밀번호를 입력해주세요'
}

const handleLogin = async () => {
  validateEmail()
  validatePassword()
  if (errors.email || errors.password) return

  try {
    const res = await login({
      email: email.value,
      password: password.value,
    })

    authStore.setToken(res.data.access_token)

    authStore.setUser({
      id: res.data.user.id,
      name: res.data.user.name,
      email: res.data.user.email,
    })

    router.push({ name: 'home' })
  } catch {
    alert('로그인 실패')
  }
}


const goSignup = () => router.push('/signup')
</script>

<style scoped>
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
