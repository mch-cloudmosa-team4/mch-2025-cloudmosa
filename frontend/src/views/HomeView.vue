<template>
  <main class="screen">
    <div class="header">
      <h1 class="title">Welcome</h1>
      <button class="settings-btn" @click="$router.push('/menu')">
        <span class="material-icons-round">settings</span>
      </button>
    </div>
    <p class="subtitle">Hi, {{ name }} 👋</p>
    <button class="btn" @click="goProfiles">Profiles</button>
    <button class="btn" @click="goJobs">Jobs</button>
    <button class="btn" @click="$router.push('/application')">My Applications</button>
    <button class="btn" @click="$router.push('/chat')">Messages</button>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isAuthed } from '../services/auth'

const router = useRouter()
const name = localStorage.getItem('auth_name') || 'Guest'

if (!isAuthed()) router.replace('/login')

function goProfiles() {
  router.push('/profile')
}

function goJobs() {
  router.push('/job')
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

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 8px;
}

.title {
  font-size: 18px;
  margin: 0;
  color: #222;
  flex: 1;
  text-align: center;
}

.settings-btn {
  background: none;
  border: none;
  padding: 4px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.settings-btn:hover {
  background: rgba(42, 65, 102, 0.1);
}

.settings-btn .material-icons-round {
  font-size: 20px;
  color: rgb(42, 65, 102);
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
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn:hover,
.btn:focus {
  background: rgb(80, 110, 160);
}
</style>
