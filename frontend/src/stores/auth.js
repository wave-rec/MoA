import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // 토큰 상태
  const accessToken = ref(localStorage.getItem('access_token'))

  // 로그인 여부
  const isLogin = computed(() => !!accessToken.value)

  // 로그인 성공 시 호출
  const setToken = (token) => {
    accessToken.value = token
    localStorage.setItem('access_token', token)
  }

  // 로그아웃 시 호출
  const logout = () => {
    accessToken.value = null
    localStorage.removeItem('access_token')
  }

  return {
    accessToken,
    isLogin,
    setToken,
    logout,
  }
})
