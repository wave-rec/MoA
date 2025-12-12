<template>
  <header class="header">
    <div class="layout-inner header-inner">
      <!-- 로고 -->
      <div class="logo-section" @click="goHome">
        <img :src="logoSrc" alt="MoA 로고" class="logo-image" />
      </div>

      <!-- 데스크톱 네비게이션 -->
      <nav class="navigation desktop-only">
        <button class="nav-link">모아의 모든 것</button>
        <button class="nav-link">예금 적금 추천</button>
        <button class="nav-link">은행 지점 찾기</button>
        <button class="nav-link">게시판</button>
      </nav>

      <!-- 우측 영역 -->
      <div class="right-section desktop-only">
        <div class="search-box">
          <input type="text" placeholder="검색" class="search-input" />
          <button class="search-button">
            <svg class="search-icon" viewBox="0 0 24 24">
              <path
                d="M21 21l-4.35-4.35m0 0A6.5 6.5 0 105.5 5.5a6.5 6.5 0 0011.15 11.15z"
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
              />
            </svg>
          </button>
        </div>

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
          <button class="mobile-nav-link">모아의 모든 것</button>
          <button class="mobile-nav-link">예금 적금 추천</button>
          <button class="mobile-nav-link">은행 지점 찾기</button>
          <button class="mobile-nav-link">게시판</button>
        </nav>

        <div class="mobile-auth">
          <button class="mobile-auth-btn" @click="goHome">홈</button>
          <button class="mobile-auth-btn primary" @click="goLogin">
            로그인
          </button>
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
  gap: 24px;
  padding: 0 28px;
}

/* 로고 */
.logo-section {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.logo-image {
  height: 56px;
}

/* 중앙 메뉴 */
.navigation {
  display: flex;
  gap: 36px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  border: none;
  background: transparent;
  font-size: 17px;
  font-weight: 600;
  color: #111827;
  cursor: pointer;
}

.nav-link:hover {
  color: #6393f2;
}

/* 우측 */
.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 360px;
  justify-content: flex-end;
}

/* 검색 */
.search-box {
  position: relative;
}

.search-input {
  width: 220px;
  height: 36px;
  border-radius: 999px;
  border: none;
  background-color: #f3f4f6;
  padding: 0 60px 0 20px;
}

.search-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  cursor: pointer;
}

.search-icon {
  width: 18px;
  height: 18px;
}

/* 홈 / 로그인 버튼 (글자 깨짐 해결 핵심) */
.auth-buttons {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.auth-link {
  min-width: 72px;
  height: 34px;
  padding: 0 18px;
  border-radius: 999px;
  border: none;
  background: transparent;
  font-size: 15px;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
}

.auth-link:hover {
  color: #6393f2;
}

.auth-link.primary {
  background-color: #6393f2;
  color: #ffffff;
}

.auth-link.primary:hover {
  background-color: #223459;
}

/* 모바일 */
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
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 12px 16px;
}

.mobile-auth {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
}

.mobile-auth-btn {
  flex: 1;
  height: 38px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
}

.mobile-auth-btn.primary {
  background-color: #6393f2;
  color: #ffffff;
  border-color: #6393f2;
}

@media (max-width: 960px) {
  .desktop-only {
    display: none;
  }

  .mobile-only {
    display: block;
  }

  .menu-toggle {
    display: flex;
  }

  .header-inner {
    height: 64px;
    padding: 0 16px;
  }
}
</style>
