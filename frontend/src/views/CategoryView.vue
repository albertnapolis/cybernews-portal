<template>
  <div class="category-view">
    <div class="container py-5">
      <h1>Category: {{ categoryName }}</h1>
      <p class="text-muted">Showing all articles in this category</p>

      <div class="row g-4 mt-4">
        <div v-for="article in filteredArticles" :key="article.id" class="col-md-4">
          <NewsCard :article="article" />
        </div>
      </div>

      <div v-if="filteredArticles.length === 0" class="text-center py-5">
        <p>No articles found in this category.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useNewsStore } from '../stores/news';
import NewsCard from '../components/NewsCard.vue';

const route = useRoute();
const newsStore = useNewsStore();

const categoryName = ref('');

const filteredArticles = computed(() => {
  return newsStore.articles.filter(article =>
    article.categories.some(cat => cat.slug === route.params.slug)
  );
});

onMounted(async () => {
  await newsStore.fetchCategories();
  const category = newsStore.categories.find(cat => cat.slug === route.params.slug);
  if (category) {
    categoryName.value = category.name;
  }
  newsStore.setFilter('category', route.params.slug);
});

watch(() => route.params.slug, (newSlug) => {
  const category = newsStore.categories.find(cat => cat.slug === newSlug);
  if (category) {
    categoryName.value = category.name;
  }
  newsStore.setFilter('category', newSlug);
});
</script>