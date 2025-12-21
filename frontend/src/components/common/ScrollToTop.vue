<template>
  <Transition name="fade">
    <div
      v-show="isVisible"
      class="scroll-to-top"
      :class="{ 'above-footer': isAboveFooter }"
      @click="scrollToTop"
    >
      <img src="@/assets/top-button.png" alt="맨 위로" class="top-icon" />
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)
const isAboveFooter = ref(false)

const handleScroll = () => {
  const scrollY = window.scrollY
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight

  isVisible.value = scrollY > 300

  const footerHeight = 150
  const bottomThreshold = documentHeight - windowHeight - footerHeight

  isAboveFooter.value = scrollY > bottomThreshold
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
  right: 50px;
  cursor: pointer;
  z-index: 1000;
  transition:
    bottom 0.3s ease-in-out,
    transform 0.2s ease-in-out,
    opacity 0.3s;
}

.scroll-to-top.above-footer {
  bottom: 170px;
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
