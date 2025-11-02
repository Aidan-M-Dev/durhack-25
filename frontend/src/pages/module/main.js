import App from './App.vue'
import router from './router.js'
// Use an absolute path from the project root so this page finds shared assets
import '/src/assets/main.css'
import { createApp } from 'vue'

const app = createApp(App)
app.use(router)
app.mount('#app')
