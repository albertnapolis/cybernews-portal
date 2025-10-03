import apiClient from './api';
import { API_ENDPOINTS } from '../config/api';

export const newsService = {
  // Get paginated news
  async getNews(params = {}) {
    const { data } = await apiClient.get(API_ENDPOINTS.NEWS, { params });
    return data;
  },

  // Get single article
  async getArticle(id) {
    const { data } = await apiClient.get(API_ENDPOINTS.NEWS_BY_ID(id));
    return data;
  },

  // Get critical news
  async getCriticalNews(limit = 10) {
    const { data } = await apiClient.get(API_ENDPOINTS.NEWS_CRITICAL, {
      params: { limit }
    });
    return data;
  },

  // Get trending news
  async getTrendingNews(hours = 24, limit = 10) {
    const { data } = await apiClient.get(API_ENDPOINTS.NEWS_TRENDING, {
      params: { hours, limit }
    });
    return data;
  },

  // Refresh news feeds
  async refreshFeeds() {
    const { data } = await apiClient.post(API_ENDPOINTS.NEWS_REFRESH);
    return data;
  },

  // Get categories
  async getCategories() {
    const { data } = await apiClient.get(API_ENDPOINTS.CATEGORIES);
    return data;
  },

  // Get sources
  async getSources(activeOnly = true) {
    const { data } = await apiClient.get(API_ENDPOINTS.SOURCES, {
      params: { active_only: activeOnly }
    });
    return data;
  },
};