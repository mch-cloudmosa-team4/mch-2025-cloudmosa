<template>
  <main>
    <h1>Jobs</h1>
    <ul>
      <li v-for="j in jobs" :key="j.id">
        <button class="job-btn" @click="goJob(j.id)">
          <div class="job-info">
            <p>
              <strong>{{ j.title }}</strong
              ><br />{{ j.description }}
            </p>
          </div>
        </button>
      </li>
    </ul>
    <button @click="$router.push('/')">Back to Home</button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const jobs = ref([])
const router = useRouter()

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'jobs.json')
  const data = await res.json()
  jobs.value = data.jobs
})

const goJob = (id) => {
  router.push(`/job/${id}`)
}
</script>

<style scoped>
.job-btn {
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

.job-btn:hover,
.job-btn:focus {
  background: #dbe3f5;
}

.job-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
}
</style>
