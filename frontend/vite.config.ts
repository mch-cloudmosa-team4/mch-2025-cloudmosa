import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
// import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/mch-2025-cloudmosa/' : '/',
  server: {
    host: '0.0.0.0',   // 監聽所有網絡接口
    port: 5173,        // 指定端口
    strictPort: true,  // 如果端口被佔用則失敗
  },
  plugins: [
    vue(),
    vueJsx(),
    // test
    // vueDevTools(), // 移除 Vue DevTools 以隱藏開發者工具圖標
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
