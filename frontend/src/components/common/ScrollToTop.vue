<template>
  <Transition name="fade">
    <div v-show="isVisible" class="scroll-to-top" @click="scrollToTop">
      <img src="@/assets/top-button.png" alt="맨 위로" class="top-icon" />
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)

const handleScroll = () => {
  isVisible.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.scroll-to-top {
  position: fixed;
  bottom: 40px;
  right: 40px;
  cursor: pointer;
  z-index: 999;
  transition: transform 0.2s;
}

.scroll-to-top:hover {
  transform: translateY(-5px);
}

.top-icon {
  width: 80px;
  height: 80px;

  object-fit: contain;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.scroll-to-top {
  position: fixed;
  bottom: 50px;
  right: 50px;
  z-index: 1000;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
