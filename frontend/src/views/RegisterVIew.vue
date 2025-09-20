<template>
  <main class="register">
    <h1 class="title">Register</h1>

    <form @submit.prevent="handleRegister" class="register-form">
      <!-- Name -->
      <label>
        Name
        <input v-model="form.name" type="text" placeholder="Your prefered name" required />
      </label>

      <!-- Email -->
      <label>
        Email
        <input v-model="form.email" type="email" placeholder="example@mail.com" required />
      </label>

      <!-- Phone -->
      <label>
        Phone
        <input v-model="form.phone" type="tel" placeholder="09xx-xxx-xxx" required />
      </label>

      <!-- Password -->
      <label>
        Password
        <input v-model="form.password" type="password" placeholder="******" required />
      </label>

      <!-- Location -->
      <label>
        Location
        <input
          v-model="locationSearch"
          type="text"
          placeholder="Search location..."
          class="search-box"
        />
        <select v-model="form.location" required>
          <option
            v-for="loc in filteredLocations"
            :key="loc.code"
            :value="loc.code"
          >
            {{ loc.name }}
          </option>
        </select>
      </label>

      <button type="submit" class="submit-btn">Register</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// router
const router = useRouter()

// 表單資料
const form = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  location: ''
})

// location 選項（代號 + 名稱）
const locations = ref([
  { code: 'TPE', name: 'Taipei' },
  { code: 'HSC', name: 'Hsinchu' },
  { code: 'TXG', name: 'Taichung' },
  { code: 'TNN', name: 'Tainan' },
  { code: 'KHH', name: 'Kaohsiung' }
])

const locationSearch = ref('')

// 篩選後的地點
const filteredLocations = computed(() =>
  locations.value.filter((loc) =>
    loc.name.toLowerCase().includes(locationSearch.value.toLowerCase())
  )
)

// submit handler
function handleRegister() {
  console.log('Register data:', form.value)
  // 這裡可以改成送出 API 請求
  alert(`Register success! Welcome ${form.value.name}`)
  router.push('/login')
}
</script>

<style scoped>
.register {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
  align-items: center;
}

.title {
  text-align: center;
  margin-bottom: 16px;
  font-size: 18px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 85%;
  margin-left: 16px;
}

.register-form label {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  color: #333;
}

.register-form input,
.register-form select {
  margin-top: 4px;
  padding: 8px;
  font-size: 13px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.search-box {
  margin-top: 4px;
  margin-bottom: 6px;
}

.submit-btn {
  margin-top: 12px;
  margin-bottom: 16px;
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  cursor: pointer;
}

.submit-btn:hover {
  background: rgb(80, 110, 160);
}
</style>