<template>
  <main v-if="application" class="application-detail">
    <h1 class="title">Application Detail</h1>

    <div class="description">
      <button class="applicant-btn" @click="goApplicantProfile">
        User {{ application.applicant_id }}
      </button>
    </div>
    <div class="description">
      <button class="applicant-btn" @click="goJobDetail">
        Job {{ application.job_id }}
      </button>
    </div>
    <div class="description">
      <button class="status-btn">
        Status {{ application.status }}
      </button>
    </div>
    <p class="description"><strong>Message:</strong></p>
    <div class="message-box">
      {{ application.message }}
    </div>

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

function goApplicantProfile() {
  if (application.value) {
    router.push(`/profile/${application.value.applicant_id}`)
  }
}

function goJobDetail() {
  if (application.value) {
    router.push(`/job/${application.value.job_id}`)
  }
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
  margin-bottom: 15px;
  text-align: center;
}

.description {
  padding-left: 16px;
}

.applicant-btn {
  padding: 4px 10px;
  border: none;
  border-radius: 20px;  /* ✅ 橢圓形 */
  background: rgb(229, 227, 227);
  color: rgb(44, 46, 60);
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
}
.applicant-btn:hover {
  background: rgb(80, 110, 160);
}

.status-btn {
  padding: 4px 10px;
  border: none;
  border-radius: 20px;  /* ✅ 橢圓形 */
  background: rgb(53, 66, 118);
  color: rgb(229, 227, 227);
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
}
.status-btn:hover {
  background: rgb(80, 110, 160);
}

.message-box {
  align-self: center;
  padding: 10px;
  width: 80%;
  border: none;
  border-radius: 5px;  /* ✅ 橢圓形 */
  color: #161620;
  background-color: #e5e5e5;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
}

/* Approve 按鈕 */
.approve-btn {
  margin-top: 12px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: rgb(103, 157, 103);
  color: rgb(255, 255, 255);
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