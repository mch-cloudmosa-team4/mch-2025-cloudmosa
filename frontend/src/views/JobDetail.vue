<template>
  <main v-if="job" class="job-detail">
    <h1 class="title">{{ job.title }}</h1>

    <button class="applications-btn" @click="goToApplications">
      View Applications
    </button>

    <p class="description"><strong>ID:</strong> {{ job.id }}</p>
    <p class="description"><strong>Employer ID:</strong> {{ job.employer_id }}</p>
    <p class="description"><strong>Description:</strong> {{ job.description }}</p>
    <p class="description"><strong>Reward:</strong> {{ job.reward }}</p>
    <p class="description"><strong>Location:</strong> {{ job.location_id }}</p>
    <p class="description"><strong>Address:</strong> {{ job.address }}</p>
    <p class="description"><strong>Work Type:</strong> {{ job.work_type }}</p>
    <p class="description"><strong>Required People:</strong> {{ job.required_people }}</p>
    <p class="description"><strong>Status:</strong> {{ job.status }}</p>
    <p class="description"><strong>Start Date:</strong> {{ job.start_date }}</p>
    <p class="description"><strong>End Date:</strong> {{ job.end_date }}</p>
    <p class="description"><strong>Created At:</strong> {{ job.created_at }}</p>
    <p class="description"><strong>Updated At:</strong> {{ job.updated_at }}</p>

    <!-- TODO: Do not show this button if employer -->
    <button class="apply-btn" @click="applyJob">
      Apply
    </button>
    <!-- TODO: Show this only if token is authenticated -->
    <button class="edit-btn" @click="goToEdit">
      ✎
    </button>
  </main>
  <main v-else>
    <p>Loading job details...</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const job = ref<any>(null)

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'jobs.json')
  const data = await res.json()
  job.value = data.jobs.find((j: any) => j.id === parseInt(route.params.id as string))
})

function applyJob() {
  router.push(`/job/${job.value.id}/apply`)
}

function goToEdit() {
  router.push(`/job/${job.value.id}/edit`)
}

function goToApplications() {
  router.push(`/job/${job.value.id}/application`)
}
</script>

<style scoped>
.job-detail {
  width: 240px;
  height: 320px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0px;
  font-size: 11px;
  position: relative;
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

/* Applications 按鈕 */
.applications-btn {
  margin: 0 16px 12px 16px;
  padding: 6px 10px;
  border: none;
  border-radius: 6px;
  background: rgb(0, 123, 255);
  color: white;
  font-size: 12px;
  cursor: pointer;
  align-self: flex-start;
}
.applications-btn:hover {
  background: rgb(0, 100, 210);
}

.edit-btn {
  position: sticky;
  bottom: 10px;
  left: 175px;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgb(255, 193, 7);
  color: black;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
  flex-shrink: 0;       /* ⭐ 避免被 flex 壓扁 */
}
.edit-btn:hover {
  background: rgb(255, 170, 0);
}
</style>