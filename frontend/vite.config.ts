import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vite.dev/config/
export default defineConfig({
  base: process.env.NODE_ENV === 'production' ? '/mch-2025-cloudmosa/' : '/',
  server: {
    host: '0.0.0.0', // 監聽所有網絡接口
    port: 5173,      // 可選：指定端口
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          // 禁用開發工具
          isCustomElement: () => false
        }
      }
    }),
    vueJsx(),
  ],
  define: {
    // 禁用 Vue DevTools
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})