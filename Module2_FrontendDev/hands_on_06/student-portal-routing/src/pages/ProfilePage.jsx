import { useSelector, useDispatch } from 'react-redux';
import { unenroll } from '../store/enrollmentSlice';

function ProfilePage() {
  const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
  const dispatch        = useDispatch();

  const totalCredits = enrolledCourses.reduce((sum, c) => sum + c.credits, 0);

  return (
    <div style={{ maxWidth:'700px', margin:'0 auto', padding:'32px 24px' }}>
      <h2 style={{ color:'#1a73e8', marginBottom:'24px' }}>My Profile</h2>
      <div style={{ background:'#e8f0fe', borderRadius:'10px', padding:'20px', marginBottom:'24px' }}>
        <p><strong>Name:</strong> Arjun Mehta</p>
        <p><strong>Total Enrolled Credits:</strong> {totalCredits}</p>
        <p><strong>Courses Enrolled:</strong> {enrolledCourses.length}</p>
      </div>

      <h3 style={{ color:'#333', marginBottom:'16px' }}>Enrolled Courses</h3>
      {enrolledCourses.length === 0
        ? <p style={{ color:'#999' }}>No courses enrolled yet. <a href="/courses">Browse courses</a></p>
        : enrolledCourses.map(c => (
          <div key={c.id} style={{ background:'white', border:'1px solid #dde3f0', borderRadius:'8px', padding:'16px', marginBottom:'12px', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
            <div>
              <strong>{c.name}</strong>
              <p style={{ color:'#666', fontSize:'0.9rem' }}>{c.code} | {c.credits} Credits</p>
            </div>
            <button
              onClick={() => dispatch(unenroll(c.id))}
              style={{ padding:'6px 14px', background:'#fce8e6', color:'#c5221f', border:'1px solid #f28b82', borderRadius:'4px', cursor:'pointer' }}
            >
              Remove
            </button>
          </div>
        ))
      }
    </div>
  );
}
export default ProfilePage;