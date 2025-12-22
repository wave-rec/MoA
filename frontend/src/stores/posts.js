import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const usePostStore = defineStore('post', () => {
  // ===== 전체 게시글 =====
  const posts = ref([])
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const currentPage = ref(1)
  const pageSize = 10

  const fetchPosts = async (category = null, search = '', page = 1) => {
    const params = { page }

    if (category) params.category = category
    if (search) params.search = search

    const res = await api.get('/api/v1/posts/', { params })

    posts.value = res.data.results
    count.value = res.data.count
    next.value = res.data.next
    previous.value = res.data.previous
    currentPage.value = page
  }

  // ===== 내가 쓴 게시글 =====
  const myPosts = ref([])

  const fetchMyPosts = async () => {
    const res = await api.get('/api/v1/posts/my/')
    myPosts.value = res.data
  }

  return {
    // 전체 게시글
    posts,
    count,
    next,
    previous,
    currentPage,
    pageSize,
    fetchPosts,

    // 내가 쓴 게시글
    myPosts,
    fetchMyPosts,
  }
})