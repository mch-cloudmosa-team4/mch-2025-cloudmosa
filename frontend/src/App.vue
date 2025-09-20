<template>
  <div class="app-container">
    <button v-if="!isLoginPage" class="menu-btn" @click="toggleMenu">☰</button>
    <router-view class="main-content" />
    <nav v-if="!isLoginPage" class="bottom-bar">
      <button @click="$router.push('/home')">Home</button>
      <button @click="$router.push('/chat')">Messages</button>
      <button @click="goMyProfile">Profile</button>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getUserId } from './services/auth'

const router = useRouter()
const route = useRoute()
const previousPage = ref<string>('')

// 監聽路由變化，記錄非menu頁面
watch(route, (newRoute) => {
  if (newRoute.path !== '/menu' && newRoute.path !== '/login') {
    previousPage.value = newRoute.path
  }
}, { immediate: true })

function goMyProfile() {
  if (getUserId()) {
    router.push(`/profile/${getUserId()}`)
  } else {
    alert('Please login first')
  }
}

function toggleMenu() {
  if (route.path === '/menu') {
    // 如果當前在menu頁面，返回之前的頁面
    if (previousPage.value) {
      router.push(previousPage.value)
    } else {
      router.push('/home') // 如果沒有記錄，默認回到home
    }
  } else {
    // 如果不在menu頁面，去menu
    router.push('/menu')
  }
}

const isLoginPage = computed(() => route.path === '/login')
</script>

<style scoped>
@font-face {
  font-family: RobotoMono;
  src: url(import.meta.env.BASE_URL + 'RobotoMono.ttf');
}

.app-container {
  width: 240px;
  height: 320px;
  margin: 0 auto;
  overflow: hidden; /* 超出部分隱藏 */
  display: flex;
  flex-direction: column;
  background: #f8f8f8;
  font-family: Arial, sans-serif;
  align-items: center;
  font-family: RobotoMono, sans-serif;
  position: relative;
}

.main-content {
  flex: 1;
  overflow-y: auto; /* 可上下捲動 */
  font-size: 14px;
}

.bottom-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 40px;
  width: 100%;
  background: #333;
  color: white;
}

.bottom-bar button {
  flex: 1;
  height: 100%;
  border: none;
  background: none;
  color: white;
  font-size: 14px;
}

.bottom-bar button:focus {
  background: #555; /* 按鍵選中狀態 */
}

.bottom-bar button:disabled {
  color: #aaa;
}

.menu-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  border: none;
  background: none;
  font-size: 18px;
  z-index: 1000;
}
</style>
