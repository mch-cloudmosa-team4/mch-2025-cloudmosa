<template>
  <main class="register">
    <h1 class="title">Register</h1>

    <form @submit.prevent="handleRegister" class="register-form">
      <!-- Name -->
      <label>
        Name
        <input v-model="form.name" type="text" placeholder="Your preferred name" required />
      </label>

      <!-- Email -->
      <label>
        Email
        <input v-model="form.email" type="email" placeholder="example@mail.com" />
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
      <button type="submit" class="submit-btn">Register</button>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../services/auth'

// router
const router = useRouter()

// 表單資料
const form = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
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
async function handleRegister() {
  try {
    console.log('📤 Register data:', form.value)

    await register({
      phone: form.value.phone,
      password: form.value.password,
      display_name: form.value.name,
      email: form.value.email
      // 這裡還可以加 birthday, gender, primary_language_code...
    })

    // alert(`🎉 Register success! Welcome ${form.value.name}`)
    router.push('/login')
  } catch (err: any) {
    console.error('❌ Register error:', err)
    alert(`Register failed: ${err.message || err}`)
  }
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