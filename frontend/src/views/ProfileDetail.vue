<template>
  <main v-if="profile" class="profile-detail">
    <h1 class="title">Profile</h1>

    <div class="profile-card">
      <h2 class="name">{{ profile.displayName }}</h2>
      <p><strong>ID:</strong> {{ profile.id }}</p>
      <p><strong>Avatar ID:</strong> {{ profile.avatarId }}</p>
      <p><strong>Birthday:</strong> {{ profile.birthday }}</p>
      <p><strong>Gender:</strong> {{ profile.gender }}</p>
      <p><strong>Location:</strong> {{ profile.locationId }}</p>
      <p><strong>Bio:</strong> {{ profile.bio }}</p>
      <p><strong>Language:</strong> {{ profile.languageId }}</p>
      <p><strong>Created:</strong> {{ profile.created_at }}</p>
      <p><strong>Updated:</strong> {{ profile.updated_at }}</p>
    </div>

    <button class="edit-btn" @click="goToEdit">✎</button>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const profile = ref<any>(null)

onMounted(async () => {
  const res = await fetch(import.meta.env.BASE_URL + 'profiles.json')
  const data = await res.json()
  profile.value = data.profiles.find((p: any) => p.id === parseInt(route.params.id as string))
})

function goToEdit() {
  router.push(`/profile/${profile.value.id}/edit`)
}
</script>

<style scoped>
.profile-detail {
  width: 240px;
  height: 320px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0px;
  font-size: 11px;
  position: relative;
}

.title {
  font-size: 20px;
  text-align: center;
  margin-bottom: 16px;
  font-weight: bold;
}

.profile-card {
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin: 10px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.profile-card p {
  font-size: 14px;
  margin: 6px 0;
}

.name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
  text-align: center;
}

.edit-btn {
  position: sticky;
  bottom: 10px;
  left: 175px;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgb(255, 193, 7);
  color: black;
  font-size: 20px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
  flex-shrink: 0;       /* ⭐ 避免被 flex 壓扁 */
}
.edit-btn:hover {
  background: rgb(255, 170, 0);
}
</style>