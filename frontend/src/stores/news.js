import { defineStore } from 'pinia';
import { newsService } from '../services/newsService';

export const useNewsStore = defineStore('news', {
  state: () => ({
    articles: [],
    currentArticle: null,
    categories: [],
    sources: [],
    criticalNews: [],
    trendingNews: [],
    loading: false,
    error: null,
    pagination: {
      total: 0,
      page: 1,
      pageSize: 20,
    },
    filters: {
      severity: null,
      category: null,
      sourceId: null,
      search: '',
      days: null,
    },
  }),

  getters: {
    filteredArticles: (state) => {
      let filtered = [...state.articles];

      if (state.filters.severity) {
        filtered = filtered.filter(a => a.severity === state.filters.severity);
      }

      if (state.filters.category) {
        filtered = filtered.filter(a =>
          a.categories.some(c => c.slug === state.filters.category)
        );
      }

      if (state.filters.search) {
        const searchLower = state.filters.search.toLowerCase();
        filtered = filtered.filter(a =>
          a.title.toLowerCase().includes(searchLower) ||
          a.description?.toLowerCase().includes(searchLower)
        );
      }

      return filtered;
    },

    totalPages: (state) => {
      return Math.ceil(state.pagination.total / state.pagination.pageSize);
    },

    severityCounts: (state) => {
      const counts = {
        critical: 0,
        high: 0,
        medium: 0,
        low: 0,
        info: 0,
      };

      state.articles.forEach(article => {
        counts[article.severity]++;
      });

      return counts;
    },
  },

  actions: {
    async fetchNews(page = 1) {
      this.loading = true;
      this.error = null;

      try {
        const params = {
          page,
          page_size: this.pagination.pageSize,
          ...this.filters,
        };

        const response = await newsService.getNews(params);
        this.articles = response.articles;
        this.pagination = {
          total: response.total,
          page: response.page,
          pageSize: response.page_size,
        };
      } catch (error) {
        this.error = 'Failed to fetch news articles';
        console.error('Error fetching news:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchArticle(id) {
      this.loading = true;
      this.error = null;

      try {
        this.currentArticle = await newsService.getArticle(id);
      } catch (error) {
        this.error = 'Failed to fetch article';
        console.error('Error fetching article:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchCriticalNews() {
      try {
        this.criticalNews = await newsService.getCriticalNews();
      } catch (error) {
        console.error('Error fetching critical news:', error);
      }
    },

    async fetchTrendingNews() {
      try {
        this.trendingNews = await newsService.getTrendingNews();
      } catch (error) {
        console.error('Error fetching trending news:', error);
      }
    },

    async fetchCategories() {
      try {
        this.categories = await newsService.getCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    async fetchSources() {
      try {
        this.sources = await newsService.getSources();
      } catch (error) {
        console.error('Error fetching sources:', error);
      }
    },

    async refreshFeeds() {
      this.loading = true;
      try {
        const response = await newsService.refreshFeeds();
        await this.fetchNews();
        return response;
      } catch (error) {
        this.error = 'Failed to refresh feeds';
        throw error;
      } finally {
        this.loading = false;
      }
    },

    setFilter(filterName, value) {
      this.filters[filterName] = value;
      this.fetchNews(1);
    },

    clearFilters() {
      this.filters = {
        severity: null,
        category: null,
        sourceId: null,
        search: '',
        days: null,
      };
      this.fetchNews(1);
    },

    setPage(page) {
      this.pagination.page = page;
      this.fetchNews(page);
    },
  },
});