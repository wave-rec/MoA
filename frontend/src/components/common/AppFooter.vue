<template>
  <footer class="footer">
    <div class="layout-inner footer-inner">
      <!-- 왼쪽 영역 -->
      <div class="footer-left">
        <p class="footer-slogan">처음 재테크, 나만의 금융 친구 MoA</p>

        <!-- 링크 영역-->
        <div class="footer-links">
          <a
            href="https://github.com/wave-rec/MoA"
            target="_blank"
            rel="noopener noreferrer"
            class="footer-github"
          >
            <img src="@/assets/icons/github.svg" class="github-icon" />
            MoA Github
          </a>
        </div>
      </div>

      <!-- 오른쪽 영역 -->
      <div class="footer-right">
        <span class="footer-copy"> Copyright ⓒ 2025 MoA. All Rights Reserved. </span>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped>
.footer {
  border-top: 1px solid #e5e7eb;
  background-color: #ffffff;
}

.footer-inner {
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
}

/* ------------------------- */
/* 왼쪽 영역 전체              */
/* ------------------------- */
.footer-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 문구 */
.footer-slogan {
  margin: 0;
  font-size: 16px;
  color: #4b5563;
}

/* 링크 그룹 */
.footer-links {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* Github 링크 */
.footer-github {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: #6393f2;
  transition: 0.15s ease;
}

.footer-github:hover {
  color: #234fa7;
}

/* Github 아이콘 */
.github-icon {
  width: 16px;
  height: 16px;
  opacity: 0.8;
}

/* 오른쪽 카피라이트 */
.footer-copy {
  font-size: 12px;
  color: #9ca3af;
}

/* 모바일 반응형 */
@media (max-width: 960px) {
  .footer-inner {
    height: auto;
    flex-direction: column;
    align-items: flex-start;
    padding: 20px 16px;
    gap: 12px;
  }
}
</style>
