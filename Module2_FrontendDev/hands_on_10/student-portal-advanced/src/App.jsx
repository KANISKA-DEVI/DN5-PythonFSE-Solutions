import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAllCourses, selectCourses, selectCoursesLoading, selectCoursesError } from './store/coursesSlice';
import { enroll, unenroll, selectEnrolled } from './store/enrollmentSlice';

function App() {
  const dispatch        = useDispatch();
  const courses         = useSelector(selectCourses);
  const loading         = useSelector(selectCoursesLoading);
  const error           = useSelector(selectCoursesError);
  const enrolledCourses = useSelector(selectEnrolled);

  // Dispatch async thunk on mount
  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  return (
    <>
      <header style={{ background:'#1a73e8', color:'white', padding:'16px 32px', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
        <span style={{ fontWeight:'bold', fontSize:'1.3rem' }}>🎓 Student Portal (Advanced)</span>
        <span style={{ background:'white', color:'#1a73e8', borderRadius:'20px', padding:'4px 12px', fontWeight:'bold' }}>
          Enrolled: {enrolledCourses.length}
        </span>
      </header>

      <main style={{ maxWidth:'1100px', margin:'0 auto', padding:'32px 24px' }}>
        <h2 style={{ color:'#1a73e8', marginBottom:'24px' }}>Courses (via Redux Async Thunk)</h2>

        {loading && <p style={{ color:'#1a73e8', fontStyle:'italic' }}>Loading courses from API...</p>}

        {error && (
          <div style={{ background:'#fce8e6', border:'1px solid #f28b82', borderRadius:'8px', padding:'16px', marginBottom:'24px' }}>
            <p style={{ color:'#c5221f' }}>Error: {error}</p>
            <button onClick={() => dispatch(fetchAllCourses())} style={{ marginTop:'10px', padding:'8px 18px', background:'#c5221f', color:'white', border:'none', borderRadius:'4px', cursor:'pointer' }}>
              Retry
            </button>
          </div>
        )}

        {!loading && !error && (
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(260px,1fr))', gap:'20px' }}>
            {courses.map(course => {
              const isEnrolled = enrolledCourses.some(c => c.id === course.id);
              return (
                <div key={course.id} style={{ background:'white', borderRadius:'10px', padding:'20px', border:'1px solid #dde3f0' }}>
                  <h3 style={{ color:'#1a73e8', marginBottom:'8px' }}>{course.name}</h3>
                  <p style={{ color:'#666', fontSize:'0.9rem', marginBottom:'12px' }}>{course.code} | {course.credits} Credits</p>
                  <div style={{ display:'flex', gap:'8px' }}>
                    <button
                      onClick={() => dispatch(enroll(course))}
                      disabled={isEnrolled}
                      style={{ padding:'6px 14px', background: isEnrolled ? '#ccc' : '#1a73e8', color:'white', border:'none', borderRadius:'4px', cursor: isEnrolled ? 'default' : 'pointer' }}
                    >
                      {isEnrolled ? '✓ Enrolled' : 'Enroll'}
                    </button>
                    {isEnrolled && (
                      <button
                        onClick={() => dispatch(unenroll(course.id))}
                        style={{ padding:'6px 14px', background:'#fce8e6', color:'#c5221f', border:'1px solid #f28b82', borderRadius:'4px', cursor:'pointer' }}
                      >
                        Remove
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {enrolledCourses.length > 0 && (
          <div style={{ marginTop:'40px', background:'#e8f0fe', borderRadius:'10px', padding:'24px' }}>
            <h3 style={{ color:'#1a73e8', marginBottom:'16px' }}>My Enrolled Courses</h3>
            {enrolledCourses.map(c => (
              <div key={c.id} style={{ background:'white', borderRadius:'8px', padding:'12px 16px', marginBottom:'10px', border:'1px solid #dde3f0' }}>
                {c.name} — {c.credits} credits
              </div>
            ))}
          </div>
        )}
      </main>

      <footer style={{ background:'#1a73e8', color:'white', textAlign:'center', padding:'16px', marginTop:'40px' }}>
        &copy; 2024 Student Portal — Advanced State Management
      </footer>
    </>
  );
}

export default App;