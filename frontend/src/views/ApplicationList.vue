<template>
  <main>
    <ul class="job-list">
      <li v-for="a in myApplications" :key="a.id">
        <button class="job-btn" @click="goDetail(a.id)">
          <div class="application-header">
            <span class="application-type">{{ getStatusText(a.status) }}</span>
          </div>
          <div class="job-info">
            <p>
              <strong>Application #{{ a.id }}</strong><br />Job {{ a.job_id }}
              <br><small>{{ formatDate(a.created_at) }}</small>
            </p>
          </div>
        </button>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserId, getAuthToken } from '../services/auth'
import { getMyApplications, getStatusText, formatDate } from '../services/applications'

const router = useRouter()
const applications = ref([])
const myId = getUserId()

onMounted(async () => {
  try {
    const token = getAuthToken()
    if (!token) {
      throw new Error('No authentication token found')
    }
    
    const data = await getMyApplications(token, { limit: 100 })
    applications.value = data
  } catch (error) {
    console.error('❌ Error fetching applications:', error)
    applications.value = []
    // 可以添加用戶友好的錯誤提示
    alert('無法載入申請列表，請檢查網路連線或重新登入')
  }
})

// API already returns only current user's applications
const myApplications = computed(() => applications.value)

function goDetail(id) {
  router.push(`/application/${id}`)
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

.job-list {
  list-style-type: none;
  padding-left: 6px;
  margin-right: 6px;
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.application-type {
  font-size: 10px;
  font-weight: bold;
  color: rgb(42, 65, 102);
  background: rgba(42, 65, 102, 0.1);
  padding: 2px 6px;
  border-radius: 12px;
}
</style>