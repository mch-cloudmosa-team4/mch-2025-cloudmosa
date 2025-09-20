<template>
  <main class="menu">
    <h1 class="title">Menu</h1>
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

.title {
  font-size: 18px;
  margin-bottom: 16px;
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
