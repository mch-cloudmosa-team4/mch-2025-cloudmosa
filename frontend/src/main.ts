import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import './style.css'

// Import CORS test utility for debugging
import './utils/cors-test'

const app = createApp(App)

app.use(router)

app.mount('#app')