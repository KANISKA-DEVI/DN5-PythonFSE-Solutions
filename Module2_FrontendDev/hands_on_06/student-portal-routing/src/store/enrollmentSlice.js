import { createSlice } from '@reduxjs/toolkit';

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: { enrolledCourses: [] },
  reducers: {
    enroll(state, action) {
      const exists = state.enrolledCourses.find(c => c.id === action.payload.id);
      if (!exists) {
        state.enrolledCourses.push(action.payload);
      }
    },
    unenroll(state, action) {
      state.enrolledCourses = state.enrolledCourses.filter(c => c.id !== action.payload);
    }
  }
});

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;