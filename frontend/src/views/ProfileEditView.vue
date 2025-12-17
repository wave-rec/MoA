<template>
  <div class="edit-page">
    <h2>회원정보 수정</h2>

    <form class="edit-form" @submit.prevent="submit">
      <label>
        이름
        <input v-model="name" />
      </label>

      <label>
        나이
        <input type="number" v-model="age" />
      </label>

      <button class="save-btn">저장</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMyInfo, updateMyInfo } from '@/api/user'

const router = useRouter()

const name = ref('')
const age = ref('')

// 기존 정보 불러오기
onMounted(async () => {
  const res = await getMyInfo()
  name.value = res.data.name
  age.value = res.data.age
})

// 저장 버튼
const submit = async () => {
  await updateMyInfo({
    name: name.value,
    age: age.value,
  })

  alert('회원정보가 수정되었습니다')
  router.push({ name: 'mypage' })
}
</script>


<style scoped>
.edit-page {
  max-width: 480px;
  margin: 80px auto;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.save-btn {
  margin-top: 20px;
  height: 44px;
  border: none;
  border-radius: 10px;
  background: #6393f2;
  color: white;
  font-weight: 600;
  cursor: pointer;
}
</style>
