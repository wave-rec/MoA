import api from './axios'

// 내 정보 조회
export const getMyInfo = () => {
  return api.get('/auth/me/')
}

// 비밀번호 변경
export const changePassword = (data) => {
  return api.post('/auth/password/', data)
}


// 회원정보 수정
export const updateMyInfo = (data) => {
  return api.patch('/auth/me/', data)
}

// 회원탈퇴
export const withdrawUser = () => {
  return api.delete('/auth/withdraw/')
}
