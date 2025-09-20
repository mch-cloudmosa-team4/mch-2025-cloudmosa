<template>
  <main class="notification-view">
    <div class="top-bar">
      <button class="back-btn" @click="$router.push('/home')">←</button>
      <h1 class="title">News</h1>
    </div>
    
    <div class="notification-list">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="['notification-item', { 'read': notification.isRead }]"
        @click="markAsRead(notification.id)"
      >
        <div class="notification-header">
          <span class="notification-type">{{ notification.type }}</span>
          <span class="notification-time">{{ formatTime(notification.createdAt) }}</span>
        </div>
        <h3 class="notification-title">{{ notification.title }}</h3>
        <p class="notification-message">{{ notification.message }}</p>
        <div v-if="!notification.isRead" class="unread-indicator"></div>
      </div>
    </div>

    <div v-if="notifications.length === 0" class="empty-state">
      <p>No news yet</p>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Notification {
  id: number
  type: string
  title: string
  message: string
  createdAt: string
  isRead: boolean
}

const notifications = ref<Notification[]>([])

onMounted(() => {
  // 模擬通知資料
  notifications.value = [
    {
      id: 1,
      type: 'Job',
      title: 'New Job Opportunity',
      message: 'A new software engineer position has been posted that matches your profile.',
      createdAt: '2025-01-20T10:00:00Z',
      isRead: false
    },
    {
      id: 2,
      type: 'Application',
      title: 'Application Status Update',
      message: 'Your application for Frontend Developer has been reviewed.',
      createdAt: '2025-01-19T15:30:00Z',
      isRead: false
    },
    {
      id: 3,
      type: 'Message',
      title: 'New Message',
      message: 'You have received a new message from John Doe.',
      createdAt: '2025-01-19T09:15:00Z',
      isRead: true
    },
    {
      id: 4,
      type: 'System',
      title: 'Profile Updated',
      message: 'Your profile has been successfully updated.',
      createdAt: '2025-01-18T14:20:00Z',
      isRead: true
    }
  ]
})

function markAsRead(notificationId: number) {
  const notification = notifications.value.find(n => n.id === notificationId)
  if (notification && !notification.isRead) {
    notification.isRead = true
  }
}

function formatTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
  
  if (diffInHours < 1) {
    return 'Just now'
  } else if (diffInHours < 24) {
    return `${diffInHours}h ago`
  } else {
    const diffInDays = Math.floor(diffInHours / 24)
    return `${diffInDays}d ago`
  }
}
</script>

<style scoped>
.notification-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 240px;
  margin: 0 auto;
}

.top-bar {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 40px;
  width: 100%;
  background: rgb(42, 65, 102);
  color: white;
  z-index: 10;
}

.back-btn {
  background: none;
  border: none;
  color: white;
  font-size: 14px;
  margin: 7px;
  cursor: pointer;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.title {
  font-size: 14px;
  margin: 0;
  font-weight: bold;
}

.notification-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.notification-item {
  position: relative;
  padding: 12px;
  border-radius: 8px;
  background: white;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-item:hover {
  background: #f5f5f5;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.notification-item.read {
  opacity: 0.6;
  background: #f8f8f8;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.notification-type {
  font-size: 10px;
  font-weight: bold;
  color: rgb(42, 65, 102);
  background: rgba(42, 65, 102, 0.1);
  padding: 2px 6px;
  border-radius: 12px;
}

.notification-time {
  font-size: 9px;
  color: #666;
}

.notification-title {
  font-size: 12px;
  font-weight: bold;
  margin: 0 0 4px 0;
  color: #333;
  line-height: 1.3;
}

.notification-message {
  font-size: 11px;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

.unread-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #e74c3c;
  border-radius: 50%;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #666;
  font-size: 12px;
}

/* 已讀通知的降低飽和度效果 */
.notification-item.read .notification-title {
  color: #888;
}

.notification-item.read .notification-message {
  color: #aaa;
}

.notification-item.read .notification-type {
  color: #888;
  background: rgba(136, 136, 136, 0.1);
}
</style>