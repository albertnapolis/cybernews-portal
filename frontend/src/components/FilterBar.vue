<template>
  <div class="filter-bar bg-light py-3">
    <div class="container">
      <div class="row g-3 align-items-end">
        <!-- Search -->
        <div class="col-md-3">
          <label class="form-label small">Search</label>
          <div class="input-group">
            <input
              type="text"
              class="form-control"
              placeholder="Search news..."
              v-model="searchTerm"
              @keyup.enter="applyFilters"
            />
            <button class="btn btn-outline-secondary" @click="applyFilters">
              <i class="bi bi-search"></i>
            </button>
          </div>
        </div>

        <!-- Severity Filter -->
        <div class="col-md-2">
          <label class="form-label small">Severity</label>
          <select class="form-select" v-model="selectedSeverity" @change="applyFilters">
            <option value="">All</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
            <option value="info">Info</option>
          </select>
        </div>

        <!-- Category Filter -->
        <div class="col-md-2">
          <label class="form-label small">Category</label>
          <select class="form-select" v-model="selectedCategory" @change="applyFilters">
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category.id" :value="category.slug">
              {{ category.name }}
            </option>
          </select>
        </div>

        <!-- Source Filter -->
        <div class="col-md-2">
          <label class="form-label small">Source</label>
          <select class="form-select" v-model="selectedSource" @change="applyFilters">
            <option value="">All Sources</option>
            <option v-for="source in sources" :key="source.id" :value="source.id">
              {{ source.name }}
            </option>
          </select>
        </div>

        <!-- Time Range -->
        <div class="col-md-2">
          <label class="form-label small">Time Range</label>
          <select class="form-select" v-model="selectedDays" @change="applyFilters">
            <option value="">All Time</option>
            <option value="1">Last 24 Hours</option>
            <option value="7">Last Week</option>
            <option value="30">Last Month</option>
          </select>
        </div>

        <!-- Clear Filters -->
        <div class="col-md-1">
          <button class="btn btn-outline-secondary w-100" @click="clearFilters">
            <i class="bi bi-x-circle"></i> Clear
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNewsStore } from '../stores/news';

const newsStore = useNewsStore();

const searchTerm = ref('');
const selectedSeverity = ref('');
const selectedCategory = ref('');
const selectedSource = ref('');
const selectedDays = ref('');

const categories = ref([]);
const sources = ref([]);

onMounted(async () => {
  await newsStore.fetchCategories();
  await newsStore.fetchSources();
  categories.value = newsStore.categories;
  sources.value = newsStore.sources;
});

const applyFilters = () => {
  newsStore.setFilter('search', searchTerm.value);
  newsStore.setFilter('severity', selectedSeverity.value || null);
  newsStore.setFilter('category', selectedCategory.value || null);
  newsStore.setFilter('sourceId', selectedSource.value || null);
  newsStore.setFilter('days', selectedDays.value || null);
};

const clearFilters = () => {
  searchTerm.value = '';
  selectedSeverity.value = '';
  selectedCategory.value = '';
  selectedSource.value = '';
  selectedDays.value = '';
  newsStore.clearFilters();
};
</script>

<style scoped>
.filter-bar {
  border-bottom: 1px solid #dee2e6;
}
</style>