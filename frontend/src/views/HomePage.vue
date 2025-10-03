<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section text-white py-5">
      <div class="container text-center">
        <h1 class="display-4 fw-bold mb-4">Cybersecurity News Portal</h1>
        <p class="lead mb-4">Stay informed about the latest threats, vulnerabilities, and security updates</p>
        <button class="btn btn-light btn-lg me-3" @click="refreshFeeds">
          <i class="bi bi-arrow-clockwise"></i> Refresh Feeds
        </button>
        <button class="btn btn-outline-light btn-lg">
          <i class="bi bi-bell"></i> Subscribe to Alerts
        </button>
      </div>
    </section>

    <!-- Critical Alerts -->
    <section v-if="criticalNews.length > 0" class="bg-danger bg-opacity-10 py-3">
      <div class="container">
        <div class="d-flex align-items-center">
          <i class="bi bi-exclamation-triangle-fill text-danger me-2" style="font-size: 1.5rem;"></i>
          <strong class="text-danger me-3">Critical Alerts:</strong>
          <div class="flex-grow-1 overflow-hidden">
            <marquee>
              <span v-for="(alert, index) in criticalNews" :key="alert.id">
                {{ alert.title }}
                <span v-if="index < criticalNews.length - 1" class="mx-3">•</span>
              </span>
            </marquee>
          </div>
        </div>
      </div>
    </section>

    <!-- Filter Bar -->
    <FilterBar />

    <!-- Main Content -->
    <div class="container py-5">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading news articles...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-circle me-2"></i>
        {{ error }}
      </div>

      <!-- News Grid -->
      <div v-else>
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2>Latest News</h2>
          <span class="text-muted">{{ pagination.total }} articles found</span>
        </div>

        <div class="row g-4">
          <div v-for="article in articles" :key="article.id" class="col-md-4">
            <NewsCard :article="article" />
          </div>
        </div>

        <!-- Pagination -->
        <nav v-if="totalPages > 1" class="mt-5">
          <ul class="pagination justify-content-center">
            <li class="page-item" :class="{ disabled: pagination.page === 1 }">
              <a class="page-link" @click="setPage(pagination.page - 1)" href="#">
                Previous
              </a>
            </li>
            <li
              v-for="page in displayedPages"
              :key="page"
              class="page-item"
              :class="{ active: page === pagination.page }"
            >
              <a class="page-link" @click="setPage(page)" href="#">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: pagination.page === totalPages }">
              <a class="page-link" @click="setPage(pagination.page + 1)" href="#">
                Next
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useNewsStore } from '../stores/news';
import NewsCard from '../components/NewsCard.vue';
import FilterBar from '../components/FilterBar.vue';

const newsStore = useNewsStore();

const articles = computed(() => newsStore.articles);
const loading = computed(() => newsStore.loading);
const error = computed(() => newsStore.error);
const pagination = computed(() => newsStore.pagination);
const totalPages = computed(() => newsStore.totalPages);
const criticalNews = computed(() => newsStore.criticalNews);

const displayedPages = computed(() => {
  const current = pagination.value.page;
  const total = totalPages.value;
  const pages = [];

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    if (current <= 3) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i);
      }
      pages.push('...');
      pages.push(total);
    } else if (current >= total - 2) {
      pages.push(1);
      pages.push('...');
      for (let i = total - 4; i <= total; i++) {
        pages.push(i);
      }
    } else {
      pages.push(1);
      pages.push('...');
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i);
      }
      pages.push('...');
      pages.push(total);
    }
  }

  return pages;
});

const setPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    newsStore.setPage(page);
    window.scrollTo(0, 0);
  }
};

const refreshFeeds = async () => {
  try {
    const response = await newsStore.refreshFeeds();
    alert(response.message);
  } catch (error) {
    alert('Failed to refresh feeds');
  }
};

onMounted(async () => {
  await newsStore.fetchNews();
  await newsStore.fetchCriticalNews();
});
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
</style>