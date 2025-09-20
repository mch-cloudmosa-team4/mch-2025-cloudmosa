<template>
  <main class="screen">
    <h1 class="title">Welcome</h1>
    <p class="subtitle">Hi, {{ name }} 👋</p>
    <button class="btn" @click="goLogout" :autofocus="true">Logout (Enter)</button>
    <button class="btn" @click="goProfiles">Profiles</button>
    <button class="btn" @click="goJobs">Jobs</button>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { logout, isAuthed } from '../services/auth'

const router = useRouter()
const name = localStorage.getItem('auth_name') || 'Guest'

if (!isAuthed()) router.replace('/login')

function goLogout() {
  logout()
  router.replace('/login')
}

function goProfiles() {
  router.replace('/profile')
}

function goJobs() {
  router.replace('/job')
}
</script>

<style scoped>
.screen {
  width: 240px;
  height: 320px;
  background: #fdfdfd;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;
}

.title {
  font-size: 18px;
  margin: 8px 0 4px;
  color: #222;
  text-align: center;
}

.subtitle {
  font-size: 13px;
  color: #555;
  margin-bottom: 16px;
}

.btn {
  width: 80%;
  padding: 8px;
  margin: 6px 0;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  background: rgb(86, 106, 138); /* 主色 */
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.btn:hover,
.btn:focus {
  background: rgb(170, 192, 233);
}
</style>
