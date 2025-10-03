<template>
  <div class="news-detail-page">
    <div class="container py-5">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Article Content -->
      <div v-else-if="article" class="row">
        <div class="col-lg-8 mx-auto">
          <!-- Back Button -->
          <router-link to="/" class="btn btn-outline-secondary mb-4">
            <i class="bi bi-arrow-left"></i> Back to News
          </router-link>

          <!-- Article Header -->
          <div class="article-header mb-4">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <span :class="severityBadgeClass" class="badge fs-6">
                {{ article.severity.toUpperCase() }}
              </span>
              <small class="text-muted">
                <i class="bi bi-clock"></i> {{ formatDate(article.published_date) }}
              </small>
            </div>

            <h1 class="display-5 fw-bold mb-3">{{ article.title }}</h1>

            <div class="d-flex flex-wrap gap-2 mb-3">
              <span
                v-for="category in article.categories"
                :key="category.id"
                class="badge bg-secondary"
                :style="{ backgroundColor: category.color }"
              >
                {{ category.name }}
              </span>
            </div>

            <div class="text-muted">
              <i class="bi bi-globe"></i> Source: {{ article.source.name }}
            </div>
          </div>

          <!-- Article Image -->
          <div v-if="article.image_url" class="mb-4">
            <img :src="article.image_url" :alt="article.title" class="img-fluid rounded" />
          </div>

          <!-- Article Description -->
          <div v-if="article.description" class="lead mb-4">
            {{ article.description }}
          </div>

          <!-- Article Content -->
          <div v-if="article.content" class="article-content">
            <div v-html="formatContent(article.content)"></div>
          </div>

          <!-- External Link -->
          <div class="mt-5 p-4 bg-light rounded">
            <h5>Read Full Article</h5>
            <p>Visit the original source for the complete article and additional information.</p>
            <a :href="article.url" target="_blank" class="btn btn-primary">
              Visit Source <i class="bi bi-box-arrow-up-right"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="alert alert-danger">
        Article not found
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useNewsStore } from '../stores/news';

const route = useRoute();
const newsStore = useNewsStore();

const article = computed(() => newsStore.currentArticle);
const loading = computed(() => newsStore.loading);

const severityBadgeClass = computed(() => {
  if (!article.value) return '';

  const severityClasses = {
    critical: 'bg-danger',
    high: 'bg-warning text-dark',
    medium: 'bg-info',
    low: 'bg-secondary',
    info: 'bg-light text-dark',
  };
  return severityClasses[article.value.severity] || 'bg-secondary';
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatContent = (content) => {
  // Basic formatting - convert line breaks to paragraphs
  return content
    .split('\n\n')
    .map(para => `<p>${para}</p>`)
    .join('');
};

onMounted(() => {
  newsStore.fetchArticle(route.params.id);
});
</script>

<style scoped>
.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
}

.article-content :deep(p) {
  margin-bottom: 1.5rem;
}
</style>