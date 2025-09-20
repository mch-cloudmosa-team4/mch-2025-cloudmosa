<template>
  <main>
    <h1 class="title">My Applications</h1>
    <ul class="application-list">
      <li v-for="a in myApplications" :key="a.id">
        <button @click="goDetail(a.id)">Application #{{ a.id }} (Job {{ a.job_id }})</button>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserId } from '../services/auth'

const router = useRouter()
const applications = ref([])
const myId = getUserId()

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'applications.json')
  const data = await res.json()
  applications.value = data.applications
})

// 只取 applicant_id = 我的 application
const myApplications = computed(() => applications.value.filter((a) => a.applicant_id === myId))

function goDetail(id) {
  router.push(`/application/${id}`)
}
</script>

<style scoped>
.title {
  font-size: 16px;
  font-weight: bold;
  margin: 12px 0;
  text-align: center;
}

.application-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.application-list button {
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-size: 13px;
  cursor: pointer;
}

.application-list button:hover {
  background: rgb(80, 110, 160);
}
</style>
