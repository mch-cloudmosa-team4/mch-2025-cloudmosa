<template>
  <main class="application-create">
    <h1>Apply for Job</h1>
    <form @submit.prevent="submitApplication" class="application-form">
      <!-- 顯示 Job ID -->
      <p><strong>Job ID:</strong> {{ jobId }}</p>

      <!-- 填寫 Cover Letter -->
      <label for="coverLetter">Message</label>
      <textarea
        id="coverLetter"
        v-model="coverLetter"
        placeholder="Write your cover letter here..."
        rows="5"
      ></textarea>
      <!-- TODO: (Backend) Check if submitted before -> alert -->
      <button type="submit">Submit Application</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 從 URL 取得 job id
const jobId = route.params.id

// 表單欄位
const coverLetter = ref('')
const expectedSalary = ref('')

// 提交表單
function submitApplication() {
  console.log('Application submitted for job:', jobId)
  console.log('Cover Letter:', coverLetter.value)
  console.log('Expected Salary:', expectedSalary.value)

  // 模擬 API 回傳 application id = 1
  router.push('/application/1')
}
</script>

<style scoped>
.application-create {
  max-width: 420px;
  margin: 0 auto;
  padding: 16px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  background: #ffffff;
}

h1 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 16px;
  text-align: center;
  color: #2a4166;
}

.application-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #2a4166;
}

input,
textarea {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  margin-top: 10px;
  padding: 10px;
  border: none;
  border-radius: 25px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s ease;
}

button:hover {
  background: rgb(80, 110, 160);
}
</style>