<template>
  <main class="chat-room">
    <div class="top-bar">
      <button class="back-btn" @click="$router.push('/chat')">←</button>
      <h1 class="title" @click="goToProfile">
        User {{ otherUserId }}
      </h1>
    </div>
    <div class="chat-box" ref="chatBox">
      <div
        v-for="m in chatMessages"
        :key="m.sent_at"
        class="message-wrapper"
        :class="{ me: m.sender_id === myId }"
      >
        <!-- 訊息框 -->
        <div class="message">
          <p>{{ m.message }}</p>
        </div>
        <!-- 時間放在訊息框下面 -->
        <small class="sent-date">
          {{ new Date(m.sent_at).toLocaleString() }}
        </small>
      </div>
    </div>
    <div class="input-bar">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Type a message..."
        @keyup.enter="sendMessage"
      />
      <button class="send-btn" @click="sendMessage">Send</button>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserId } from '../services/auth'

const route = useRoute()
const router = useRouter()
const myId = getUserId()
const messages = ref([])
const conversations = ref([])
const otherUserId = ref('?')
const newMessage = ref('')
const chatBox = ref(null)

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'messages.json')
  console.log("RES: ", res)
  const data = await res.json()
  messages.value = data.messages

  // load conversation
  const resConv = await fetch(import.meta.env.BASE_URL + 'conversations.json')
  const dataConv = await resConv.json()
  conversations.value = dataConv.conversations

  const conv = conversations.value.find((c) => c.id === parseInt(route.params.id))
  if (conv) {
    otherUserId.value = conv.user_1_id === myId ? conv.user_2_id : conv.user_1_id
  }
  scrollToBottom()
})

const chatMessages = computed(() =>
  messages.value.filter((m) => m.conversation_id === parseInt(route.params.id)),
)

function sendMessage() {
  if (!newMessage.value.trim()) return
  // TODO: Amend to DB
  messages.value.push({
    conversation_id: parseInt(route.params.id),
    sender_id: myId,
    message: newMessage.value,
    sent_at: new Date().toISOString(),
  })
  newMessage.value = ''
  nextTick(() => {
    scrollToBottom()
  })
}

function goToProfile() {
  router.push(`/profile/${otherUserId.value}`)
}

function scrollToBottom() {
  if (chatBox.value) {
    console.log('Scrolling to bottom wioth height: ', chatBox.value.scrollHeight)
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
}
</script>

<style scoped>
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 撐滿畫面 */
}
.chat-box {
  display: flex;
  overflow-y: auto;
  flex-direction: column;
  gap: 8px;
  margin: 12px 0;
  flex: 1;
}
.message-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}
.message {
  margin-left: 5px;
  border-radius: 20px;
  background: #eee;
  align-self: flex-start;
  max-width: 70%;
  font-size: 10px;
  padding: 10px;
  padding-top: 0px;
  padding-bottom: 0px;
}
.message-wrapper.me .message {
  margin-right: 5px;
  background: rgb(130, 157, 201);
  color: white;
  align-self: flex-end;
}
.message small {
  font-size: 7px;
  display: block;
  color: rgb(130, 157, 201);
}
.message-wrapper.me .message small {
  color: white;
  text-align: right;
}
.sent-date {
  font-size: 6px;
  color: #888;
  margin-top: 2px;
  margin-left: 10px;
}

.message-wrapper.me .sent-date {
  text-align: right; /* 自己發的日期靠右 */
  margin-right: 10px;
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
}
.back-btn {
  background: none;
  border: none;
  color: white;
  font-size: 14px;
  margin: 7px;
}
.title {
  font-size: 14px;
  margin: 0;
}
.input-bar {
  position: sticky;
  bottom: 0;
  display: flex;
  padding: 8px;
  border-top: 1px solid #ccc;
  background: #f9f9f9;
}
.input-bar input {
  width: 65%;
  padding: 6px;
  border-radius: 8px;
  border: 1px solid #ccc;
}
.send-btn {
  margin-left: 8px;
  padding: 6px 12px;
  border: none;
  border-radius: 8px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
}
.send-btn:hover {
  background: rgb(80, 110, 160);
}
</style>
