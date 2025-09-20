<template>
  <main class="screen">
    <div class="header">
      <h1 class="title">Hi, {{ name }} 👋</h1>
      <button class="settings-btn" @click="$router.push('/menu')">
        <span class="material-icons-round">settings</span>
      </button>
    </div>
    <img src="/PIG.gif" alt="fun gif" class="gif" />

    <div class="level-container">
      <span class="level-label">Level {{ level }}</span>
      <div class="level-bar">
        <div class="level-progress" :style="{ width: progress + '%' }"></div>
      </div>
      <span class="level-exp">{{ exp }}/{{ expNeeded }} EXP</span>
    </div>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isAuthed } from '../services/auth'
import { ref } from 'vue'

const router = useRouter()
const name = localStorage.getItem('auth_name') || 'Guest'

// Mock level
const level = ref(3)
const exp = ref(120)          // 當前經驗
const expNeeded = ref(200)    // 升級所需經驗
const progress = ref((exp.value / expNeeded.value) * 100)

if (!isAuthed()) router.replace('/login')

</script>

<style scoped>
.screen {
  width: 240px;
  height: 320px;
  background: #fdfdfd;
  display: flex;
  flex-direction: column;
  align-items: center;
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

.gif {
  width: 80%;
  max-height: 120px;
  object-fit: contain;
  margin-top: 30px;
}

.video {
  width: 80%;
  max-height: 120px;
  object-fit: contain;
  margin: 8px 0;
}

.level-container {
  width: 100%;
  text-align: center;
  margin-top: 16px;
  align-self: center;
  align-items: center;
  flex-direction: column;
}

.level-label {
  font-size: 12px;
  font-weight: bold;
  color: #333;
}

.level-bar {
  width: 80%;
  height: 10px;
  background: #ddd;
  border-radius: 6px;
  margin: 6px 0;
  overflow: hidden;
  align-self: center;
  margin-left: 25px;
}

.level-progress {
  height: 100%;
  background: linear-gradient(to right, #2a4166, #5070a0);
  transition: width 0.3s ease;
}

.level-exp {
  font-size: 11px;
  color: #666;
}
</style>
