import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const usePostStore = defineStore('post', () => {
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

  return {
    posts,
    count,
    next,
    previous,
    currentPage,
    fetchPosts,
    pageSize, 
  }
})
