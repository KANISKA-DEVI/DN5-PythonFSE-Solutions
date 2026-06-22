import { useDispatch, useSelector } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { coursesData } from '../data';
import { Link } from 'react-router-dom';

function CoursesPage() {
  const dispatch        = useDispatch();
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);

  return (
    <div style={{ maxWidth:'1100px', margin:'0 auto', padding:'32px 24px' }}>
      <h2 style={{ color:'#1a73e8', marginBottom:'24px' }}>All Courses</h2>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(260px,1fr))', gap:'20px' }}>
        {coursesData.map(course => {
          const isEnrolled = enrolledCourses.some(c => c.id === course.id);
          return (
            <div key={course.id} style={{ background:'white', borderRadius:'10px', padding:'20px', border:'1px solid #dde3f0', boxShadow:'0 2px 8px rgba(0,0,0,0.07)' }}>
              <h3 style={{ color:'#1a73e8', marginBottom:'8px' }}>
                <Link to={`/courses/${course.id}`} style={{ color:'#1a73e8', textDecoration:'none' }}>
                  {course.name}
                </Link>
              </h3>
              <p style={{ color:'#666', fontSize:'0.9rem', marginBottom:'12px' }}>{course.code} | {course.credits} Credits</p>
              <button
                onClick={() => dispatch(enroll(course))}
                disabled={isEnrolled}
                style={{ padding:'8px 16px', background: isEnrolled ? '#ccc' : '#1a73e8', color:'white', border:'none', borderRadius:'4px', cursor: isEnrolled ? 'default' : 'pointer' }}
              >
                {isEnrolled ? '✓ Enrolled' : 'Enroll'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
export default CoursesPage;