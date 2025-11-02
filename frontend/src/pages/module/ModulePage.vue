<template>
  <div id="module-page">
    <div class="header">
      <router-link to="/" class="back-link">← Back to Search</router-link>
    </div>

    <div v-if="loading" class="loading">Loading module {{ moduleCode }}...</div>
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
#module-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  color: #3b82f6;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.back-link:hover {
  background-color: #eff6ff;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  font-size: 1.125rem;
}

.error {
  color: #dc2626;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 1rem;
}

pre {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  padding: 1.5rem;
  border-radius: 8px;
  overflow-x: auto;
  font-size: 0.875rem;
}
</style>
