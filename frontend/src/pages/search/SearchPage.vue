<template>
  <div class="page-container">
    <div class="search-container">
      <h1>Search Modules</h1>

      <div class="search-box">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search by module name or code..."
          class="input search-input"
          autofocus
        />
        <button v-if="searchQuery" @click="clearSearch" class="clear-button">
          ✕
        </button>
      </div>

      <div v-if="loading" class="loading">
        Searching...
      </div>

      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <div v-else-if="searchQuery && results.length === 0" class="no-results">
        No modules found matching "{{ searchQuery }}"
      </div>

      <div v-else-if="results.length > 0" class="results">
        <p class="results-count">Found {{ results.length }} module{{ results.length !== 1 ? 's' : '' }}</p>

        <div class="results-list">
          <router-link
            v-for="module in results"
            :key="module.id"
            :to="`/module/${module.code}`"
            class="module-card"
          >
            <div class="module-code">{{ module.code }}</div>
            <div class="module-name">{{ module.name }}</div>
            <div class="module-credits">{{ module.credits }} credits</div>
          </router-link>
        </div>
      </div>

      <div v-else class="search-prompt">
        <p>Enter a module name or code to search</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import '/src/assets/shared.css'

export default {
  name: 'SearchPage',
  setup() {
    const searchQuery = ref('')
    const results = ref([])
    const loading = ref(false)
    const error = ref(null)
    let searchTimeout = null

    const performSearch = async (query) => {
      if (!query.trim()) {
        results.value = []
        return
      }

      loading.value = true
      error.value = null

      try {
        const response = await fetch(`/api/searchModules?q=${encodeURIComponent(query)}`)

        if (!response.ok) {
          throw new Error(`Search failed: ${response.statusText}`)
        }

        const data = await response.json()
        results.value = data.modules || []
      } catch (err) {
        error.value = err.message
        console.error('Search error:', err)
      } finally {
        loading.value = false
      }
    }

    const handleSearch = () => {
      // Debounce search - wait 300ms after user stops typing
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        performSearch(searchQuery.value)
      }, 300)
    }

    const clearSearch = () => {
      searchQuery.value = ''
      results.value = []
      error.value = null
    }

    return {
      searchQuery,
      results,
      loading,
      error,
      handleSearch,
      clearSearch
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
  text-align: center;
}

.search-box {
  position: relative;
  margin-bottom: 2rem;
}

.search-input {
  padding-right: 3rem;
}

.clear-button {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
  transition: color 0.2s;
}

.clear-button:hover {
  color: #6b7280;
}

.error {
  text-align: center;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
  font-size: 1.125rem;
}

.search-prompt {
  text-align: center;
  padding: 4rem 2rem;
  color: #9ca3af;
  font-size: 1.125rem;
}

.results-count {
  color: #6b7280;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.module-card {
  display: block;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  text-decoration: none;
  transition: all 0.2s;
}

.module-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.module-code {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3b82f6;
  margin-bottom: 0.5rem;
  letter-spacing: 0.05em;
}

.module-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.module-credits {
  font-size: 0.875rem;
  color: #6b7280;
}
</style>
