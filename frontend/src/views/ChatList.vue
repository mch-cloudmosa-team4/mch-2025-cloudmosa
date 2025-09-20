<template>
  <main class="chat-list">
    <h1 class="title">Messages</h1>
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
</script>

<style scoped>
.chat-list {
  padding: 12px;
  font-family: Roboto, sans-serif;
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
</style>
