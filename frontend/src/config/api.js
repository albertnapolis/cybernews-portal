export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';

export const API_ENDPOINTS = {
  // News endpoints
  NEWS: '/news',
  NEWS_BY_ID: (id) => `/news/${id}`,
  NEWS_CRITICAL: '/news/latest/critical',
  NEWS_TRENDING: '/news/trending',
  NEWS_REFRESH: '/news/refresh',

  // Categories endpoints
  CATEGORIES: '/categories',
  CATEGORY_BY_ID: (id) => `/categories/${id}`,
  CATEGORY_BY_SLUG: (slug) => `/categories/slug/${slug}`,
  CATEGORY_STATS: (id) => `/categories/${id}/stats`,

  // Sources endpoints
  SOURCES: '/sources',
  SOURCE_BY_ID: (id) => `/sources/${id}`,
  SOURCE_TOGGLE: (id) => `/sources/${id}/toggle`,
};