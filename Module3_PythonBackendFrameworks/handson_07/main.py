from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import time

from database import Course, get_db
from schemas  import CourseCreate, CourseUpdate, CourseResponse

app = FastAPI(
    title       = "Course Management API v2",
    description = "FastAPI with Background Tasks and full CRUD",
    version     = "2.0.0"
)


# ---- Background Task Functions ----
def send_confirmation_email(student_email: str, course_name: str):
    """
    Simulates sending a confirmation email.
    Runs AFTER the response is returned to the client.
    """
    time.sleep(1)   # Simulate email sending delay
    print(f"\n[Background Task] Sending confirmation to {student_email} for course '{course_name}'")


def log_enrollment(student_id: int, course_id: int):
    print(f"[Background Task] Logged enrollment: student {student_id} → course {course_id}")


# ---- Root ----
@app.get("/", tags=["Health"])
def root():
    return {"message": "API running", "docs": "/docs"}


# ---- Courses ----

@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
def get_courses(
    skip:          int           = 0,
    limit:         int           = 10,
    department_id: Optional[int] = None,
    db:            Session       = Depends(get_db)
):
    query = db.query(Course)
    if department_id:
        query = query.filter(Course.department_id == department_id)
    return query.offset(skip).limit(limit).all()


@app.post("/api/courses/",
          response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["Courses"],
          summary="Create a course",
          response_description="The newly created course")
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(course, k, v)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()


# ---- Enrollment with Background Task ----

@app.post("/api/enrollments/",
          status_code=status.HTTP_201_CREATED,
          tags=["Enrollments"],
          summary="Enroll a student — triggers background email")
def enroll_student(
    student_id:      int,
    course_id:       int,
    student_email:   str,
    background_tasks: BackgroundTasks,
    db:              Session = Depends(get_db)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Add background tasks — they run AFTER this response is sent
    background_tasks.add_task(send_confirmation_email, student_email, course.name)
    background_tasks.add_task(log_enrollment, student_id, course_id)

    # Response is returned immediately (201) — email sends in background
    return {
        "message":    "Enrollment successful",
        "student_id": student_id,
        "course_id":  course_id,
        "note":       "Confirmation email is being sent in the background"
    }