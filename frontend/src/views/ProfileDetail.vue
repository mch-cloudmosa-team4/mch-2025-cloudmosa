<template>
  <main v-if="profile">
    <h1 class="title">Profile</h1>
    <h1>{{ profile.displayName }}</h1>
    <p><strong>ID:</strong> {{ profile.id }}</p>
    <p><strong>Avatar ID:</strong> {{ profile.avatarId }}</p>
    <p><strong>Birthday:</strong> {{ profile.birthday }}</p>
    <p><strong>Gender:</strong> {{ profile.gender }}</p>
    <p><strong>Location:</strong> {{ profile.locationId }}</p>
    <p><strong>Bio:</strong> {{ profile.bio }}</p>
    <p><strong>Language:</strong> {{ profile.languageId }}</p>
    <p><strong>Created:</strong> {{ profile.created_at }}</p>
    <p><strong>Updated:</strong> {{ profile.updated_at }}</p>
    <button @click="$router.push('/profile')">Back</button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const profile = ref(null)

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'profiles.json')
  console.log('Fetching profiles.json', res)
  const data = await res.json()
  profile.value = data.profiles.find((p) => p.id === parseInt(route.params.id))
  console.log('Loaded profile: ', profile.value)
})
</script>
