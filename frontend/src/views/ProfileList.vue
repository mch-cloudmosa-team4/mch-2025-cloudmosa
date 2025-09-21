<template>
  <main>
    <h1>Profiles</h1>
    <div class="filters">
      <input
        type="text"
        placeholder="Search people..."
        class="search-box"
      />
    </div>
    <button @click="goMe()">Go to My Profile</button>
    <ul>
      <li v-for="p in profiles" :key="p.id">
        <button @click="goDetail(p.id)">
          {{ p.displayName }}
        </button>
      </li>
    </ul>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getUserId } from '../services/auth'
import { getProfiles } from '../services/profiles'

const profiles = ref([])
const search = ref('')
const router = useRouter()

onMounted(async () => {
  // const res = await fetch(import.meta.env.BASE_URL + 'profiles.json')
  // const data = await res.json()
  // profiles.value = data.profiles
  try {
    const token = localStorage.getItem('auth_token')
    console.log("Auth token", token)
    // TODO: Get all profiles
    const res = await getProfiles(token, [1, 2, 3])
    profiles.value = res.profiles
  } catch (err) {
    console.error('Failed to fetch profiles:', err)
  }
})

function goDetail(id: any) {
  router.push(`/profile/${id}`)
}

function goMe() {
  console.log('Going to my profile:', getUserId())
  router.push(`/profile/${getUserId()}`)
}

const filteredProfiles = computed(() => {
  if (!search.value) return profiles.value
  return profiles.value.filter((p) =>
    p.display_name.toLowerCase().includes(search.value.toLowerCase())
  )
})
</script>
<style scoped>
main {
  max-width: 420px;
  margin: 0 auto;
  padding: 16px;
  font-family: "Helvetica Neue", Arial, sans-serif;
  background: #ffffff;
}

/* 標題 */
h1 {
  font-size: 14px;
  font-weight: 700;
  text-align: center;
  color: #2a4166;
}

/* 搜尋列區塊 */
.filters {
  position: sticky;
  top: 0;
  background: #fff;
  padding: 8px 0;
  z-index: 10;
}

.search-box {
  padding: 10px 14px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 14px;
  width: 80%;
  transition: all 0.2s ease;
}

.search-box:focus {
  border-color: #2a4166;
  outline: none;
  box-shadow: 0 0 5px rgba(42, 65, 102, 0.3);
}

/* 全域按鈕樣式 */
button {
  padding: 10px 14px;
  font-size: 14px;
  border: none;
  border-radius: 25px;
  color: rgb(44, 52, 70);
  background-color: white;
  cursor: pointer;
  transition: transform 0.1s ease;
}

button:hover {
  background: rgb(80, 110, 160);
  transform: scale(1.02);
}

/* 「我的 Profile」按鈕 */
main > button {
  display: block;
  margin: 10px auto;
  font-weight: 600;
  background: white;  /* 改成白色背景 */
  color: #2a4166;     /* 深藍字色，避免跟背景同色 */
  border: 1px solid #ccc; /* 給邊框讓它不會看起來消失 */
  border-width: 1.5px;
  border-color: #2a4166;
}

main > button:hover {
  background: #2a4166; /* hover 時變成深藍 */
  color: white;        /* 文字改成白色 */
}

/* Profile 列表 */
ul {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 每一個 Profile 卡片 */
li button {
  width: 100%;
  text-align: left;
  background: #f9f9f9;
  color: #222;
  font-size: 15px;
  font-weight: 500;
  padding: 14px 16px;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
}

li button:hover {
  background: #eef3fb;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(42, 65, 102, 0.15);
}

/* Back to Home 按鈕 */
main > button:last-of-type {
  margin-top: 20px;
  width: 100%;
}

</style>