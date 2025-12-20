import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const useCommentStore = defineStore('comment', () => {
  const comments = ref([])

  const fetchComments = async (postId) => {
    const res = await api.get(`posts/${postId}/comments/`)
    comments.value = res.data
  }

  const createComment = async (postId, content) => {
    await api.post(`posts/${postId}/comments/`, { content })
    await fetchComments(postId)
  }

  return { comments, fetchComments, createComment }
})
