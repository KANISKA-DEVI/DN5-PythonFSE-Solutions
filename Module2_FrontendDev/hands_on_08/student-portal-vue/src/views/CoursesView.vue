<template>
  <div class="container">
    <h2>Available Courses</h2>

    <input
      v-model="searchTerm"
      type="text"
      placeholder="Search courses..."
      class="search-input"
    />

    <div class="grid">
      <div v-for="course in filteredCourses" :key="course.id" class="course-wrapper">
        <CourseCard v-bind="course" />
        <div class="actions">
          <RouterLink :to="`/courses/${course.id}`" class="detail-link">Details</RouterLink>
          <button @click="handleEnroll(course)" :disabled="isEnrolled(course.id)" class="enroll-btn">
            {{ isEnrolled(course.id) ? '✓ Enrolled' : 'Enroll' }}
          </button>
        </div>
      </div>
    </div>

    <p v-if="filteredCourses.length === 0" style="color:#999;">No courses found.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useEnrollmentStore } from '@/stores/enrollment';
import { coursesData } from '@/data';
import CourseCard from '@/components/CourseCard.vue';

const store      = useEnrollmentStore();
const searchTerm = ref('');
const courses    = ref([]);

onMounted(() => { courses.value = coursesData; });

const filteredCourses = computed(() =>
  courses.value.filter(c => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
);

const isEnrolled = (id) => store.enrolledCourses.some(c => c.id === id);

function handleEnroll(course) {
  store.enroll(course);
}
</script>

<style scoped>
.container { max-width:1100px; margin:0 auto; padding:32px 24px; }
h2 { color:#1a73e8; margin-bottom:20px; }
.search-input { padding:10px 16px; width:100%; max-width:400px; border:1px solid #ccc; border-radius:6px; margin-bottom:24px; font-size:1rem; }
.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:20px; }
.course-wrapper { display:flex; flex-direction:column; gap:10px; }
.actions { display:flex; gap:8px; }
.detail-link { padding:6px 14px; background:#f1f3f4; color:#333; text-decoration:none; border-radius:4px; font-size:0.9rem; }
.enroll-btn { padding:6px 14px; background:#1a73e8; color:white; border:none; border-radius:4px; cursor:pointer; font-size:0.9rem; }
.enroll-btn:disabled { background:#ccc; cursor:default; }
</style>