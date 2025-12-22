<template>
  <header class="header">
    <div class="layout-inner header-inner">
      <!-- 로고 -->
      <div class="logo-section" @click="goHome">
        <img :src="logoSrc" alt="MoA 로고" class="logo-image" />
      </div>

      <!-- 데스크톱 네비게이션 -->
      <nav class="navigation desktop-only">
        <button class="nav-link" @click="goRecommend">예금 적금 추천</button>
        <button class="nav-link" @click="goExchange">금•은 시세 확인</button>
        <button class="nav-link" @click="goBanks">은행 지점 찾기</button>
        <button class="nav-link" @click="goPosts">게시판</button>
      </nav>

      <!-- 우측 영역 -->
      <div class="right-section desktop-only">
        <button class="search-box" @click="goYoutube">
          <svg class="search-icon" viewBox="0 0 24 24" aria-hidden="true">
            <path
              d="M21 21l-4.35-4.35m0 0A6.5 6.5 0 105.5 5.5a6.5 6.5 0 0011.15 11.15z"
              fill="none"
              stroke="currentColor"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.8"
            />
          </svg>
          <span class="search-text">Youtube에서 금융 용어 검색해보기</span>
        </button>

        <div class="auth-buttons">
          <button class="auth-link" @click="goHome">홈</button>
          <button class="auth-link primary" @click="goLogin">로그인</button>
        </div>
      </div>

      <!-- 모바일 햄버거 -->
      <button class="menu-toggle mobile-only" @click="toggleMenu">
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
      </button>
    </div>

    <!-- 모바일 메뉴 -->
    <transition name="mobile-menu-fade">
      <div v-if="isMenuOpen" class="mobile-menu mobile-only">
        <nav class="mobile-nav">
          <button class="mobile-nav-link" @click="goRecommend">예금 적금 추천</button>
          <button class="mobile-nav-link" @click="goExchange">금•은 시세 확인</button>
          <button class="mobile-nav-link" @click="goBanks">은행 지점 찾기</button>
          <button class="mobile-nav-link" @click="goPosts">게시판</button>
          <button class="mobile-nav-link" @click="goYoutube">금융 용어 알아보기</button>
        </nav>

        <div class="mobile-auth">
          <button class="mobile-auth-btn" @click="goHome">홈</button>
          <button class="mobile-auth-btn primary" @click="goLogin">로그인</button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import logoSrc from '@/assets/logo-moa.png'

const router = useRouter()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const goHome = () => {
  isMenuOpen.value = false
  router.push({ name: 'home' })
}

const goLogin = () => {
  isMenuOpen.value = false
  router.push({ name: 'login' })
}

const goRecommend = () => {
  isMenuOpen.value = false
  router.push({ name: 'recommend' })
}

const goExchange = () => {
  isMenuOpen.value = false
  router.push({ name: 'commodity' })
}

const goBanks = () => {
  isMenuOpen.value = false
  router.push({ name: 'banks' })
}

const goPosts = () => {
  isMenuOpen.value = false
  router.push({ name: 'posts' })
}

const goYoutube = () => {
  isMenuOpen.value = false
  router.push({ name: 'YoutubeSearch' })
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.header-inner {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 0 28px;
}

.logo-section {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  cursor: pointer;
}

.logo-image {
  height: 56px;
  display: block;
}

.navigation {
  display: flex;
  align-items: center;
  gap: 28px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  padding: 0;
  border: none;
  background: transparent;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #111827;
  cursor: pointer;
  white-space: nowrap;
  transition:
    color 0.15s ease,
    transform 0.15s ease;
}

.nav-link:hover {
  color: #6393f2;
  transform: translateY(-1px);
}

.right-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
  justify-content: flex-end;
}

.search-box {
  position: relative;
  width: 200px;
  height: 36px;
  border-radius: 999px;
  border: none;
  background-color: #f3f4f6;
  padding: 0 18px 0 50px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.search-box:hover {
  width: 250px;
  background-color: #e5e7eb;
}

.search-text {
  color: #9ca3af;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-icon {
  position: absolute;
  left: 18px;
  width: 18px;
  height: 18px;
  color: #6b7280;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.auth-link {
  min-width: 54px;
  padding: 0 16px;
  white-space: nowrap;
  height: 34px;
  border-radius: 999px;
  border: none;
  background: transparent;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: #111827;
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.auth-link:hover {
  color: #6393f2;
  transform: translateY(-1px);
}

.auth-link.primary {
  background-color: #6393f2;
  color: #ffffff;
}

.auth-link.primary:hover {
  background-color: #4f7de0;
}

.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

.menu-toggle {
  width: 40px;
  height: 40px;
  background: transparent;
  border: none;
  display: none;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
}

.menu-bar {
  width: 18px;
  height: 2px;
  background-color: #6393f2;
}

.mobile-menu {
  border-top: 1px solid #e5e7eb;
  background-color: #ffffff;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 16px 8px;
}

.mobile-nav-link {
  text-align: left;
  padding: 10px 0;
  border: none;
  background: transparent;
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  cursor: pointer;
}

.mobile-nav-link:hover {
  color: #6393f2;
}

.mobile-auth {
  display: flex;
  gap: 8px;
  padding: 0 16px 12px;
}

.mobile-auth-btn {
  flex: 1;
  height: 38px;
  border: 1px solid #e5e7eb;
  background-color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.mobile-auth-btn:hover {
  border-color: #6393f2;
}

.mobile-auth-btn.primary {
  background-color: #6393f2;
  border-color: #6393f2;
  color: #ffffff;
}

.mobile-menu-fade-enter-active,
.mobile-menu-fade-leave-active {
  transition: opacity 0.18s ease;
}

.mobile-menu-fade-enter-from,
.mobile-menu-fade-leave-to {
  opacity: 0;
}

@media (max-width: 1200px) {
  .navigation {
    gap: 20px;
  }

  .nav-link {
    font-size: 16px;
  }

  .search-box {
    width: 180px;
  }

  .search-box:hover {
    width: 200px;
  }
}

@media (max-width: 960px) {
  .header-inner {
    height: 64px;
    padding: 0 16px;
  }

  .logo-image {
    height: 48px;
  }

  .desktop-only {
    display: none;
  }

  .mobile-only {
    display: block;
  }

  .menu-toggle {
    display: flex;
    margin-left: auto;
  }
}
</style>
