import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // 토큰 상태
  const accessToken = ref(localStorage.getItem('access_token'))
  const user = ref(
    localStorage.getItem('user')
      ? JSON.parse(localStorage.getItem('user'))
      : null
  )

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
  const setUser = (userData) => {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }
  

  return {
    accessToken,
    user, 
    isLogin,
    setToken,
    logout,
    setUser,
  }
})
