<template>
  <div class="layout">
    <header class="header-area">
      <AppHeaderGuest />
      <!-- <AppHeaderUser v-if="isLogin" /> -->
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

export default {
  components: { AppHeaderGuest, AppFooter, AppHeaderUser },
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
