<template>
  <div class="card news-card h-100 border-0 shadow-sm">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <span :class="severityBadgeClass" class="badge">
          {{ article.severity.toUpperCase() }}
        </span>
        <small class="text-muted">
          <i class="bi bi-clock"></i> {{ formatDate(article.published_date) }}
        </small>
      </div>

      <h5 class="card-title">
        <router-link :to="`/news/${article.id}`" class="text-decoration-none text-dark">
          {{ article.title }}
        </router-link>
      </h5>

      <p class="card-text text-muted">
        {{ truncateText(article.description, 150) }}
      </p>

      <div class="d-flex flex-wrap gap-1 mb-3">
        <span
          v-for="category in article.categories"
          :key="category.id"
          class="badge bg-secondary"
          :style="{ backgroundColor: category.color }"
        >
          {{ category.name }}
        </span>
      </div>

      <div class="d-flex justify-content-between align-items-center">
        <small class="text-muted">
          <i class="bi bi-globe"></i> {{ article.source.name }}
        </small>
        <router-link :to="`/news/${article.id}`" class="btn btn-sm btn-outline-primary">
          Read More <i class="bi bi-arrow-right"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  article: {
    type: Object,
    required: true,
  },
});

const severityBadgeClass = computed(() => {
  const severityClasses = {
    critical: 'bg-danger',
    high: 'bg-warning text-dark',
    medium: 'bg-info',
    low: 'bg-secondary',
    info: 'bg-light text-dark',
  };
  return severityClasses[props.article.severity] || 'bg-secondary';
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));

  if (diffHours < 24) {
    return `${diffHours} hours ago`;
  } else if (diffHours < 48) {
    return 'Yesterday';
  } else {
    return date.toLocaleDateString();
  }
};

const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};
</script>

<style scoped>
.news-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

.card-title a:hover {
  color: #0d6efd !important;
}
</style>