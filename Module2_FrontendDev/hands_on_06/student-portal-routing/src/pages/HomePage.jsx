import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div style={{ textAlign:'center', padding:'80px 32px', background:'linear-gradient(135deg,#e8f0fe,#d2e3fc)', minHeight:'60vh' }}>
      <h1 style={{ color:'#1a73e8', fontSize:'2.5rem', marginBottom:'16px' }}>Welcome to Student Portal</h1>
      <p style={{ color:'#555', fontSize:'1.1rem', marginBottom:'32px' }}>Manage your courses and track your progress.</p>
      <Link to="/courses" style={{ background:'#1a73e8', color:'white', padding:'14px 32px', borderRadius:'6px', textDecoration:'none', fontSize:'1rem' }}>
        Browse Courses
      </Link>
    </div>
  );
}
export default HomePage;