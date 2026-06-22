<template>
  <div class="container">
    <div v-if="course" class="detail-card">
      <h2>{{ course.name }}</h2>
      <p><strong>Code:</strong> {{ course.code }}</p>
      <p><strong>Credits:</strong> {{ course.credits }}</p>
      <p><strong>Grade:</strong> {{ course.grade }}</p>
      <div class="btn-row">
        <button @click="handleEnroll" class="enroll-btn">Enroll &amp; Go to Profile</button>
        <button @click="router.go(-1)" class="back-btn">← Back</button>
      </div>
    </div>
    <div v-else>Course not found.</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useEnrollmentStore } from '@/stores/enrollment';
import { coursesData } from '@/data';

const route  = useRoute();
const router = useRouter();
const store  = useEnrollmentStore();

const course = computed(() => coursesData.find(c => c.id === parseInt(route.params.id)));

function handleEnroll() {
  if (course.value) {
    store.enroll(course.value);
    router.push('/profile');
  }
}
</script>

<style scoped>
.container { max-width:600px; margin:60px auto; padding:24px; }
.detail-card { background:white; border-radius:12px; padding:32px; border:1px solid #dde3f0; box-shadow:0 4px 16px rgba(0,0,0,0.08); }
h2 { color:#1a73e8; margin-bottom:16px; }
p { margin-bottom:10px; }
.btn-row { display:flex; gap:12px; margin-top:24px; }
.enroll-btn { padding:10px 24px; background:#1a73e8; color:white; border:none; border-radius:6px; cursor:pointer; }
.back-btn { padding:10px 24px; background:#f1f3f4; color:#333; border:none; border-radius:6px; cursor:pointer; }
</style>