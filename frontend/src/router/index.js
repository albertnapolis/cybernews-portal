import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import NewsDetail from '../views/NewsDetail.vue';
import CategoryView from '../views/CategoryView.vue';
import SourcesView from '../views/SourcesView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/news/:id',
    name: 'NewsDetail',
    component: NewsDetail,
    props: true,
  },
  {
    path: '/category/:slug',
    name: 'Category',
    component: CategoryView,
    props: true,
  },
  {
    path: '/sources',
    name: 'Sources',
    component: SourcesView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;