import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// Configure Vite to read env files from the repository root so the frontend and
// backend can share a single `.env` file placed at the project root.
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_BACKEND_URL || `http://backend:5000`,
        changeOrigin: true,
        secure: false,
      }
    },
    port: 5173,
    watch: {
      usePolling: true,
      interval: 1000,
      ignored: ['**/node_modules/**', '**/vite.config.js', '**/.env']
    },
    hmr: {
      overlay: true
    }
  }
})
