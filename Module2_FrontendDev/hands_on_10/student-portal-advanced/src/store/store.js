import { configureStore } from '@reduxjs/toolkit';
import coursesReducer    from './coursesSlice';
import enrollmentReducer from './enrollmentSlice';

const store = configureStore({
  reducer: {
    courses:    coursesReducer,
    enrollment: enrollmentReducer
  }
});

export default store;