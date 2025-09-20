<template>
  <main>
    <div class="filters">
      <input
        type="text"
        placeholder="Search jobs..."
        class="search-box"
      />
      <select class="filter-select">
        <option value="">Filter by skill</option>
        <option value="skill_1">Skill 1</option>
        <option value="skill_2">Skill 2</option>
        <option value="skill_3">Skill 3</option>
      </select>
    </div>
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
    <button class="create-btn" @click="goToCreate">
      +
    </button>
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

function goToCreate() {
  router.push(`/job/create`)
}
</script>

<style scoped>
.filters {
  position: sticky;
  top: 0;
  background: none;
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 10;
}

.search-box {
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 50px;
  font-size: 13px;
  width: 80%;
}

.filter-select {
  width: 85%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 13px;
  background: #f9f9f9;
}

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

.create-btn {
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
.create-btn:hover {
  background: rgb(255, 170, 0);
}
</style>
