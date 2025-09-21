<template>
  <main class="dashboard">
    <!-- Tab Bar -->
    <div class="tab-bar">
      <button
        :class="{ active: activeTab === 'applications' }"
        @click="activeTab = 'applications'"
      >
        Applications
      </button>
      <button
        :class="{ active: activeTab === 'jobs' }"
        @click="activeTab = 'jobs'"
      >
        Jobs
      </button>
    </div>

    <div class="tab-content">
      <ApplicationList v-if="activeTab === 'applications'" />
      <MyJobList v-else />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ApplicationList from './ApplicationList.vue'
import MyJobList from './MyJobList.vue'

const activeTab = ref<'applications' | 'jobs'>('applications')
</script>

<style scoped>
.dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tab-bar {
  height: 35px;
  display: flex;
  justify-content: space-around;
  background: #f5f5f5;
  padding: 6px;
  border-bottom: 1px solid #ccc;
}

.tab-bar button {
  flex: 1;
  padding: 10px;
  border: none;
  background: none;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
}

.tab-bar button.active {
  border-bottom: 2px solid rgb(42, 65, 102);
  color: rgb(42, 65, 102);
}

.tab-content {
  flex: 1;
  overflow-y: auto;
}
</style>