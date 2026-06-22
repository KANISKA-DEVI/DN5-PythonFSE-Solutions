import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getAllCourses } from '../api/courseApi';

// Async thunk — handles the API call
export const fetchAllCourses = createAsyncThunk(
  'courses/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      return await getAllCourses();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Selectors (decouples components from store shape)
export const selectCourses        = state => state.courses.items;
export const selectCoursesLoading = state => state.courses.loading;
export const selectCoursesError   = state => state.courses.error;

const coursesSlice = createSlice({
  name: 'courses',
  initialState: { items: [], loading: false, error: null },
  reducers: {},
  extraReducers: builder => {
    builder
      .addCase(fetchAllCourses.pending,   state => { state.loading = true;  state.error = null; })
      .addCase(fetchAllCourses.fulfilled, (state, action) => { state.loading = false; state.items = action.payload; })
      .addCase(fetchAllCourses.rejected,  (state, action) => { state.loading = false; state.error = action.payload; });
  }
});

export default coursesSlice.reducer;