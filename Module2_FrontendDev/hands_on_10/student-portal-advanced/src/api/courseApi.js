// ============================================================
// Course API Functions — all use the centralised apiClient
// File: src/api/courseApi.js
// ============================================================
import apiClient from './apiClient';

export async function getAllCourses() {
  // Using /posts as a stand-in for courses
  const posts = await apiClient.get('/posts?_limit=5');
  // Map posts to course-like objects
  return posts.map((p, i) => ({
    id:      p.id,
    name:    p.title.substring(0, 40),
    code:    `CS10${i + 1}`,
    credits: (i % 2 === 0) ? 4 : 3,
    grade:   ['A','B','A','B','C'][i]
  }));
}

export async function getCourseById(id) {
  const post = await apiClient.get(`/posts/${id}`);
  return { id: post.id, name: post.title, body: post.body };
}