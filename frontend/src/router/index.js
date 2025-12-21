import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import BankSearchView from '@/views/BankSearchView.vue'
import MyPageView from '@/views/MyPageView.vue'
import ProfileEditView from '@/views/ProfileEditView.vue'
import RecommendView from '@/views/RecommendView.vue'
import PostListView from '@/views/PostListView.vue'
import PostCreateView from '@/views/PostCreateView.vue'
import PostDetailView from '@/views/PostDetailView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: 'login',
          name: 'login',
          component: LoginView,
        },
        {
          path: 'signup',
          name: 'signup',
          component: SignupView,
        },
        {
          path: 'banks',
          name: 'banks',
          component: BankSearchView,
        },
        {
          path: 'mypage',
          name: 'mypage',
          component: MyPageView,
        },
        {
          path: 'profile/edit',
          name: 'profile-edit',
          component: ProfileEditView,
        },
        {
          path: '/recommend',
          name: 'recommend',
          component: RecommendView,
        },
        {
          path: 'posts',
          name: 'posts',
          component: PostListView,
        },
        {
          path: 'posts/create',
          name: 'post-create',
          component: PostCreateView,
        },
        {
          path: 'posts/:id',
          name: 'post-detail',
          component: PostDetailView,
          props: true,
        },
        {
          path: '/products/:id',
          name: 'ProductDetail',
          component: ProductDetailView,
        },
      ],
    },
  ],
})

export default router
