<template>
  <div class="sources-view">
    <div class="container py-5">
      <h1 class="mb-4">News Sources</h1>
      <p class="text-muted mb-5">We aggregate cybersecurity news from trusted sources around the web.</p>

      <div class="row g-4">
        <div v-for="source in sources" :key="source.id" class="col-md-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ source.name }}</h5>
              <p class="card-text text-muted">{{ source.description }}</p>
              <div class="d-flex justify-content-between align-items-center">
                <span :class="source.is_active ? 'badge bg-success' : 'badge bg-secondary'">
                  {{ source.is_active ? 'Active' : 'Inactive' }}
                </span>
                <a :href="source.url" target="_blank" class="btn btn-sm btn-outline-primary">
                  Visit Site <i class="bi bi-box-arrow-up-right"></i>
                </a>
              </div>
              <div v-if="source.last_fetched" class="mt-2">
                <small class="text-muted">
                  Last updated: {{ formatDate(source.last_fetched) }}
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useNewsStore } from '../stores/news';

const newsStore = useNewsStore();
const sources = ref([]);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

onMounted(async () => {
  await newsStore.fetchSources();
  sources.value = newsStore.sources;
});
</script>