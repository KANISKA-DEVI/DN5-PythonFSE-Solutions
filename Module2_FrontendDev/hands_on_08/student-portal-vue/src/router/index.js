import { createRouter, createWebHistory } from 'vue-router';
import CoursesView      from '@/views/CoursesView.vue';
import CourseDetailView from '@/views/CourseDetailView.vue';
import ProfileView      from '@/views/ProfileView.vue';

const routes = [
  { path: '/',            component: CoursesView      },
  { path: '/courses/:id', component: CourseDetailView },
  { path: '/profile',     component: ProfileView      },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to) => {
  console.log(`Navigating to: ${to.path}`);
});

export default router;