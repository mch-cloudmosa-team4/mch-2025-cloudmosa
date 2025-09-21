<template>
  <main class="chat-list">
    <!-- 上方 Tab -->
    <div class="tab-bar">
      <button
        :class="{ active: activeTab === 'employer' }"
        @click="activeTab = 'employer'"
      >
        Employer
      </button>
      <button
        :class="{ active: activeTab === 'applicant' }"
        @click="activeTab = 'applicant'"
      >
        Applicant
      </button>
    </div>

    <!-- 聊天室清單 -->
    <ul>
      <li v-for="c in myConversations" :key="c.id" class="chat-item">
        <button class="chat-btn" @click="goChat(c.id)">
          <!-- 頭像 -->
          <img src="/pig.png" alt="avatar" class="chat-avatar" />

          <!-- 使用者資訊 -->
          <div class="chat-info">
            <span class="chat-user">User {{ getOtherUser(c) }}</span>
            <span class="chat-sub">Last message ...</span>
          </div>

          <!-- 箭頭 -->
          <span class="chat-arrow">›</span>
        </button>
      </li>
    </ul>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserId } from '../services/auth'

const router = useRouter()
const conversations = ref([])
const myId = getUserId()

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'conversations.json')
  const data = await res.json()
  conversations.value = data.conversations
})

const myConversations = computed(() =>
  conversations.value.filter((c) => c.user_1_id === myId || c.user_2_id === myId),
)

function goChat(id) {
  router.push(`/chat/${id}`)
}

function getOtherUser(c) {
  return c.user_1_id === myId ? c.user_2_id : c.user_1_id
}

const activeTab = ref<'employer' | 'applicant'>('employer')
</script>

<style scoped>
.chat-list {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

/* Tab Bar */
.tab-bar {
  height: 35px;
  display: flex;
  justify-content: space-around;
  background: #f5f5f5;
  padding: 6px;
  border-bottom: 1px solid #ccc;
}

.tab-bar button {
  flex: 1;
  padding: 10px;
  border: none;
  background: none;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s;
}

.tab-bar button.active {
  border-bottom: 2px solid rgb(42, 65, 102);
  color: rgb(42, 65, 102);
}

/* 聊天室項目 */
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.chat-item {
  margin-bottom: 2px;
}

.chat-btn {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 10px;
  border: none;
  background: #fff;
  cursor: pointer;
  transition: background 0.2s ease;
}

.chat-btn:hover {
  background: #f0f4ff;
}

/* 頭像 */
.chat-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
  border: 1px solid #ddd;
}

/* 使用者資訊 */
.chat-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.chat-user {
  font-size: 15px;
  font-weight: bold;
  color: #2a4166;
}

.chat-sub {
  font-size: 12px;
  color: #777;
  margin-top: 2px;
}

/* 箭頭 */
.chat-arrow {
  font-size: 18px;
  color: #bbb;
  margin-left: auto;
}
</style>