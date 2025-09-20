<template>
  <div class="app-container">
    <router-view class="main-content" />
    
    <!-- 新的底部導航欄 -->
    <nav v-if="!isLoginPage" class="bottom-nav">
      <!-- Home展開選單 - 圓弧形浮動選單 -->
      <div 
        v-if="showHomeMenu" 
        class="home-menu-overlay"
        @mouseenter="cancelHideTimer"
        @mouseleave="startHideTimer"
      >
        <div class="circular-menu">
          <div 
            class="menu-item item-1" 
            @click="goToPage('/profile/' + getUserId())"
            @mouseenter="showProfileLabel = true"
            @mouseleave="showProfileLabel = false"
          >
            <span class="material-icons-round">account_circle</span>
            <span v-if="showProfileLabel" class="item-label">Profile</span>
          </div>
          <div 
            class="menu-item item-2" 
            @click="goToPage('/job')"
            @mouseenter="showJobsLabel = true"
            @mouseleave="showJobsLabel = false"
          >
            <span v-if="showJobsLabel" class="item-label">Jobs</span>
            <span class="material-icons-round">work</span>
          </div>
          <div 
            class="menu-item item-3" 
            @click="goToPage('/dashboard')"
            @mouseenter="showDashboardLabel = true"
            @mouseleave="showDashboardLabel = false"
          >
            <span v-if="showDashboardLabel" class="item-label">Dashboard</span>
            <span class="material-icons-round">dashboard</span>
          </div>
          <div 
            class="menu-item item-4" 
            @click="goToPage('/profile')"
            @mouseenter="showCommunityLabel = true"
            @mouseleave="showCommunityLabel = false"
          >
            <span class="material-icons-round">groups</span>
            <span v-if="showCommunityLabel" class="item-label">Community</span>
          </div>
        </div>
      </div>
      
      <!-- 底部三個主要按鈕 -->
      <div class="nav-container">
        <!-- Chat按鈕 -->
        <div 
          class="nav-item" 
          :class="{ active: activeTab === 'chat' }" 
          @click="goToChat"
          @mouseenter="showChatLabel = true"
          @mouseleave="showChatLabel = false"
        >
          <span class="material-icons-round">
            {{ hasUnreadChat ? 'mark_unread_chat_alt' : 'chat' }}
          </span>
          <span v-if="showChatLabel" class="nav-label">Chat</span>
        </div>
        
        <!-- Home按鈕 -->
        <div 
          class="nav-item home-item" 
          :class="{ active: activeTab === 'home' }" 
          @click="goToHome"
          @mouseenter="showMenu"
          @mouseleave="startHideTimer"
        >
          <span class="material-icons-round">home</span>
          <span v-if="showHomeMenu" class="nav-label">Home</span>
        </div>
        
        <!-- News按鈕 -->
        <div 
          class="nav-item" 
          :class="{ active: activeTab === 'news' }" 
          @click="goToNews"
          @mouseenter="showNewsLabel = true"
          @mouseleave="showNewsLabel = false"
        >
          <span class="material-icons-round">
            {{ hasUnreadNews ? 'notifications_active' : 'notifications' }}
          </span>
          <span v-if="showNewsLabel" class="nav-label">News</span>
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
const showChatLabel = ref(false)
const showNewsLabel = ref(false)
const showProfileLabel = ref(false)
const showJobsLabel = ref(false)
const showDashboardLabel = ref(false)
const showCommunityLabel = ref(false)
let hideTimer: number | null = null

// 計算屬性
const isLoginPage = computed(() => route.path === '/login')

const activeTab = computed(() => {
  const currentRoute = route.name as string
  if (!currentRoute) return 'home'
  
  if (['chat', 'chatroom'].includes(currentRoute)) return 'chat'
  if (['home'].includes(currentRoute)) return 'home'
  if (['news'].includes(currentRoute)) return 'news'
  return 'home'
})

const hasUnreadChat = computed(() => {
  // 這裡可以根據實際需求來判斷是否有未讀聊天
  return false
})

const hasUnreadNews = computed(() => {
  // 這裡可以根據實際需求來判斷是否有未讀通知
  return true
})

// 方法
function showMenu() {
  // 清除任何現有的隱藏計時器
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
  showHomeMenu.value = true
}

function startHideTimer() {
  // 設置延遲隱藏
  hideTimer = setTimeout(() => {
    showHomeMenu.value = false
    hideTimer = null
  }, 200)
}

function cancelHideTimer() {
  // 取消隱藏計時器
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
}

function hideMenu() {
  // 立即隱藏選單
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
  showHomeMenu.value = false
  // 重置所有標籤狀態
  showProfileLabel.value = false
  showJobsLabel.value = false
  showDashboardLabel.value = false
  showCommunityLabel.value = false
}

function goToHome() {
  // 如果選單已經顯示，直接導航到 Home 頁面
  // 先清除計時器和關閉選單，然後跳轉
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
  showHomeMenu.value = false
  router.push('/home')
}

function goToChat() {
  hideMenu()
  router.push('/chat')
}

