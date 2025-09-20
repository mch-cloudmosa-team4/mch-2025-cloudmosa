<template>
  <main class="job-application">
    <h1 class="title">Applications for Job {{ route.params.id }}</h1>

    <div v-if="applications.length > 0" class="applications-list">
      <button
        v-for="app in applications"
        :key="app.id"
        class="application-btn"
        @click="goToApplication(app.id)"
      >
        <strong>Applicant {{ app.applicant_id }}</strong>
        <p>{{ app.message }}</p>
      </button>
    </div>

    <p v-else>No applications found.</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter , useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()
const applications = ref<any[]>([])

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'applications.json')
  const data = await res.json()
  applications.value = data.applications
})

function goToApplication(id: number) {
  router.push(`/application/${id}`)
}
</script>

<style scoped>
.job-application {
  width: 280px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  font-size: 12px;
  padding: 16px;
}

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 16px;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.application-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 10px;
  border: 1px solid #aaa;
  border-radius: 6px;
  background: #f8f8f8;
  cursor: pointer;
  text-align: left;
}
.application-btn:hover {
  background: #e4e4e4;
}
.application-btn strong {
  font-size: 13px;
}
.application-btn p {
  margin: 0;
  font-size: 12px;
  color: #333;
}
</style>