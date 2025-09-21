<template>
  <main class="job-create">
    <h1 class="title">Create Job</h1>

    <form @submit.prevent="createJob" class="form">
      <div class="field">
        <label>Title:</label>
        <input v-model="form.title" type="text" required />
      </div>

      <div class="field">
        <label>Description:</label>
        <input v-model="form.description" type="text" required />
      </div>

      <div class="field">
        <label>Reward:</label>
        <input v-model="form.reward" type="text" required />
      </div>

      <div class="field">
        <label>Location ID:</label>
        <input v-model.number="form.location_id" type="number" required />
      </div>

      <div class="field">
        <label>Address:</label>
        <input v-model="form.address" type="text" required />
      </div>

      <div class="field">
        <label>Work Type:</label>
        <select v-model.number="form.work_type" required>
          <option disabled value="">Select one</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>
      </div>

      <div class="field">
        <label>Required People:</label>
        <input v-model.number="form.required_people" type="number" required />
      </div>

      <div class="field">
        <label>Status:</label>
        <select v-model.number="form.status" required>
          <option disabled value="">Select one</option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
        </select>
      </div>

      <div class="field">
        <label>Start Date:</label>
        <input v-model="form.start_date" type="date" required />
      </div>

      <div class="field">
        <label>End Date:</label>
        <input v-model="form.end_date" type="date" required />
      </div>

      <!-- 儲存 -->
      <button type="submit" class="save-btn">Create</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref<any>({
  title: '',
  description: '',
  reward: '',
  location_id: null,
  address: '',
  work_type: null,
  required_people: null,
  status: null,
  start_date: '',
  end_date: ''
})

function createJob() {
  // TODO: call API to create job
  alert('Job created:\n' + JSON.stringify(form.value, null, 2))
  router.push('/jobs') // 建立完成後導回 jobs 頁面
}
</script>

<style scoped>
.job-create {
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