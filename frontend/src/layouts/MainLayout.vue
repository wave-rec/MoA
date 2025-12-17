<template>
  <div class="layout">
    <header class="header-area">
      <AppHeaderGuest v-if="!auth.isLogin" />
      <AppHeaderUser v-else />
    </header>

    <main class="main-area">
      <router-view />
    </main>

    <footer class="footer-area">
      <AppFooter />
    </footer>
  </div>
</template>

<script>
import AppHeaderGuest from '@/components/common/AppHeaderGuest.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import AppHeaderUser from '@/components/common/AppHeaderUser.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  components: {
    AppHeaderGuest,
    AppHeaderUser,
    AppFooter,
  },

  setup() {
    const auth = useAuthStore()
    console.log('LAYOUT isLogin:', auth.isLogin)
    return {
      auth,
    }
  },
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-area {
  flex-shrink: 0;
}

.main-area {
  flex: 1;
  min-height: 2000px;
}

.footer-area {
  flex-shrink: 0;
}
</style>
