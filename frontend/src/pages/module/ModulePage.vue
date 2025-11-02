<template>
  <div id="module-page">
    <div v-if="loading">Loading module {{ moduleCode }}...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <h1>Module: {{ moduleCode }}</h1>
      <div v-if="moduleData">
        <h2>Module Information</h2>
        <pre>{{ JSON.stringify(moduleData, null, 2) }}</pre>
      </div>
      <div v-else>
        <p>No data available for this module.</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'ModulePage',
  setup() {
    const route = useRoute()
    const moduleCode = ref(route.params.moduleName)
    const moduleData = ref(null)
    const loading = ref(false)
    const error = ref(null)

    const fetchModuleData = async (code) => {
      loading.value = true
      error.value = null

      try {
        // First query: search for modules by code
        const searchResponse = await fetch(`/api/searchModulesByCode/${code}`)
        if (!searchResponse.ok) {
          throw new Error(`Failed to search modules: ${searchResponse.statusText}`)
        }
        const searchData = await searchResponse.json()
        const modules = searchData.modules || []

        if (modules.length === 0) {
          moduleData.value = null
          return
        }

        // Use the first matching module (for now, selection will be on a different page)
        const moduleId = modules[0].id

        // Second query: get detailed module info by ID
        const detailsResponse = await fetch(`/api/getModuleInfo/${moduleId}`)
        if (!detailsResponse.ok) {
          throw new Error(`Failed to fetch module details: ${detailsResponse.statusText}`)
        }

        const detailsData = await detailsResponse.json()
        moduleData.value = detailsData
      } catch (err) {
        error.value = err.message
        console.error('Error fetching module data:', err)
      } finally {
        loading.value = false
      }
    }

    // Fetch data when component mounts
    onMounted(() => {
      if (moduleCode.value) {
        fetchModuleData(moduleCode.value)
      }
    })

    // Watch for route parameter changes
    watch(() => route.params.moduleName, (newModuleCode) => {
      moduleCode.value = newModuleCode
      if (newModuleCode) {
        fetchModuleData(newModuleCode)
      }
    })

    return {
      moduleCode,
      moduleData,
      loading,
      error
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
  padding: 1rem;
  border: 1px solid red;
  border-radius: 4px;
  margin: 1rem 0;
}

pre {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
}
</style>
