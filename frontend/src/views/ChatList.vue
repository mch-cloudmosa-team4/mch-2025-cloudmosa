<template>
  <main class="chat-list">
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
    <ul>
      <li v-for="c in myConversations" :key="c.id" class="chat-item">
        <button class="chat-btn" @click="goChat(c.id)">
          <div class="chat-info">
            <span class="chat-user">User {{ getOtherUser(c) }}</span>
          </div>
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
  console.log(import.meta.env.BASE_URL)
  const res = await fetch(import.meta.env.BASE_URL + 'conversations.json')
  const data = await res.json()
  conversations.value = data.conversations
  console.log('Loaded conversations: ', conversations.value)
})

const myConversations = computed(() =>
  conversations.value.filter((c) => c.user_1_id === myId || c.user_2_id === myId),
)
console.log('My user ID: ', myId)
console.log('My conversations: ', myConversations.value)

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
}

.title {
  font-size: 18px;
  margin-bottom: 12px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.chat-item {
  margin-bottom: 8px;
}

.chat-btn {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: none;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
}

.chat-btn:hover,
.chat-btn:focus {
  background: #dbe3f5;
}

.chat-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.chat-user {
  font-size: 14px;
  font-weight: bold;
  color: #2a4166;
}

/* TODO: This can serve for last message in future */
.chat-sub {
  font-size: 12px;
  color: #777;
}

.chat-arrow {
  font-size: 18px;
  color: #aaa;
}
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
}

.tab-bar button.active {
  border-bottom: 2px solid rgb(42, 65, 102);
  color: rgb(42, 65, 102);
}

.tab-content {
  flex: 1;
  overflow-y: auto;
}
</style>
