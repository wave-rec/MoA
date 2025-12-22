<template>
  <div class="edit-page">
    <h2>회원정보 수정</h2>

    <form class="edit-form" @submit.prevent="submitAll">
      <label>
        이름
        <input v-model="name" />
      </label>

      <label>
        나이
        <input type="number" v-model="age" />
      </label>

      <label>
        이메일
        <input type="email" v-model="email" />
      </label>

      <hr />

      <h3>비밀번호 변경 (선택)</h3>

      <label>
        현재 비밀번호
        <input type="password" v-model="currentPassword" />
      </label>

      <label>
        새 비밀번호
        <input type="password" v-model="newPassword" />
      </label>

      <button class="save-btn">저장</button>
    </form>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyInfo, updateMyInfo, changePassword } from '@/api/user'

const router = useRouter()

const name = ref('')
const age = ref('')
const email = ref('')

const currentPassword = ref('')
const newPassword = ref('')

// 기존 정보 불러오기
onMounted(async () => {
  const res = await getMyInfo()
  name.value = res.data.name
  age.value = res.data.age
  email.value = res.data.email
})

// 저장 버튼 하나로 처리
const submitAll = async () => {
  try {
    // 1️⃣ 프로필 정보 수정
    await updateMyInfo({
      name: name.value,
      age: age.value,
      email: email.value,
    })

    // 2️⃣ 비밀번호 변경 (선택)
    if (currentPassword.value || newPassword.value) {
      if (!currentPassword.value || !newPassword.value) {
        alert('비밀번호를 변경하려면 현재/새 비밀번호를 모두 입력해주세요')
        return
      }

      await changePassword({
        current_password: currentPassword.value,
        new_password: newPassword.value,
      })

      alert('비밀번호가 변경되었습니다. 다시 로그인해주세요.')
      localStorage.clear()
      router.push({ name: 'login' })
      return
    }

    alert('회원정보가 수정되었습니다')
    router.push({ name: 'mypage' })
  } catch (err) {
    console.error(err)
    alert('수정 중 오류가 발생했습니다')
  }
}
</script>


<style scoped>
.edit-page {
  max-width: 480px;
  margin: 80px auto;
}

.edit-form,
.password-box {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.password-box {
  margin-top: 40px;
}

label {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input {
  height: 42px;
  padding: 0 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.save-btn,
.password-btn {
  height: 44px;
  border: none;
  border-radius: 10px;
  background: #6393F2;
  color: white;
  font-weight: 600;
  cursor: pointer;
}
</style>
