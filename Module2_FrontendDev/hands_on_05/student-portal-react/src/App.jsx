import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import { coursesData } from './data';

function App() {
  // State: all courses loaded from data
  const [courses, setCourses]               = useState([]);
  // State: search term for filtering
  const [searchTerm, setSearchTerm]         = useState('');
  // State: enrolled courses (lifted up from CourseCard)
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  // State: loading indicator
  const [loading, setLoading]               = useState(true);
  // State: error message
  const [error, setError]                   = useState(null);

  // useEffect: fetch (simulated) courses on mount
  useEffect(() => {
    async function loadCourses() {
      try {
        setLoading(true);
        // Simulate API call with a delay
        await new Promise(resolve => setTimeout(resolve, 800));
        setCourses(coursesData);
      } catch (err) {
        setError('Failed to load courses.');
      } finally {
        setLoading(false);
      }
    }
    loadCourses();
  }, []);  // Empty array = run once on mount

  // Log to console whenever courses change
  useEffect(() => {
    if (courses.length > 0) {
      console.log('Courses updated:', courses.length, 'courses loaded');
    }
  }, [courses]);  // Dependency array: runs when courses changes

  // Handle enroll button click
  function handleEnroll(course) {
    if (!enrolledCourses.find(c => c.id === course.id)) {
      setEnrolledCourses(prev => [...prev, course]);
      alert(`✅ Enrolled in "${course.name}"!`);
    } else {
      alert(`Already enrolled in "${course.name}"`);
    }
  }

  // Filter courses based on search term
  const filteredCourses = courses.filter(c =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main style={{ maxWidth:'1100px', margin:'0 auto', padding:'32px 24px' }}>
        <h2 style={{ color:'#1a73e8', marginBottom:'20px' }}>Available Courses</h2>

        {/* Search input */}
        <input
          type="text"
          placeholder="Search courses..."
          value={searchTerm}
          onChange={e => setSearchTerm(e.target.value)}
          style={{ padding:'10px 16px', width:'100%', maxWidth:'400px', border:'1px solid #ccc', borderRadius:'6px', marginBottom:'24px', fontSize:'1rem' }}
        />

        {/* Loading state */}
        {loading && <p style={{ color:'#1a73e8', fontStyle:'italic' }}>Loading courses...</p>}

        {/* Error state */}
        {error && <p style={{ color:'red' }}>{error}</p>}

        {/* Course grid */}
        {!loading && !error && (
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit, minmax(260px,1fr))', gap:'20px' }}>
            {filteredCourses.map(course => (
              <CourseCard
                key={course.id}
                {...course}
                onEnroll={handleEnroll}
              />
            ))}
            {filteredCourses.length === 0 && (
              <p style={{ color:'#999' }}>No courses match your search.</p>
            )}
          </div>
        )}

        {/* Enrolled courses summary */}
        {enrolledCourses.length > 0 && (
          <div style={{ marginTop:'32px', background:'#e8f0fe', borderRadius:'10px', padding:'20px' }}>
            <h3 style={{ color:'#1a73e8', marginBottom:'12px' }}>My Enrolled Courses</h3>
            <ul>
              {enrolledCourses.map(c => (
                <li key={c.id} style={{ marginBottom:'6px', color:'#333' }}>
                  {c.name} — {c.credits} credits
                </li>
              ))}
            </ul>
          </div>
        )}
      </main>

      <Footer />
    </>
  );
}

export default App;