<template>
  <div class="app-container">
    <RouterView />

    <ScrollToTop />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import ScrollToTop from '@/components/common/ScrollToTop.vue'
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  position: relative;
}
</style>
