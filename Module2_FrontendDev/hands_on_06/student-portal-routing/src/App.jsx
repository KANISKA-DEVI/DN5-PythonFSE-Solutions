import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import HomePage       from './pages/HomePage';
import CoursesPage    from './pages/CoursesPage';
import CourseDetailPage from './pages/CourseDetailPage';
import ProfilePage    from './pages/ProfilePage';

function App() {
  const enrolledCount = useSelector(state => state.enrollment.enrolledCourses.length);

  return (
    <BrowserRouter>
      <header style={{ background:'#1a73e8', color:'white', padding:'16px 32px', display:'flex', justifyContent:'space-between', alignItems:'center' }}>
        <div style={{ fontWeight:'bold', fontSize:'1.3rem' }}>🎓 Student Portal</div>
        <nav style={{ display:'flex', gap:'20px', alignItems:'center' }}>
          <Link to="/"        style={{ color:'white', textDecoration:'none' }}>Home</Link>
          <Link to="/courses" style={{ color:'white', textDecoration:'none' }}>Courses</Link>
          <Link to="/profile" style={{ color:'white', textDecoration:'none' }}>Profile</Link>
          <span style={{ background:'white', color:'#1a73e8', borderRadius:'20px', padding:'4px 12px', fontWeight:'bold', fontSize:'0.85rem' }}>
            Enrolled: {enrolledCount}
          </span>
        </nav>
      </header>

      <main style={{ minHeight:'80vh' }}>
        <Routes>
          <Route path="/"               element={<HomePage />}         />
          <Route path="/courses"        element={<CoursesPage />}      />
          <Route path="/courses/:courseId" element={<CourseDetailPage />} />
          <Route path="/profile"        element={<ProfilePage />}      />
        </Routes>
      </main>

      <footer style={{ background:'#1a73e8', color:'white', textAlign:'center', padding:'16px' }}>
        &copy; 2024 Student Portal
      </footer>
    </BrowserRouter>
  );
}

export default App;