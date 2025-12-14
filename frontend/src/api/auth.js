import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

export const login = (payload) => {
  return axios.post(`${API_URL}/auth/login/`, payload)
}

export const signup = (payload) => {
  return axios.post(`${API_URL}/auth/signup/`, payload)
}
