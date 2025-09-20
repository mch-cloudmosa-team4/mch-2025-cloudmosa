<template>
  <main v-if="job" class="job-edit">
    <h1 class="title">Edit Job (ID: {{ job.id }})</h1>

    <form @submit.prevent="saveJob" class="form">
      <!-- 不可編輯欄位 -->
      <div class="field"><label>Employer ID:</label> <span>{{ job.employer_id }}</span></div>
      <div class="field"><label>Created At:</label> <span>{{ job.created_at }}</span></div>
      <div class="field"><label>Updated At:</label> <span>{{ job.updated_at }}</span></div>

      <!-- 可編輯欄位 -->
      <div class="field">
        <label>Title:</label>
        <input v-model="form.title" type="text" />
      </div>

      <div class="field">
        <label>Description:</label>
        <input v-model="form.description" type="text" />
      </div>

      <div class="field">
        <label>Reward:</label>
        <input v-model="form.reward" type="text" />
      </div>

      <div class="field">
        <label>Location ID:</label>
        <input v-model.number="form.location_id" type="number" />
      </div>

      <div class="field">
        <label>Address:</label>
        <input v-model="form.address" type="text" />
      </div>

      <div class="field">
        <label>Work Type:</label>
        <select v-model.number="form.work_type">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>
      </div>

      <div class="field">
        <label>Required People:</label>
        <input v-model.number="form.required_people" type="number" />
      </div>

      <div class="field">
        <label>Status:</label>
        <select v-model.number="form.status">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>
      </div>

      <div class="field">
        <label>Start Date:</label>
        <input v-model="form.start_date" type="date" />
      </div>

      <div class="field">
        <label>End Date:</label>
        <input v-model="form.end_date" type="date" />
      </div>

      <!-- 儲存 -->
      <button type="submit" class="save-btn">Save</button>
    </form>
  </main>

  <main v-else>
    <p>Loading job...</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const job = ref<any>(null)
const form = ref<any>({})

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'jobs.json')
  const data = await res.json()
  job.value = data.jobs.find((j: any) => j.id === parseInt(route.params.id as string))

  if (job.value) {
    // Copy job data to form for editing
    form.value = { ...job.value }
  }
})

function saveJob() {
  // TODO: call API to save job
  alert('Job updated:\n' + JSON.stringify(form.value, null, 2))
  router.push(`/job/${job.value.id}`)
}
</script>

<style scoped>
.job-edit {
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  font-size: 12px;
  padding: 16px;
}

.title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  padding: 16px 0;
  width: 80%;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 90%;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 90%;
}

label {
  font-weight: bold;
}

input, select, textarea {
  padding: 6px;
  border: 1px solid #aaa;
  border-radius: 4px;
}

.save-btn {
  margin-top: 16px;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  width: 90%;
}
.save-btn:hover {
  background: rgb(80, 110, 160);
}
</style>