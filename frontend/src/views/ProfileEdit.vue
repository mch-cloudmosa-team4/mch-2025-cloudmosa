<template>
  <main v-if="profile">
    <h1 class="title">Edit Profile</h1>

    <form @submit.prevent="saveProfile" class="profile-form">
      <!-- Display Name -->
      <label>
        Display Name
        <input v-model="profile.display_name" type="text" required />
      </label>

      <!-- Birthday -->
      <label>
        Birthday
        <input v-model="profile.birthday" type="date" />
      </label>

      <!-- Gender -->
      <label>
        Gender
        <select v-model="profile.gender">
          <option value="0">Not specified</option>
          <option value="1">Male</option>
          <option value="2">Female</option>
        </select>
      </label>
      
      <!-- Bio -->
      <label>
        Bio
        <textarea v-model="profile.bio" rows="3" placeholder="Tell us about yourself"></textarea>
      </label>

      <!-- Language -->
      <label>
        Language
        <input v-model="profile.primary_language_code" type="text" placeholder="en, zh, jp..." />
      </label>

      <!-- Buttons -->
      <div class="actions">
        <button type="submit" class="save-btn">Save</button>
        <button type="button" class="cancel-btn" @click="$router.push('/profile')">
          Cancel
        </button>
      </div>
    </form>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { isAuthed } from '@/services/auth'
import { getMyProfile, updateMyProfileAll } from '../services/profiles'

const route = useRoute()
const router = useRouter()
const profile = ref<any>(null)

onMounted(async () => {
  // const res = await fetch(import.meta.env.BASE_URL + 'profiles.json')
  // console.log('Fetching profiles.json', res)
  // const data = await res.json()
  // profile.value = data.profiles.find((p: any) => p.id === parseInt(route.params.id as string))
  // console.log('Loaded profile: ', profile.value)
  try {
    const token = localStorage.getItem('auth_token')
    const data = await getMyProfile(token)
    profile.value = data
  } catch (err) {
    console.error('Failed to load profile:', err)
  }
})

async function saveProfile() {
  try {
    const token = localStorage.getItem('auth_token')
    await updateMyProfileAll(token, {
      display_name: profile.value.display_name,
      birth_date: profile.value.birthday,
      gender: profile.value.gender,
      bio: profile.value.bio,
      primary_language_code: profile.value.primary_language_code,
    })
    alert('Profile updated successfully!')
    router.push('/profile')
  } catch (err) {
    console.error('Failed to update profile:', err)
    alert('Failed to update profile.')
  }
}
</script>

<style scoped>
.title {
  font-size: 16px;
  font-weight: bold;
  margin: 12px 0;
  text-align: center;
}

.profile-form {
  width: 80%;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 320px;
  margin: 0 auto;
}

.profile-form label {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  color: #333;
}

.profile-form input,
.profile-form select,
.profile-form textarea {
  margin-top: 4px;
  padding: 8px;
  font-size: 13px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
  margin-bottom: 16px;
}

.save-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  background: rgb(42, 65, 102);
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.save-btn:hover {
  background: rgb(80, 110, 160);
}

.cancel-btn {
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  background: #ddd;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #bbb;
}
</style>