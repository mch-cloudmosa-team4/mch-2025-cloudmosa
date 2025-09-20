<!-- TODO: input form order -->
<template>
  <main class="screen">
    <h1 class="title">Sign in</h1>

    <label class="field">
      <span>Phone Number</span>
      <input
        ref="userRef"
        v-model.trim="phone"
        type="tel"
        inputmode="tel"
        autocomplete="tel"
        placeholder="+886000000000"
        @focus="focusedIndex = 0"
        @keydown="handleKeys"
      />
    </label>

    <label class="field">
      <span>Password</span>
      <input
        ref="passRef"
        v-model="password"
        type="password"
        autocomplete="current-password"
        @focus="focusedIndex = 1"
        @keydown="handleKeys"
      />
    </label>

    <button
      ref="btnRef"
      class="btn primary"
      :disabled="loading"
      @focus="focusedIndex = 2"
      @click="submit"
      @keydown="handleKeys"
    >
      {{ loading ? 'Signing in...' : 'Login (Enter)' }}
    </button>

    <button class="btn" @click="$router.push('/register')">
      Register
    </button>

    <p v-if="error" class="error" role="alert">{{ error }}</p>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { login, isAuthed } from '../services/auth'

const router = useRouter()
const phone = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const userRef = ref(null)
const passRef = ref(null)
const btnRef = ref(null)
const focusables = [userRef, passRef, btnRef]
const focusedIndex = ref(0)

onMounted(() => {
  if (isAuthed()) router.replace('/home')
  window.addEventListener('keydown', handleKeys)
  // Ensure initial focus is correctly set
  nextTick(() => {
    focusAt(0)
  })
})
onUnmounted(() => window.removeEventListener('keydown', handleKeys))

function focusAt(i) {
  const newIndex = ((i % focusables.length) + focusables.length) % focusables.length
  focusedIndex.value = newIndex
  const el = focusables[newIndex]?.value
  nextTick(() => {
    if (el && el.focus) {
      el.focus()
    }
  })
}

function handleKeys(e) {
  if (['ArrowDown', 'ArrowUp'].includes(e.key)) {
    e.preventDefault()

    // Find current focused element index
    const currentElement = document.activeElement
    let currentIndex = focusedIndex.value

    // Double check the current index by comparing with refs
    if (currentElement === userRef.value) currentIndex = 0
    else if (currentElement === passRef.value) currentIndex = 1
    else if (currentElement === btnRef.value) currentIndex = 2

    const direction = e.key === 'ArrowDown' ? -1 : 1
    const newIndex = currentIndex + direction
    focusAt(newIndex)
  }
  if (e.key === 'Enter') {
    e.preventDefault()
    submit()
  }
}

async function submit() {
  console.log('🔐 Login button clicked!')
  
  if (loading.value) return
  
  // 基本驗證
  if (!phone.value.trim()) {
    error.value = 'Please enter your phone number'
    return
  }
  
  // 簡單的電話號碼格式檢查
  const phoneRegex = /^\+886\d{9}$/
  if (!phoneRegex.test(phone.value.trim())) {
    error.value = 'Please enter a valid phone number (e.g., +886000000000)'
    return
  }
  
  if (!password.value) {
    error.value = 'Please enter your password'
    return
  }
  
  console.log('📝 Validation passed, calling login API...', {
    phone: phone.value.trim(),
    password: '***' // 不顯示密碼
  })
  
  error.value = ''
  loading.value = true
  
  try {
    await login(phone.value.trim(), password.value)
    console.log('✅ Login successful!')
    router.replace('/home')
  } catch (err: any) {
    console.error('❌ Login failed:', err)
    // 顯示服務器返回的錯誤訊息
    if (err.message === 'Invalid phone number or password') {
      error.value = 'Invalid phone number or password'
    } else {
      error.value = err.message || 'Login failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 與其他頁面統一：小螢幕 240×320 */
.screen {
  width: 240px;
  height: 320px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #fdfdfd;
  font-size: 13px;
  padding-top: 16px;
}

.title {
  font-size: 18px;
  margin: 4px 0 12px;
  text-align: center;
  color: #222;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field > span {
  font-size: 12px;
  color: #555;
  padding-left: 16px;
}

input {
  font-size: 14px;
  padding: 6px 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 80%;
  align-self: center;
}

.btn {
  padding: 8px;
  font-size: 14px;
  border: none;
  border-radius: 6px;
  width: 80%;
  margin: 0 auto;
  cursor: pointer;
  margin-top: 10px;
}

.primary {
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
}

.btn:disabled {
  background: #aaa;
  cursor: not-allowed;
}

.error {
  color: #b00020;
  font-size: 12px;
  text-align: center;
  margin-top: 4px;
}
</style>
