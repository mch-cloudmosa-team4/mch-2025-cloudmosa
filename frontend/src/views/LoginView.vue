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
        placeholder="Enter your phone number"
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

    <button class="btn" @click="$router.push('/register')" @focus="focusedIndex = 3">
      Register
    </button>

    <div v-if="locationStatus" class="location-status">
      <p :class="locationStatus.type">{{ locationStatus.message }}</p>
    </div>

    <p v-if="error" class="error" role="alert">{{ error }}</p>
    
    <!-- 全螢幕錯誤提示 -->
    <div v-if="showFullscreenError" class="fullscreen-error" @click="hideFullscreenError">
      <div class="error-content">
        <div class="error-icon">❌</div>
        <div class="error-message">{{ fullscreenErrorMessage }}</div>
        <div class="error-hint">Tap to dismiss</div>
      </div>
    </div>
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
const locationStatus = ref<{ type: 'info' | 'warning' | 'error'; message: string } | null>(null)

// 全螢幕錯誤提示
const showFullscreenError = ref(false)
const fullscreenErrorMessage = ref('')
let errorTimeout: NodeJS.Timeout | null = null

const userRef = ref(null)
const passRef = ref(null)
const btnRef = ref(null)
const focusables = [userRef, passRef, btnRef]
const focusedIndex = ref(0)

onMounted(() => {
  if (isAuthed()) router.replace('/home')
  window.addEventListener('keydown', handleKeys)
  
  // 顯示位置資訊狀態
  locationStatus.value = { type: 'info', message: '🌍 Location will be requested during login' }
  
  // Ensure initial focus is correctly set
  nextTick(() => {
    focusAt(0)
  })
})
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeys)
  // 清理定時器
  if (errorTimeout) {
    clearTimeout(errorTimeout)
  }
})

// 顯示全螢幕錯誤
function showFullscreenErrorMessage(message: string) {
  fullscreenErrorMessage.value = message
  showFullscreenError.value = true
  
  // 清除之前的定時器
  if (errorTimeout) {
    clearTimeout(errorTimeout)
  }
  
  // 2秒後自動隱藏
  errorTimeout = setTimeout(() => {
    hideFullscreenError()
  }, 2000)
}

// 隱藏全螢幕錯誤
function hideFullscreenError() {
  showFullscreenError.value = false
  fullscreenErrorMessage.value = ''
  if (errorTimeout) {
    clearTimeout(errorTimeout)
    errorTimeout = null
  }
}

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
  
  // 只保留基本的空值檢查，移除格式驗證
  if (!phone.value.trim()) {
    error.value = 'Please enter your phone number'
    return
  }
  
  if (!password.value) {
    error.value = 'Please enter your password'
    return
  }
  
  console.log('📝 Basic validation passed, calling login API...', {
    phone: phone.value.trim(),
    password: '***' // 不顯示密碼
  })
  
  error.value = ''
  loading.value = true
  locationStatus.value = { type: 'info', message: '🔍 Getting location...' }
  
  try {
    await login(phone.value.trim(), password.value)
    console.log('✅ Login successful!')
    locationStatus.value = { type: 'info', message: '✅ Login successful!' }
    router.replace('/home')
  } catch (err: any) {
    console.error('❌ Login failed:', err)
    
    // 根據錯誤類型設置不同的狀態和訊息
    if (err.message === 'Invalid phone number or password') {
      locationStatus.value = { type: 'error', message: '❌ Authentication failed' }
      // 使用全螢幕錯誤提示
      showFullscreenErrorMessage('Invalid phone number or password')
    } else if (err.message.includes('Location') || err.message.includes('Geolocation')) {
      locationStatus.value = { type: 'warning', message: '⚠️ Location unavailable' }
      error.value = err.message
    } else {
      locationStatus.value = { type: 'error', message: '❌ Login failed' }
      // 其他錯誤也使用全螢幕提示
      showFullscreenErrorMessage(err.message || 'Login failed. Please try again.')
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

.location-status {
  margin-top: 8px;
}

.location-status p {
  font-size: 11px;
  text-align: center;
  margin: 2px 0;
}

.location-status .info {
  color: #1976d2;
}

.location-status .warning {
  color: #f57c00;
}

.location-status .error {
  color: #d32f2f;
}

/* 全螢幕錯誤提示 */
.fullscreen-error {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

.error-content {
  background: white;
  padding: 20px 16px; /* 減少內邊距 */
  border-radius: 8px; /* 稍微減少圓角 */
  text-align: center;
  max-width: 220px; /* 減少最大寬度 */
  margin: 0 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25); /* 稍微減少陰影 */
}

.error-icon {
  font-size: 32px; /* 縮小圖示 */
  margin-bottom: 12px; /* 減少底部邊距 */
}

.error-message {
  font-size: 14px; /* 縮小字體 */
  color: #b00020;
  font-weight: 600;
  margin-bottom: 8px; /* 減少底部邊距 */
  line-height: 1.3;
}

.error-hint {
  font-size: 10px; /* 縮小提示文字 */
  color: #666;
  opacity: 0.8;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
