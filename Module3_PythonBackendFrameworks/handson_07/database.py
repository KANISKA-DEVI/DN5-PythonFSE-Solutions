from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./coursemanager.db"

engine        = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal  = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base          = declarative_base()


class Department(Base):
    __tablename__ = "departments"
    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String(100), nullable=False)
    courses = relationship("Course", back_populates="department")


class Course(Base):
    __tablename__ = "courses"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(150), nullable=False)
    code          = Column(String(20), unique=True, index=True)
    credits       = Column(Integer, default=3)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    department    = relationship("Department", back_populates="courses")


# Create tables
Base.metadata.create_all(bind=engine)


# Dependency — yields a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()