<template>
  <main>
    <div class="filters">
      <input
        type="text"
        placeholder="Search jobs..."
        class="search-box"
      />
      <select class="filter-select">
        <option value="">Filter by status</option>
        <option value="draft">Draft</option>
        <option value="active">Active</option>
        <option value="closed">Closed</option>
      </select>
    </div>
    
    <!-- Loading 狀態 -->
    <div v-if="loading" class="loading">Loading jobs...</div>
    
    <!-- 錯誤狀態 -->
    <div v-if="error" class="error">{{ error }}</div>
    
    <!-- 工作列表 -->
    <ul v-if="!loading && !error" class="job-list">
      <li v-for="job in jobs" :key="job.id">
        <button class="job-btn" @click="goJob(job.id)">
          <div class="job-header">
            <span class="job-type" :class="`status-${job.status}`">{{ job.status }}</span>
          </div>
          <div class="job-info">
            <p>
              <strong>{{ job.title }}</strong><br />
              {{ job.description }}<br />
              <small>Reward: {{ job.reward }} | People: {{ job.required_people }}</small>
            </p>
          </div>
        </button>
      </li>
    </ul>
    
    <!-- 空狀態 -->
    <div v-if="!loading && !error && jobs.length === 0" class="empty">
      No jobs found
    </div>
    
    <button class="create-btn" @click="goToCreate">
      +
    </button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getAuthHeaders } from '../services/auth'

// API 基礎 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 狀態管理
const jobs = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const router = useRouter()
const route = useRoute()

// 定義 Job 型別（基於 API 規格）
interface Job {
  id: string
  employer_id: string
  title: string
  description: string
  reward: string
  work_type: 'short' | 'long' | 'project'
  required_people: number
  start_date: string
  status: 'draft' | 'active' | 'closed'
  location_id: string
  address: string
  end_date: string
  pictures: string[]
  created_at: string
  updated_at: string
}

// 獲取工作列表
async function fetchJobs(skip: number = 0, limit: number = 10) {
  loading.value = true
  error.value = ''
  
  try {
    console.log('📤 Fetching jobs from API...')
    
    const url = `${API_BASE_URL}/api/v1/jobs/?skip=${skip}&limit=${limit}`
    console.log('🌐 API URL:', url)
    
    const response = await fetch(url, {
      method: 'GET',
      headers: getAuthHeaders()
    })
    
    console.log('📥 Response received:', response.status, response.statusText)
    console.log('📥 Response headers:', Object.fromEntries(response.headers.entries()))
    
    // 先獲取原始文本
    const responseText = await response.text()
    console.log('📥 Raw response text:', responseText)
    
    if (!response.ok) {
      let errorMessage = 'Failed to fetch jobs'
      try {
        const errorData = JSON.parse(responseText)
        console.error('❌ Error response data:', errorData)
        errorMessage = errorData.detail || errorMessage
      } catch {
        errorMessage = `HTTP ${response.status}: ${response.statusText}`
      }
      throw new Error(errorMessage)
    }
    
    // 解析 JSON
    const data: Job[] = JSON.parse(responseText)
    console.log('✅ Jobs fetched successfully:', data)
    console.log('📊 Number of jobs received:', data.length)
    console.log('🔍 Jobs data structure:', JSON.stringify(data, null, 2))
    
    jobs.value = data
    
  } catch (err: any) {
    console.error('🚨 Fetch jobs error:', err)
    error.value = err.message || 'Failed to fetch jobs'
  } finally {
    loading.value = false
  }
}

// 頁面載入時獲取工作列表
onMounted(() => {
  console.log('📱 JobList component mounted, fetching jobs...')
  fetchJobs()
})

// 監聽路由變化，當從 create 頁面回來時重新獲取數據
watch(() => route.path, (newPath, oldPath) => {
  console.log('🛣️ Route changed from', oldPath, 'to', newPath)
  if (newPath === '/job') {
    console.log('📱 JobList route activated, refetching jobs...')
    fetchJobs()
  }
}, { immediate: false })

// 導航到工作詳情
const goJob = (id: string) => {
  router.push(`/job/${id}`)
}

// 導航到創建工作頁面
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
  justify-content: space-between;
  align-items: center;
  border: none;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
  margin: 3px 0;
  padding: 8px;
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

.job-info p {
  margin: 4px 0;
  line-height: 1.4;
}

.job-info small {
  color: #666;
  font-size: 10px;
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
  flex-shrink: 0;
}

.create-btn:hover {
  background: rgb(255, 170, 0);
}

.job-list {
  list-style-type: none;
  padding-left: 6px;
  margin-right: 6px;
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.job-type {
  margin-top: 8px;
  font-size: 10px;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 12px;
  text-transform: uppercase;
}

/* Status 相關的樣式 */
.status-draft {
  color: #856404;
  background: #fff3cd;
}

.status-active {
  color: #155724;
  background: #d4edda;
}

.status-closed {
  color: #721c24;
  background: #f8d7da;
}

/* 狀態訊息樣式 */
.loading {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
}

.error {
  text-align: center;
  padding: 20px;
  color: #721c24;
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  margin: 8px;
  font-size: 12px;
}

.empty {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
}
</style>
