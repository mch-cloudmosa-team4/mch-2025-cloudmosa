<template>
  <main class="settings">
    <div class="settings-header">
      <button class="back-btn" @click="goBack">←</button>
      <h1 class="title">Settings</h1>
    </div>
    
    <div class="settings-section">
      <h3>Account</h3>
      <button class="setting-item" @click="$router.push('/profile/' + getUserId())">
        <span class="material-icons-round">person</span>
        <span>Profile Settings</span>
      </button>
    </div>
    
    <div class="settings-section">
      <h3>Preferences</h3>
      <button class="setting-item">
        <span class="material-icons-round">notifications</span>
        <span>Notification Settings</span>
      </button>
      <button class="setting-item">
        <span class="material-icons-round">security</span>
        <span>Privacy & Security</span>
      </button>
    </div>
    
    <div class="settings-section">
      <h3>Support</h3>
      <button class="setting-item">
        <span class="material-icons-round">help</span>
        <span>Help & Support</span>
      </button>
      <button class="setting-item">
        <span class="material-icons-round">info</span>
        <span>About</span>
      </button>
    </div>
    
    <button class="logout-btn" @click="handleLogout">
      <span class="material-icons-round">logout</span>
      <span>Logout</span>
    </button>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout } from '../services/auth'
import { getUserId } from '../services/auth'

const router = useRouter()

function handleLogout() {
  logout()
  router.replace('/login')
}

function goBack() {
  router.go(-1)
}
</script>

<style scoped>
.settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 240px;
  margin: 0 auto;
  padding: 8px;
}

.settings-header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 8px;
}

.back-btn {
  position: absolute;
  left: 0;
  background: none;
  border: none;
  font-size: 16px;
  color: rgb(42, 65, 102);
  cursor: pointer;
  padding: 4px 8px;
}

.back-btn:hover {
  background: rgba(42, 65, 102, 0.1);
  border-radius: 4px;
}

.title {
  font-size: 18px;
  margin: 0;
  color: rgb(42, 65, 102);
}

.settings-section {
  margin-bottom: 8px;
}

.settings-section h3 {
  font-size: 12px;
  color: #666;
  margin: 0 0 8px 8px;
  text-transform: uppercase;
  font-weight: 600;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px;
  border: none;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 4px;
  font-size: 14px;
  text-align: left;
  transition: background-color 0.2s ease;
}

.setting-item:hover {
  background: #f5f5f5;
}

.setting-item .material-icons-round {
  font-size: 20px;
  color: rgb(42, 65, 102);
}

.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 90%;
  align-self: center;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: #e74c3c;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 16px;
  transition: background-color 0.2s ease;
}

.logout-btn:hover {
  background: #c0392b;
}

.logout-btn .material-icons-round {
  font-size: 20px;
}
</style>
