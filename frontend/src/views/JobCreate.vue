<template>
  <main class="job-create">
    <h1 class="title">Create Job</h1>

    <form @submit.prevent="createJob" class="form">
      <div class="field">
        <label>Title:</label>
        <input v-model="form.title" type="text" />
      </div>

      <div class="field">
        <label>Description:</label>
        <textarea v-model="form.description" rows="3"></textarea>
      </div>

      <div class="field">
        <label>Reward:</label>
        <input v-model="form.reward" type="text" placeholder="e.g., $500" />
      </div>

      <div class="field">
        <label>Work Type:</label>
        <select v-model="form.work_type">
          <option disabled value="">Select work type</option>
          <option value="short">Short-term</option>
          <option value="long">Long-term</option>
          <option value="project">Project-based</option>
        </select>
      </div>

      <div class="field">
        <label>Required People:</label>
        <input v-model.number="form.required_people" type="number" min="1" />
      </div>

      <div class="field">
        <label>Status:</label>
        <select v-model="form.status">
          <option disabled value="">Select status</option>
          <option value="draft">Draft</option>
          <option value="active">Active</option>
          <option value="closed">Closed</option>
        </select>
      </div>

      <div class="field">
        <label>Location ID:</label>
        <input v-model="form.location_id" type="text" placeholder="Location identifier" />
      </div>

      <div class="field">
        <label>Address:</label>
        <input v-model="form.address" type="text" placeholder="Full address" />
      </div>

      <div class="field">
        <label>Start Date:</label>
        <input v-model="form.start_date" type="datetime-local" />
      </div>

      <div class="field">
        <label>End Date:</label>
        <input v-model="form.end_date" type="datetime-local" />
      </div>

      <div class="field">
        <label>Pictures (URLs):</label>
        <div v-for="(picture, index) in form.pictures" :key="index" class="picture-input">
          <input 
            v-model="form.pictures[index]" 
            type="url" 
            placeholder="https://example.com/image.jpg"
          />
          <button type="button" @click="removePicture(index)" class="remove-btn">×</button>
        </div>
        <button type="button" @click="addPicture" class="add-btn">Add Picture</button>
      </div>

      <!-- 提交按鈕 -->
      <button type="submit" class="save-btn" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Job' }}
      </button>
    </form>

    <!-- 錯誤訊息 -->
    <div v-if="error" class="error">{{ error }}</div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { getAuthHeaders, getUserUUID } from '../services/auth'

const router = useRouter()

// API 基礎 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 表單狀態
const loading = ref(false)
const error = ref('')

// 表單資料
const form = ref({
  title: '',
  description: '',
  reward: '',
  work_type: 'short', // 預設值
  required_people: 1,
  status: 'draft', // 預設值
  location_id: '',
  address: '',
  start_date: '',
  end_date: '',
  pictures: [''] // 初始化一個空的圖片 URL 輸入框
})

// 添加圖片 URL 輸入框
function addPicture() {
  form.value.pictures.push('')
}

// 移除圖片 URL 輸入框
function removePicture(index: number) {
  if (form.value.pictures.length > 1) {
    form.value.pictures.splice(index, 1)
  }
}

// 創建工作
async function createJob() {
  console.log('🚀 createJob function called!')
  
  if (loading.value) return
  
  error.value = ''
  loading.value = true
  
  try {
    // 獲取當前用戶 ID 作為 employer_id
    const employerId = getUserUUID()
    if (!employerId) {
      throw new Error('User not authenticated')
    }
    
    // 準備 API 請求資料
    const requestData = {
      employer_id: employerId,
      title: form.value.title,
      description: form.value.description,
      reward: form.value.reward,
      work_type: form.value.work_type,
      required_people: form.value.required_people,
      status: form.value.status,
      // location_id: form.value.location_id,
      address: form.value.address,
      start_date: new Date(form.value.start_date).toISOString(),
      end_date: new Date(form.value.end_date).toISOString(),
      // pictures: form.value.pictures.filter(url => url.trim() !== '') // 過濾空的 URL
    }
    
    console.log('📤 Creating job with data:', requestData)
    console.log('🔑 Auth headers:', getAuthHeaders())
    console.log('🌐 API URL:', `${API_BASE_URL}/api/v1/jobs/`)
    
    // 先測試一個簡單的 GET 請求看看 CORS 是否真的有問題
    try {
      const testResponse = await fetch(`${API_BASE_URL}/api/v1/health`, {
        method: 'GET',
        mode: 'cors'
      })
      console.log('✅ Health check response:', testResponse.status)
    } catch (testError) {
      console.error('❌ Health check failed:', testError)
    }
    
    // 發送 API 請求
    const response = await fetch(`${API_BASE_URL}/api/v1/jobs/`, {
      method: 'POST',
      mode: 'cors',
      headers: getAuthHeaders(),
      body: JSON.stringify(requestData)
    })
    
    console.log('📥 Response received:', response.status, response.statusText)
    console.log('📥 Response headers:', response.headers)
    
    if (!response.ok) {
      let errorMessage = 'Failed to create job'
      try {
        const errorData = await response.json()
        console.error('❌ Error response data:', errorData)
        errorMessage = errorData.detail || `HTTP ${response.status}: ${response.statusText}`
      } catch (parseError) {
        console.error('❌ Failed to parse error response:', parseError)
        errorMessage = `HTTP ${response.status}: ${response.statusText}`
      }
      throw new Error(errorMessage)
    }
    
    const result = await response.json()
    console.log('✅ Job created successfully:', result)
    
    // 成功後導回工作列表頁面
    router.push('/job')
    
  } catch (err: any) {
    console.error('🚨 Create job error:', err)
    console.error('🚨 Error type:', typeof err)
    console.error('🚨 Error name:', err.name)
    console.error('🚨 Error message:', err.message)
    console.error('🚨 Error stack:', err.stack)
    
    // 更詳細的錯誤訊息
    if (err.name === 'TypeError' && err.message.includes('Load failed')) {
      error.value = 'Network error: Unable to connect to server. Please check if the backend is running and CORS is properly configured.'
    } else if (err.message.includes('No authentication token')) {
      error.value = 'Please log in first to create a job.'
    } else {
      error.value = err.message || 'Failed to create job'
    }
  } finally {
    loading.value = false
  }
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
  font-size: 12px;
}

textarea {
  resize: vertical;
  min-height: 60px;
}

.picture-input {
  display: flex;
  gap: 8px;
  align-items: center;
}

.picture-input input {
  flex: 1;
}

.remove-btn {
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  background: #cc0000;
}

.add-btn {
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
  font-size: 11px;
  margin-top: 4px;
}

.add-btn:hover {
  background: #218838;
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

.save-btn:hover:not(:disabled) {
  background: rgb(80, 110, 160);
}

.save-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error {
  background: #ffebee;
  color: #c62828;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ef5350;
  margin-top: 12px;
  font-size: 11px;
  width: 90%;
}
</style>