from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import Course, Department, get_db
from schemas  import CourseCreate, CourseUpdate, CourseResponse

app = FastAPI(
    title       = "Course Management API",
    description = "A FastAPI-based Course Management System",
    version     = "1.0.0",
    contact     = {"name": "Digital Nurture 5.0", "email": "support@college.edu"}
)


# ---- Root ----
@app.get("/", tags=["Health"])
def root():
    return {"message": "Course Management API is running", "docs": "/docs"}


# ---- Courses CRUD ----

@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"],
         summary="List all courses", response_description="List of courses")
def get_courses(
    skip:          int           = 0,
    limit:         int           = 10,
    department_id: Optional[int] = None,
    db:            Session       = Depends(get_db)
):
    """Get all courses with optional pagination and department filter."""
    query = db.query(Course)
    if department_id:
        query = query.filter(Course.department_id == department_id)
    return query.offset(skip).limit(limit).all()


@app.post("/api/courses/", response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED, tags=["Courses"],
          summary="Create a new course")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course. Validates with Pydantic, returns 422 on invalid input."""
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def update_course(course_id: int, course_data: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = course_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    # 204 No Content — return nothing