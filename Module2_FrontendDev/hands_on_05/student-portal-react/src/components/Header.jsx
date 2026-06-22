function Header({ siteName, enrolledCount }) {
  return (
    <header style={{
      background:'#1a73e8', color:'white', padding:'16px 32px',
      display:'flex', justifyContent:'space-between', alignItems:'center'
    }}>
      <div style={{ fontSize:'1.4rem', fontWeight:'bold' }}>🎓 {siteName}</div>
      <nav style={{ display:'flex', gap:'20px', alignItems:'center' }}>
        <a href="#" style={{ color:'white', textDecoration:'none' }}>Home</a>
        <a href="#" style={{ color:'white', textDecoration:'none' }}>Courses</a>
        <a href="#" style={{ color:'white', textDecoration:'none' }}>Profile</a>
        <span style={{
          background:'white', color:'#1a73e8',
          borderRadius:'20px', padding:'4px 12px',
          fontWeight:'bold', fontSize:'0.85rem'
        }}>
          Enrolled: {enrolledCount}
        </span>
      </nav>
    </header>
  );
}

export default Header;