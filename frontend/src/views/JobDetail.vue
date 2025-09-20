<template>
  <main v-if="job" class="job-detail">
    <h1 class="title">{{ job.title }}</h1>
    <p class="description"><strong>ID:</strong> {{ job.id }}</p>
    <p class="description"><strong>Employer ID:</strong> {{ job.employer_id }}</p>
    <p class="description"><strong>Description:</strong> {{ job.description }}</p>
    <p class="description"><strong>Reward:</strong> {{ job.reward }}</p>
    <p class="description"><strong>Location:</strong> {{ job.addredd }}</p>
    <p class="description"><strong>Work Type:</strong> {{ job.work_type }}</p>
    <p class="description"><strong>Required People:</strong> {{ job.required_people }}</p>
    <p class="description"><strong>Status:</strong> {{ job.status }}</p>
    <p class="description"><strong>Start Date:</strong> {{ job.start_date }}</p>
    <p class="description"><strong>End Date:</strong> {{ job.end_date }}</p>
    <p class="description"><strong>Created At:</strong> {{ job.created_at }}</p>
    <p class="description"><strong>Updated At:</strong> {{ job.updated_at }}</p>

    <!-- TODO: Do not show this button if employer -->
    <button class="apply-btn" @click="applyJob">
      <!-- TODO: For applicant, add query for current status -->
      Apply
    </button>
    <!-- TODO: For employer, show all the applcations -->
  </main>
  <main v-else>
    <p>Loading job details...</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const job = ref(null)

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'jobs.json')
  const data = await res.json()
  job.value = data.jobs.find((j) => j.id === parseInt(route.params.id))
})

function applyJob() {
  alert('Application submitted for job: ' + job.value.title)
}
</script>

<style scoped>
.job-detail {
  width: 240px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0px;
  font-size: 11px;
  padding-bottom: 16px;
}

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 16px;
}

.description {
  padding-left: 16px;
}

.apply-btn {
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
.apply-btn:hover {
  background: rgb(80, 110, 160);
}
</style>
