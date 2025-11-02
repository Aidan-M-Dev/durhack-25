<template>
  <div>
    <p class="mb-4">This is a minimal frontend that will call the backend and use Supabase for auth.</p>

    <div class="space-y-3">
      <button @click="callHello" class="px-4 py-2 bg-blue-600 text-white rounded">Call /api/hello</button>
      <div v-if="helloMsg" class="p-3 bg-gray-100 rounded">{{ helloMsg }}</div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup() {
    const helloMsg = ref(null)

    async function callHello() {
      try {
        const address = `/api/hello`
        console.log('Fetching from:', address)
        const res = await fetch(address)
        console.log('Response:', res)
        const data = await res.json()
        helloMsg.value = JSON.stringify(data)
      } catch (err) {
        helloMsg.value = 'Error: ' + err.message
      }
    }

    return { helloMsg, callHello }
  }
}
</script>

<style scoped>
</style>