function goToNews() {
  hideMenu()
  router.push('/news')
}

function goToPage(path: string) {
  hideMenu()
  router.push(path)
}

// 監聽路由變化，關閉選單
watch(route, () => {
  hideMenu()
})
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
  max-width: 240px; /* 確保最大寬度 */
  max-height: 320px; /* 確保最大高度 */
}

.main-content {
  flex: 1;
  overflow-y: auto;
  font-size: 14px;
  transition: opacity 0.3s ease; /* 添加淡化過渡效果 */
}

/* 當 Home 選單展開時，淡化主內容 */
.app-container:has(.home-menu-overlay) .main-content {
  opacity: 0.3; /* 淡化主內容到 30% 透明度 */
}

/* 底部導航欄 */
.bottom-nav {
  position: relative;
  height: 45px; /* 從 60px 降低到 45px */
  background: rgb(42, 65, 102); /* 改為藍色背景 */
  border-top: 1px solid #e0e0e0;
  z-index: 1001; /* 設置導航欄層級 */
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
  color: rgba(255, 255, 255, 0.7); /* 預設半透明白色 */
}

.nav-item.home-item {
  background: transparent; /* 改為透明背景，與其他按鈕一致 */
  border-radius: 0; /* 移除圓形設計 */
  width: auto; /* 改為自動寬度 */
  height: auto; /* 改為自動高度 */
  color: rgba(255, 255, 255, 0.7); /* 使用與其他按鈕相同的半透明白色 */
  margin-top: 0; /* 移除負邊距，讓它與其他按鈕對齊 */
  box-shadow: none; /* 移除陰影 */
  z-index: 1001;
  position: relative;
  padding: 8px 12px; /* 與其他按鈕使用相同的內邊距 */
}

.nav-item.home-item .material-icons-round {
  color: rgba(255, 255, 255, 0.7) !important; /* 使用與其他按鈕相同的半透明白色 */
}

.nav-item.home-item .nav-label {
  color: white !important; /* 標籤保持白色 */
}

.nav-item.home-item.active {
  color: white; /* 被選中時變為白色 */
}

.nav-item.home-item.active .material-icons-round {
  color: white !important; /* 被選中時圖示變為白色 */
}

.nav-item.active {
  color: white; /* 被選中的按鈕變白色 */
}

.nav-item .material-icons-round {
  font-size: 20px; /* 從 24px 調整為 20px */
  margin-bottom: 2px;
}

.nav-label {
  font-size: 9px;
  font-weight: 500;
  white-space: nowrap;
  color: white; /* 標籤文字白色 */
  animation: labelFadeIn 0.2s ease-in-out;
}

/* Home展開選單 - 圓弧形浮動選單 */
.home-menu-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  pointer-events: none;
  z-index: 1000;
}

.circular-menu {
  position: absolute;
  bottom: 0px; /* 距離底部導航欄的距離 */
  width: 200px;
  height: 130px;
  left: 50%;
  transform: translateX(-50%);
  pointer-events: auto; /* 恢復選單的鼠標事件 */ 
  z-index: 1002; /* 確保在導航欄之上 */
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
  z-index: 1003; /* 確保選單項目在最上層 */
  opacity: 0;
  transform: scale(0);
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

/* 為 Jobs 和 Dashboard 調整圖示間距 */
.item-2 .material-icons-round,
.item-3 .material-icons-round {
  margin-bottom: 0;
  margin-top: 2px;
}

.menu-item:hover .material-icons-round {
  color: white;
}

/* 懸浮狀態下 Jobs 和 Dashboard 的圖示間距 */
.item-2:hover .material-icons-round,
.item-3:hover .material-icons-round {
  margin-bottom: 0;
  margin-top: 2px;
}

.item-label {
  font-size: 6px;
  font-weight: 600;
  color: rgb(42, 65, 102);
  white-space: nowrap;
  animation: labelFadeIn 0.2s ease-in-out;
}

.menu-item:hover .item-label {
  color: white;
  animation: labelFadeIn 0.2s ease-in-out;
}

/* 圓弧形排列 - 沿著半圓弧均勻分布四個選項 */
/* 使用圓弧數學計算：半徑80px，角度從-135°到-45°均勻分布 */
.item-1 {
  bottom: 5px;   /* Profile - 左下角，提高位置避免與導航欄重疊 */
  left: 15px;
  animation: menuItemAppear 0.4s ease-out 0.1s forwards;
}

.item-2 {
  bottom: 37px;   /* Jobs - 左上角 */
  left: 51px;
  animation: menuItemAppear 0.4s ease-out 0.2s forwards;
}

.item-3 {
  bottom: 37px;   /* Dashboard - 右上角 */
  right: 51px;
  animation: menuItemAppear 0.4s ease-out 0.3s forwards;
}

.item-4 {
  bottom: 5px;   /* Community - 右下角，提高位置避免與導航欄重疊 */
  right: 15px;
  animation: menuItemAppear 0.4s ease-out 0.4s forwards;
}

@keyframes labelFadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes menuItemAppear {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
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
