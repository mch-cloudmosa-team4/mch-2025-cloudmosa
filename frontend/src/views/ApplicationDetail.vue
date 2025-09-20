<template>
  <main v-if="application" class="application-detail">
    <h1 class="title">Application Detail</h1>

    <p class="description"><strong>ID:</strong> {{ application.id }}</p>
    <p class="description"><strong>Applicant ID:</strong> {{ application.applicant_id }}</p>
    <p class="description"><strong>Job ID:</strong> {{ application.job_id }}</p>
    <p class="description"><strong>Message:</strong> {{ application.message }}</p>
    <p class="description"><strong>Status:</strong> {{ application.status }}</p>
    <p class="description"><strong>Created At:</strong> {{ application.created_at }}</p>
    <p class="description"><strong>Updated At:</strong> {{ application.updated_at }}</p>

    <!-- Approve 按鈕 -->
    <button
      v-if="application.applicant_id !== myId"
      class="approve-btn"
      @click="approveApplication"
    >
      Approve Application
    </button>


    <!-- Back 按鈕 -->
    <button class="back-btn" @click="goBack">← Back</button>
  </main>

  <main v-else>
    <p>Loading application details...</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserId} from '../services/auth'

const route = useRoute()
const router = useRouter()
const application = ref(null)
const myId = getUserId()

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'applications.json')
  const data = await res.json()
  application.value = data.applications.find((a) => a.id === parseInt(route.params.id))
})

function goBack() {
  console.log(route.query.from)
  if (route.query.from === 'apply') {
    router.push('/dashboard')
  } else {
    router.back()
  }
}

// Approve -> 建立 conversation (假設 id=1) -> 跳轉 chat
function approveApplication() {
  // TODO: 真實情況應該要呼叫 API 建立 conversation
  const conversationId = 1
  router.push(`/chat/${conversationId}`)
}
</script>

<style scoped>
.application-detail {
  width: 240px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
  padding-bottom: 16px;
}

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  text-align: center;
}

.description {
  padding-left: 16px;
}

/* Approve 按鈕 */
.approve-btn {
  margin-top: 12px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: rgb(103, 157, 103);
  color: white;
  font-weight: bold;
  cursor: pointer;
  width: 80%;
  align-self: center;
}
.approve-btn:hover {
  background: darkgreen;
}

/* Back 按鈕 */
.back-btn {
  margin-top: 8px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  width: 80%;
  align-self: center;
}
.back-btn:hover {
  background: rgb(80, 110, 160);
}
</style>