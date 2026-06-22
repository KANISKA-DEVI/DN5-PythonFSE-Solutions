# ============================================================
# Hands-On 6: SQLAlchemy ORM — Model Definitions
# File: models.py
# Location: C:\DigitalNurture5\Module1_DatabaseIntegration\hands_on_6\
# ============================================================

from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Date, Numeric, DateTime, func
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Create the base class for all models
Base = declarative_base()

# --- Database connection ---
# Creates a NEW database (college_db_orm) to avoid conflicts with SQL exercises
# Change the password if yours is different
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)
# echo=True prints every SQL statement — great for learning!

SessionLocal = sessionmaker(bind=engine)


# ============================================================
# MODEL 1: Department
# ============================================================
class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Numeric(12, 2))

    # Relationships (one department has many students, courses, professors)
    students   = relationship("Student",   back_populates="department")
    courses    = relationship("Course",    back_populates="department")
    professors = relationship("Professor", back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name='{self.dept_name}')>"


# ============================================================
# MODEL 2: Student
# ============================================================
class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)

    # Relationships
    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name='{self.first_name} {self.last_name}')>"


# ============================================================
# MODEL 3: Course
# ============================================================
class Course(Base):
    __tablename__ = "courses"

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20), unique=True)
    credits       = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    # Relationships
    department  = relationship("Department",  back_populates="courses")
    enrollments = relationship("Enrollment",  back_populates="course")

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}', name='{self.course_name}')>"


# ============================================================
# MODEL 4: Enrollment
# ============================================================
class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(String(2))

    # Relationships (many-to-one back to Student and Course)
    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, course_id={self.course_id}, grade='{self.grade}')>"


# ============================================================
# MODEL 5: Professor
# ============================================================
class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Numeric(10, 2))

    # Relationship
    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor(id={self.professor_id}, name='{self.prof_name}')>"


# ============================================================
# Create all tables in the database
# ============================================================
if __name__ == "__main__":
    # First create the database in PostgreSQL
    # Run this in psql: CREATE DATABASE college_db_orm;
    print("Creating all tables in college_db_orm...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
    print("Tables in database:", Base.metadata.tables.keys())