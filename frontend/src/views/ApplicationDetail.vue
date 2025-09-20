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

    <button class="back-btn" @click="goBack">← Back</button>
  </main>

  <main v-else>
    <p>Loading application details...</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const application = ref(null)

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

.back-btn {
  margin-top: 16px;
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
