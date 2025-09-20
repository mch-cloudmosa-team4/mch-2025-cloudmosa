<template>
  <div class="app-container">
    <router-view class="main-content" />
    
    <!-- 新的底部導航欄 -->
    <nav v-if="!isLoginPage" class="bottom-nav">
      <!-- Home展開選單 - 圓弧形浮動選單 -->
      <div 
        v-if="showHomeMenu" 
        class="home-menu-overlay"
        @mouseenter="keepMenuOpen"
        @mouseleave="hideMenu"
      >
        <div class="circular-menu">
          <div class="menu-item item-1" @click="goToPage('/profile/' + getUserId())">
            <span class="material-icons-round">account_circle</span>
            <span class="item-label">Profile</span>
          </div>
          <div class="menu-item item-2" @click="goToPage('/job')">
            <span class="material-icons-round">work</span>
            <span class="item-label">Jobs</span>
          </div>
          <div class="menu-item item-3" @click="goToPage('/application')">
            <span class="material-icons-round">dashboard</span>
            <span class="item-label">Dashboard</span>
          </div>
          <div class="menu-item item-4" @click="goToPage('/profile')">
            <span class="material-icons-round">groups</span>
            <span class="item-label">Community</span>
          </div>
        </div>
      </div>
      
      <!-- 底部三個主要按鈕 -->
      <div class="nav-container">
        <!-- Chat按鈕 -->
        <div class="nav-item" :class="{ active: activeTab === 'chat' }" @click="goToChat">
          <span class="material-icons-round">
            {{ hasUnreadChat ? 'mark_unread_chat_alt' : 'chat' }}
          </span>
          <span v-if="activeTab === 'chat'" class="nav-label">Chat</span>
        </div>
        
        <!-- Home按鈕 -->
        <div 
          class="nav-item home-item" 
          :class="{ active: activeTab === 'home' || showHomeMenu }" 
          @click="goToHome"
          @mouseenter="showMenu"
          @mouseleave="hideMenu"
        >
          <span class="material-icons-round">home</span>
          <span v-if="activeTab === 'home' || showHomeMenu" class="nav-label">Home</span>
        </div>
        
        <!-- News按鈕 -->
        <div class="nav-item" :class="{ active: activeTab === 'news' }" @click="goToNews">
          <span class="material-icons-round">
            {{ hasUnreadNews ? 'notifications_active' : 'notifications' }}
          </span>
          <span v-if="activeTab === 'news'" class="nav-label">News</span>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getUserId } from './services/auth'

const router = useRouter()
const route = useRoute()
const showHomeMenu = ref(false)
const activeTab = ref('')
const hasUnreadChat = ref(false) // 模擬未讀聊天
const hasUnreadNews = ref(true) // 模擬未讀新聞

// 監聽路由變化，設置活動標籤
watch(route, (newRoute) => {
  const path = newRoute.path
  if (path.startsWith('/chat')) {
    activeTab.value = 'chat'
  } else if (path === '/home') {
    activeTab.value = 'home'
  } else if (path === '/news') {
    activeTab.value = 'news'
  } else {
    activeTab.value = ''
  }
  
  // 關閉home選單當路由改變時
  showHomeMenu.value = false
}, { immediate: true })

function goToChat() {
  router.push('/chat')
  hasUnreadChat.value = false // 標記為已讀
}

function goToNews() {
  router.push('/news')
  hasUnreadNews.value = false // 標記為已讀
}

function goToHome() {
  router.push('/home')
  showHomeMenu.value = false
}

function showMenu() {
  showHomeMenu.value = true
}

function hideMenu() {
  // 添加小延遲，避免鼠標快速移動時選單閃爍
  setTimeout(() => {
    showHomeMenu.value = false
  }, 100)
}

function keepMenuOpen() {
  showHomeMenu.value = true
}

function goToPage(path: string) {
  router.push(path)
  showHomeMenu.value = false
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
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: #f8f8f8;
  font-family: RobotoMono, sans-serif;
  position: relative;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  font-size: 14px;
}

/* 底部導航欄 */
.bottom-nav {
  position: relative;
  height: 60px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.nav-container {
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: space-around;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item.home-item {
  background: rgb(42, 65, 102);
  border-radius: 50%;
  width: 50px;
  height: 50px;
  color: white;
  margin-top: -10px;
  box-shadow: 0 2px 8px rgba(42, 65, 102, 0.3);
}

.nav-item.active {
  color: rgb(42, 65, 102);
}

.nav-item .material-icons-round {
  font-size: 24px;
  margin-bottom: 2px;
}

.nav-label {
  font-size: 9px;
  font-weight: 500;
  white-space: nowrap;
}

/* Home展開選單 - 圓弧形浮動選單 */
.home-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  pointer-events: none; /* 讓背景不攔截鼠標事件 */
}

.circular-menu {
  position: absolute;
  bottom: 120px;
  width: 220px;
  height: 120px;
  animation: fadeIn 0.3s ease-out;
  pointer-events: auto; /* 恢復選單的鼠標事件 */
}

.menu-item {
  position: absolute;
  width: 50px;
  height: 50px;
  background: white;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  animation: scaleIn 0.4s ease-out;
}

.menu-item:hover {
  transform: scale(1.1);
  background: rgb(42, 65, 102);
  color: white;
}

.menu-item .material-icons-round {
  font-size: 20px;
  color: rgb(42, 65, 102);
  margin-bottom: 2px;
}

.menu-item:hover .material-icons-round {
  color: white;
}

.item-label {
  font-size: 7px;
  font-weight: 600;
  color: rgb(42, 65, 102);
  white-space: nowrap;
}

.menu-item:hover .item-label {
  color: white;
}

/* 圓弧形排列 - 調整為更明顯的半圓弧 */
.item-1 {
  bottom: 30px;
  left: 15px;
  animation-delay: 0.1s;
}

.item-2 {
  bottom: 90px;
  left: 60px;
  animation-delay: 0.2s;
}

.item-3 {
  bottom: 90px;
  right: 60px;
  animation-delay: 0.3s;
}

.item-4 {
  bottom: 30px;
  right: 15px;
  animation-delay: 0.4s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 未讀狀態動畫 */
.nav-item .material-icons-round {
  animation: none;
}

.nav-item:has(.material-icons-round:contains('mark_unread_chat_alt')) .material-icons-round,
.nav-item:has(.material-icons-round:contains('notifications_active')) .material-icons-round {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}
</style>
