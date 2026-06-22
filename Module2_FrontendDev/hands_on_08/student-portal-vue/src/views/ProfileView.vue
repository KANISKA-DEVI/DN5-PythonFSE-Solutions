<template>
  <div class="container">
    <h2>My Profile</h2>
    <div class="summary">
      <p><strong>Total Credits:</strong> {{ store.totalCredits }}</p>
      <p><strong>Courses Enrolled:</strong> {{ store.enrolledCourses.length }}</p>
    </div>
    <h3>Enrolled Courses</h3>
    <p v-if="store.enrolledCourses.length === 0" style="color:#999;">
      No courses yet. <RouterLink to="/">Browse courses</RouterLink>
    </p>
    <div v-for="course in store.enrolledCourses" :key="course.id" class="enrolled-row">
      <div>
        <strong>{{ course.name }}</strong>
        <span style="color:#666; font-size:0.9rem; margin-left:8px;">{{ course.code }} | {{ course.credits }} Credits</span>
      </div>
      <button @click="store.unenroll(course.id)" class="remove-btn">Remove</button>
    </div>
  </div>
</template>

<script setup>
import { useEnrollmentStore } from '@/stores/enrollment';
const store = useEnrollmentStore();
</script>

<style scoped>
.container { max-width:700px; margin:0 auto; padding:32px 24px; }
h2 { color:#1a73e8; margin-bottom:20px; }
h3 { margin:24px 0 12px; }
.summary { background:#e8f0fe; border-radius:10px; padding:20px; margin-bottom:24px; }
.enrolled-row { background:white; border:1px solid #dde3f0; border-radius:8px; padding:16px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; }
.remove-btn { padding:6px 14px; background:#fce8e6; color:#c5221f; border:1px solid #f28b82; border-radius:4px; cursor:pointer; }
</style>