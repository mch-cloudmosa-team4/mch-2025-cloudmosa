<template>
  <main class="menu">
    <div class="menu-header">
      <button class="back-btn" @click="goBack">←</button>
      <h1 class="title">Menu</h1>
    </div>
    <button class="btn" @click="$router.push('/application')">My Application</button>
    <button class="btn" @click="$router.push('/job')">Find Jobs</button>
    <button class="btn" @click="$router.push('/profile')">Who</button>
    <button class="btn" @click="$router.push('/notification')">Notifications</button>
    <button class="btn logout" @click="handleLogout">Logout</button>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout } from '../services/auth'

const router = useRouter()

function handleLogout() {
  logout()
  router.replace('/login')
}

function goBack() {
  // 使用瀏覽器的回退功能
  router.go(-1)
}
</script>

<style scoped>
.menu {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 240px;
  margin: 0 auto;
  text-align: center;
}

.menu-header {
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
}

.btn {
  padding: 10px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
  width: 80%;
  align-self: center;
}

.btn:hover {
  background: rgb(80, 110, 160);
}

.logout {
  background: #c0392b;
}

.logout:hover {
  background: #e74c3c;
}
</style>
