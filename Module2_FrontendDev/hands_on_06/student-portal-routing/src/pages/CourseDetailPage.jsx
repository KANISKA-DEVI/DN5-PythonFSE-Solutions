import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { enroll } from '../store/enrollmentSlice';
import { coursesData } from '../data';

function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate     = useNavigate();
  const dispatch     = useDispatch();

  const course = coursesData.find(c => c.id === parseInt(courseId));

  if (!course) {
    return <div style={{ padding:'32px' }}>Course not found. <a href="/courses">Go back</a></div>;
  }

  function handleEnroll() {
    dispatch(enroll(course));
    navigate('/profile');  // Navigate to profile after enrolling
  }

  return (
    <div style={{ maxWidth:'600px', margin:'60px auto', padding:'32px', background:'white', borderRadius:'12px', boxShadow:'0 4px 16px rgba(0,0,0,0.1)' }}>
      <h2 style={{ color:'#1a73e8', marginBottom:'16px' }}>{course.name}</h2>
      <p><strong>Code:</strong> {course.code}</p>
      <p><strong>Credits:</strong> {course.credits}</p>
      <p><strong>Your Grade:</strong> {course.grade}</p>
      <div style={{ marginTop:'24px', display:'flex', gap:'12px' }}>
        <button onClick={handleEnroll} style={{ padding:'10px 24px', background:'#1a73e8', color:'white', border:'none', borderRadius:'6px', cursor:'pointer' }}>
          Enroll &amp; Go to Profile
        </button>
        <button onClick={() => navigate(-1)} style={{ padding:'10px 24px', background:'#f1f3f4', color:'#333', border:'none', borderRadius:'6px', cursor:'pointer' }}>
          ← Back
        </button>
      </div>
    </div>
  );
}
export default CourseDetailPage;