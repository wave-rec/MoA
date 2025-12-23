<template>
  <div class="mypage">
    <!-- 상단 영역 -->
    <section class="profile-card">
      <div class="profile-left">
        <!-- 파란 사람 아이콘 -->
        <div class="avatar">
          <svg viewBox="0 0 24 24">
            <path
              d="M12 12c2.2 0 4-1.8 4-4s-1.8-4-4-4
                 -4 1.8-4 4 1.8 4 4 4zm0 2
                 c-2.8 0-8 1.4-8 4v2h16v-2
                 c0-2.6-5.2-4-8-4z"
            />
          </svg>
        </div>

        <!-- 유저 정보 -->
        <div class="info">
          <h2>{{ user.name }}</h2>
          <p>{{ user.age }}세</p>
        </div>
      </div>

      <div class="profile-right">
        <button class="logout" @click="logout">로그아웃</button>
      </div>
    </section>

    <!-- 메뉴 카드 -->
    <section class="menu-grid">
      <div class="menu-card" @click="goEdit">
        <h3>회원정보 수정</h3>
        <p>개인 정보 및 비밀번호 변경</p>
      </div>

      <div class="menu-card" @click="goLikes">
        <h3>가입 상품 목록</h3>
        <p>가입 상품 한눈에 보기</p>
      </div>
      <div class="menu-card" @click="goPosts">
        <h3>내가 쓴 게시글</h3>
        <p>작성한 글 관리</p>
      </div>
    </section>

    <!-- 위험 영역 -->
    <section class="danger-zone">
      <button class="withdraw" @click="handleWithdraw">회원 탈퇴</button>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyInfo, withdrawUser } from '@/api/user'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = ref({
  name: '',
  age: '',
})

// 마이페이지 진입 시 내 정보 조회
onMounted(async () => {
  const res = await getMyInfo()
  user.value = res.data
})

// 회원정보 수정
const goEdit = () => {
  router.push({ name: 'profile-edit' })
}

// 찜 목록

const goLikes = () => {
  router.push({ name: 'LikedProducts' })
}

// 내가 쓴 게시글
const goPosts = () => {
  router.push({ name: 'my-posts' })
}

// 로그아웃
const logout = () => {
  authStore.logout()
  router.push({ name: 'home' })
}

// 회원탈퇴
const handleWithdraw = async () => {
  if (!confirm('정말 회원 탈퇴하시겠습니까?')) return

  await withdrawUser()
  authStore.logout()
  router.push({ name: 'home' })
}
</script>



<style scoped>
.mypage {
  max-width: 960px;
  margin: 0 auto;
  padding: 60px 20px;
}

/* ===== 프로필 카드 ===== */
.profile-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px;
  border-radius: 20px;
  background: #f9fafb;
  margin-bottom: 60px;
}

.profile-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #6393f2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar svg {
  width: 36px;
  height: 36px;
  fill: white;
}

.info h2 {
  font-size: 20px;
  margin-bottom: 6px;
}

.info p {
  color: #6b7280;
}

.logout {
  border: none;
  background: transparent;
  color: #ef4444;
  font-size: 14px;
  cursor: pointer;
}

/* ===== 메뉴 카드 ===== */
.menu-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.menu-card {
  padding: 28px;
  border-radius: 18px;
  background: white;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: all 0.2s ease;
}

.menu-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.menu-card h3 {
  font-size: 16px;
  margin-bottom: 8px;
}

.menu-card p {
  font-size: 14px;
  color: #6b7280;
}

/* ===== 위험 영역 ===== */
.danger-zone {
  margin-top: 80px;
  text-align: center;
}

.withdraw {
  border: none;
  background: none;
  color: #9ca3af;
  font-size: 14px;
  cursor: pointer;
}

.withdraw:hover {
  color: #ef4444;
}

/* ===== 반응형 ===== */
@media (max-width: 768px) {
  .menu-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .profile-left {
    flex-direction: column;
  }
}
</style>
