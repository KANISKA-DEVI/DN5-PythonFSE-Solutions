# ============================================================
# Hands-On 7: models_v2.py — Updated models with new columns
# File: models_v2.py  
# Location: C:\DigitalNurture5\Module1_DatabaseIntegration\hands_on_7\
# ============================================================
# This file adds:
# 1. is_active column to Student
# 2. New CourseSchedule table
# ============================================================

from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Date, Numeric, Boolean, Time
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/college_db_orm"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    head_of_dept  = Column(String(100))
    budget        = Column(Numeric(12, 2))
    students      = relationship("Student",         back_populates="department")
    courses       = relationship("Course",          back_populates="department")
    professors    = relationship("Professor",       back_populates="department")
    schedules     = relationship("CourseSchedule",  back_populates="department")


class Student(Base):
    __tablename__ = "students"
    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)
    is_active       = Column(Boolean, default=True)   # NEW COLUMN (Step 98)

    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = "courses"
    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20), unique=True)
    credits       = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department  = relationship("Department",     back_populates="courses")
    enrollments = relationship("Enrollment",     back_populates="course")
    schedules   = relationship("CourseSchedule", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(String(2))

    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")


class Professor(Base):
    __tablename__ = "professors"
    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Numeric(10, 2))
    department    = relationship("Department", back_populates="professors")


# NEW TABLE: CourseSchedule (Step 102)
class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id   = Column(Integer, primary_key=True, autoincrement=True)
    course_id     = Column(Integer, ForeignKey("courses.course_id"))
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    day_of_week   = Column(String(10))   # e.g., "Monday"
    start_time    = Column(Time)
    end_time      = Column(Time)

    course     = relationship("Course",      back_populates="schedules")
    department = relationship("Department",  back_populates="schedules")

    def __repr__(self):
        return f"<CourseSchedule(course_id={self.course_id}, day='{self.day_of_week}')>"