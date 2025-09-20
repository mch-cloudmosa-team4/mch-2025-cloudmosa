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

      <!-- Location（先保留前端欄位；註冊 API 不一定吃這欄） -->
      <!-- <label>
        Location
        <input
          v-model="locationSearch"
          type="text"
          placeholder="Search location..."
          class="search-box"
        />
        <select v-model="form.location">
          <option
            v-for="loc in filteredLocations"
            :key="loc.code"
            :value="loc.code"
          >
            {{ loc.name }}
          </option>
        </select>
      </label> -->

      <button type="submit" class="submit-btn" :disabled="isSubmitting" :aria-busy="isSubmitting">
        {{ isSubmitting ? 'Submitting...' : 'Register' }}
      </button>

      <p v-if="errorMsg" class="error">{{ errorMsg }}</p>
      <p v-if="successMsg" class="success">{{ successMsg }}</p>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { sha256 as sha256Lib } from 'js-sha256'

// router
const router = useRouter()

// API base
const API_BASE = (import.meta.env.VITE_API_BASE_URL as string) || 'http://203.116.30.130:8000'
console.log(API_BASE)

// 表單資料
const form = ref({
  name: '',
  email: '',
  phone: '',
  password: '',
  location: ''
})

const isSubmitting = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

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

// --- Utils ---
// 1) SHA-256 to hex（Browser Web Crypto）
function hasWebCrypto(): boolean {
  try {
    // HTTPS 或 localhost 才算安全環境；同時需要 TextEncoder 與 subtle.digest
    const isSecure = typeof location !== 'undefined' &&
      (location.protocol === 'https:' || location.hostname === 'localhost')
    return !!(globalThis.crypto?.subtle?.digest && typeof TextEncoder !== 'undefined' && isSecure)
  } catch {
    return false
  }
}

async function sha256Hex(text: string): Promise<string> {
  if (hasWebCrypto()) {
    const data = new TextEncoder().encode(text)
    const digest = await crypto.subtle.digest('SHA-256', data)
    const bytes = new Uint8Array(digest)
    return Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('')
  }
  // ★ fallback：環境不支援 subtle 時改用純 JS
  return sha256Lib(text)
}

function normalizeTWPhone(input: string): string {
  const raw = input.replace(/[\s-]/g, '')
  if (raw.startsWith('+')) return raw
  if (/^09\d{8}$/.test(raw)) {
    return '+886' + raw.slice(1) // 去掉前導 0
  }
  return raw // 其他格式先原樣送出
}

// submit handler
async function handleRegister() {
  errorMsg.value = ''
  successMsg.value = ''
  isSubmitting.value = true
  try {
    console.log("[DEBUGGING] Test")
    const phone = form.value.phone
    // TODO: hash the password
    const passwd_hash = await sha256Hex(form.value.password)
    console.log("[DEBUGGING] ", passwd_hash)

    const payload: {
      phone: string
      passwd_hash: string
      display_name: string
      email?: string
    } = {
      phone,
      passwd_hash,
      display_name: form.value.name.trim()
    }
    if (form.value.email.trim()) {
      payload.email = form.value.email.trim()
    }
    
    console.log("[DEBUGGING]: ", payload)
    console.log("[DEBUGGING]: ", JSON.stringify(payload))
    const resp = await fetch(`${API_BASE}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    console.log("[DEBUGGING] Test02")

    // 非 2xx 視為錯誤
    if (!resp.ok) {
      // 嘗試讀取後端錯誤訊息
      let detail = ''
      try {
        const data = await resp.json()
        detail = data?.message || data?.error || JSON.stringify(data)
      } catch {
        detail = await resp.text()
      }
      throw new Error(detail || `HTTP ${resp.status}`)
    }

    // 讀回 Response（有些後端會回 tokens，有些只回 user 資料）
    const data = await resp.json().catch(() => ({}))

    // 若有回 access_token / refresh_token，就先存起來（依需求可改成 cookie）
    if (data?.access_token) {
      localStorage.setItem('access_token', data.access_token)
    }
    if (data?.refresh_token) {
      localStorage.setItem('refresh_token', data.refresh_token)
    }

    successMsg.value = 'Register success!'
    // 成功後導到 login（或直接導到首頁／填寫個人資料頁）
    setTimeout(() => {
      router.push('/login')
    }, 600)
  } catch (err: any) {
    errorMsg.value = err?.message ? String(err.message) : 'Register failed'
  } finally {
    isSubmitting.value = false
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
  margin-bottom: 8px;
  padding: 10px;
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  cursor: pointer;
}
.submit-btn[disabled] {
  opacity: 0.7;
  cursor: default;
}
.submit-btn:hover:not([disabled]) {
  background: rgb(80, 110, 160);
}

.error {
  margin-top: 6px;
  color: #b91c1c;
  font-size: 12px;
  line-height: 1.4;
}
.success {
  margin-top: 6px;
  color: #065f46;
  font-size: 12px;
}
</style>