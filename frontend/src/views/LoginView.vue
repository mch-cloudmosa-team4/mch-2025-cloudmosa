<!-- TODO: input form order -->
<template>
  <main class="screen" @keydown="handleKeys">
    <h1 class="title">Sign in</h1>

    <label class="field">
      <span>Username</span>
      <input
        ref="userRef"
        v-model.trim="username"
        type="text"
        inputmode="text"
        autocomplete="username"
        :autofocus="true"
        @focus="focusedIndex = 0"
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
      />
    </label>

    <button
      ref="btnRef"
      class="btn primary"
      :disabled="loading"
      @focus="focusedIndex = 2"
      @click="submit"
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
const username = ref('')
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
})
onUnmounted(() => window.removeEventListener('keydown', handleKeys))

function focusAt(i) {
  focusedIndex.value = (i + focusables.length) % focusables.length
  const el = focusables[focusedIndex.value]?.value
  nextTick(() => el && el.focus())
}

function handleKeys(e) {
  if (['ArrowDown', 'ArrowUp'].includes(e.key)) {
    e.preventDefault()
    focusAt(focusedIndex.value + (e.key === 'ArrowDown' ? 1 : -1))
  }
  if (e.key === 'Enter') {
    e.preventDefault()
    submit()
  }
}

async function submit() {
  if (loading.value) return
  error.value = ''
  loading.value = true
  try {
    await login(username.value, password.value)
    router.replace('/home')
  } catch (err) {
    error.value = err.message || 'Login failed'
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
