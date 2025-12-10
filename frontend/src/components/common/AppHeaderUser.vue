<template>
  <header class="header">
    <div class="layout-inner header-inner">
      <!-- 로고 -->
      <div class="logo-section">
        <img :src="logoSrc" alt="MoA 로고" class="logo-image" />
      </div>

      <!-- 데스크탑용 네비게이션 -->
      <nav class="navigation desktop-only">
        <button class="nav-link">모아의 모든 것</button>
        <button class="nav-link">예금 적금 추천</button>
        <button class="nav-link">은행 지점 찾기</button>
        <button class="nav-link">게시판</button>
      </nav>

      <!-- 데스크탑용: 검색 + 홈 + 프로필 -->
      <div class="right-section desktop-only">
        <div class="search-box">
          <input type="text" placeholder="검색" class="search-input" />
          <button class="search-button">
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
          </button>
        </div>

        <div class="auth-buttons">
          <button class="auth-link">홈</button>

          <!-- 로그인 후 전용 프로필 버튼 -->
          <button class="auth-link primary profile-button">
            <svg class="profile-icon" viewBox="0 0 24 24" aria-hidden="true">
              <path
                d="M12 12c2.2 0 4-1.8 4-4s-1.8-4-4-4-4 1.8-4 4 1.8 4 4 4zm0 2c-2.8 0-8 1.4-8 4v1.5h16V18c0-2.6-5.2-4-8-4z"
                fill="currentColor"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- 모바일용 햄버거 -->
      <button class="menu-toggle mobile-only" @click="toggleMenu">
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
        <span class="menu-bar"></span>
      </button>
    </div>

    <!-- 모바일 드롭다운 메뉴 -->
    <transition name="mobile-menu-fade">
      <div v-if="isMenuOpen" class="mobile-menu mobile-only">
        <nav class="mobile-nav">
          <button class="mobile-nav-link">모아의 모든 것</button>
          <button class="mobile-nav-link">예금 적금 추천</button>
          <button class="mobile-nav-link">은행 지점 찾기</button>
          <button class="mobile-nav-link">게시판</button>
        </nav>

        <div class="mobile-auth">
          <button class="mobile-auth-btn">홈</button>
          <button class="mobile-auth-btn primary">마이페이지</button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import logoSrc from '@/assets/logo-moa.png'

const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}
</script>

<style scoped>
/* ====== 공통 레이아웃 (로그인 전과 동일) ====== */
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
  flex-shrink: 0;
}

.logo-image {
  height: 56px;
  display: block;
}

/* 중앙 메뉴 */
.navigation {
  display: flex;
  align-items: center;
  gap: 36px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  padding: 0;
  border: none;
  background: transparent;
  font-size: 17px;
  font-weight: 600;
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

/* 우측 영역 */
.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
  flex-shrink: 0;
  width: 360px;
  justify-content: flex-end;
}

/* 검색창 */
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
  font-size: 15px;
  outline: none;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  border-radius: 999px;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  cursor: pointer;
}

.search-icon {
  width: 18px;
  height: 18px;
}

/* 홈 / 프로필 (데스크탑) */
.auth-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.auth-link {
  min-width: 54px;
  padding: 0 18px;
  white-space: nowrap;
  height: 34px;
  border-radius: 999px;
  border: none;
  background: transparent;
  font-size: 15px;
  font-weight: 500;
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

/* 로그인 후 전용 프로필 버튼 */
.profile-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.profile-button:hover {
  transform: translateY(-1px);
}

.profile-icon {
  width: 22px;
  height: 22px;
  color: #6393f2;
}

/* 공통: 데스크탑 / 모바일 표시 제어 */
.desktop-only {
  display: flex;
}

.mobile-only {
  display: none;
}

/* 햄버거 버튼 */
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

/* 모바일 드롭다운 메뉴 */
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
  padding: 8px 0;
  border: none;
  background: transparent;
  font-size: 15px;
  font-weight: 500;
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
  font-weight: 500;
  cursor: pointer;
}

.mobile-auth-btn.primary {
  background-color: #6393f2;
  border-color: #6393f2;
  color: #ffffff;
}

/* 모바일 메뉴 페이드 효과 */
.mobile-menu-fade-enter-active,
.mobile-menu-fade-leave-active {
  transition: opacity 0.18s ease;
}
.mobile-menu-fade-enter-from,
.mobile-menu-fade-leave-to {
  opacity: 0;
}

/* 반응형 브레이크포인트 (로그인 전과 동일) */
@media (max-width: 960px) {
  .header-inner {
    height: 64px;
    padding: 0 16px;
  }

  .logo-section {
    gap: 8px;
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
