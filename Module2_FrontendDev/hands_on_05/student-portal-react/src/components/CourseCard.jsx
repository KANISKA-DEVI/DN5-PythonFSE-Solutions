// CourseCard — accepts name, code, credits, grade, onEnroll as props
function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  const cardStyle = {
    background:'white', border:'1px solid #dde3f0', borderRadius:'10px',
    padding:'20px', boxShadow:'0 2px 8px rgba(0,0,0,0.07)'
  };

  return (
    <article style={cardStyle}>
      <span style={{ float:'right', background:'#34a853', color:'white', borderRadius:'20px', padding:'3px 10px', fontSize:'0.8rem' }}>
        {grade}
      </span>
      <h3 style={{ color:'#1a73e8', marginBottom:'8px' }}>{name}</h3>
      <p style={{ color:'#666', fontSize:'0.9rem', marginBottom:'12px' }}>{code}</p>
      <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center' }}>
        <span style={{ background:'#e8f0fe', color:'#1a73e8', borderRadius:'20px', padding:'3px 10px', fontSize:'0.8rem', fontWeight:'bold' }}>
          {credits} Credits
        </span>
        <button
          onClick={() => onEnroll({ id, name, code, credits, grade })}
          style={{ padding:'6px 16px', background:'#1a73e8', color:'white', border:'none', borderRadius:'4px', cursor:'pointer' }}
        >
          Enroll
        </button>
      </div>
    </article>
  );
}

export default CourseCard;