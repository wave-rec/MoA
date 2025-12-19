import apiClient from '@/api/client'

// 은행 목록
export const fetchBanks = () => apiClient.get('/products/banks/')

// 추천
export const recommendProducts = (payload) => apiClient.post('/products/recommend/', payload)

// 상품 상세
export const fetchProductDetail = (id) => apiClient.get(`/products/${id}/`)
