<template>
  <header class="app-header">
    <span class="logo">🎓 Student Portal (Vue)</span>
    <nav>
      <RouterLink to="/">Courses</RouterLink>
      <RouterLink to="/profile">
        Profile
        <span class="badge">{{ store.enrolledCourses.length }}</span>
      </RouterLink>
    </nav>
  </header>

  <RouterView />

  <footer class="app-footer">&copy; 2024 Student Portal — Vue.js</footer>
</template>

<script setup>
import { useEnrollmentStore } from '@/stores/enrollment';
const store = useEnrollmentStore();
</script>

<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Arial,sans-serif; background:#f4f6f9; }
.app-header { background:#1a73e8; color:white; padding:16px 32px; display:flex; justify-content:space-between; align-items:center; }
.logo { font-size:1.3rem; font-weight:bold; }
nav { display:flex; gap:20px; align-items:center; }
nav a { color:white; text-decoration:none; }
.badge { background:white; color:#1a73e8; border-radius:20px; padding:2px 10px; font-size:0.8rem; font-weight:bold; margin-left:6px; }
.app-footer { background:#1a73e8; color:white; text-align:center; padding:16px; margin-top:40px; }
</style>