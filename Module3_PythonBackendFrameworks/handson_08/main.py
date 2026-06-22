from fastapi import FastAPI, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from database import Course, get_db
from schemas  import (CourseCreate, CourseUpdate, CoursePatch,
                      CourseResponse, ErrorResponse, PaginatedResponse)

app = FastAPI(
    title   = "Course Management API",
    version = "1.0.0",
    contact = {"name": "Digital Nurture 5.0"}
)


# ---- Standardised error handler ----
def error_response(code: str, message: str, field: str = None, status_code: int = 400):
    return JSONResponse(
        status_code = status_code,
        content     = {"error": {"code": code, "message": message, "field": field}}
    )


# ---- v1 Courses ----

@app.get("/api/v1/courses/", tags=["v1 - Courses"])
def get_courses_v1(
    request:       Request,
    page:          int           = Query(1,  ge=1),
    page_size:     int           = Query(10, ge=1, le=100),
    search:        Optional[str] = None,
    department_id: Optional[int] = None,
    db:            Session       = Depends(get_db)
):
    """
    List courses with pagination and search.
    Returns DRF-style envelope: count, next, previous, results.

    Versioning note:
    - URL versioning (/api/v1/): simple, visible, easy to test in browser
    - Header versioning (Accept: application/vnd.api+json;version=1): cleaner URLs
      but harder to test and requires client header support
    """
    query = db.query(Course)

    if department_id:
        query = query.filter(Course.department_id == department_id)

    if search:
        query = query.filter(
            Course.name.ilike(f"%{search}%") | Course.code.ilike(f"%{search}%")
        )

    total     = query.count()
    skip      = (page - 1) * page_size
    courses   = query.offset(skip).limit(page_size).all()
    base_url  = str(request.base_url)

    def build_url(p):
        return f"{base_url}api/v1/courses/?page={p}&page_size={page_size}"

    return {
        "count":    total,
        "next":     build_url(page + 1) if (skip + page_size) < total else None,
        "previous": build_url(page - 1) if page > 1 else None,
        "results":  [{"id": c.id, "name": c.name, "code": c.code, "credits": c.credits} for c in courses]
    }


@app.post("/api/v1/courses/",
          response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["v1 - Courses"])
def create_course_v1(course: CourseCreate, request: Request, db: Session = Depends(get_db)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    # Add Location header pointing to the new resource
    response = JSONResponse(
        content     = {"id": db_course.id, "name": db_course.name, "code": db_course.code, "credits": db_course.credits},
        status_code = 201,
        headers     = {"Location": f"{request.base_url}api/v1/courses/{db_course.id}"}
    )
    return response


@app.get("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["v1 - Courses"])
def get_course_v1(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course with id {course_id} does not exist", status_code=404)
    return course


@app.patch("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["v1 - Courses"])
def patch_course_v1(course_id: int, data: CoursePatch, db: Session = Depends(get_db)):
    """PATCH — update only the supplied fields (partial update)."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(course, k, v)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/v1/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["v1 - Courses"])
def delete_course_v1(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return error_response("NOT_FOUND", f"Course {course_id} not found", status_code=404)
    db.delete(course)
    db.commit()