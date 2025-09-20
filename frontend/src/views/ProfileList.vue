<template>
  <main>
    <h1>Profiles</h1>
    <button @click="goMe()">Go to My Profile</button>
    <ul>
      <li v-for="p in profiles" :key="p.id">
        <button @click="goDetail(p.id)">
          {{ p.displayName }}
        </button>
      </li>
    </ul>
    <button @click="$router.push('/')">Back to Home</button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserId } from '../services/auth'

const profiles = ref([])
const router = useRouter()

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'profiles.json')
  const data = await res.json()
  profiles.value = data.profiles
})

function goDetail(id) {
  router.push(`/profile/${id}`)
}

function goMe() {
  console.log('Going to my profile:', getUserId())
  router.push(`/profile/${getUserId()}`)
}
</script>
