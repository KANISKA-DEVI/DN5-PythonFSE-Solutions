from pydantic import BaseModel
from typing   import Optional, List, Any


class CourseCreate(BaseModel):
    name:          str
    code:          str
    credits:       int
    department_id: Optional[int] = None

class CourseUpdate(BaseModel):
    name:          Optional[str] = None
    code:          Optional[str] = None
    credits:       Optional[int] = None
    department_id: Optional[int] = None

class CoursePatch(BaseModel):
    name:    Optional[str] = None
    credits: Optional[int] = None

class CourseResponse(BaseModel):
    id:            int
    name:          str
    code:          str
    credits:       int
    department_id: Optional[int] = None
    class Config:
        from_attributes = True

# Standard error envelope
class ErrorDetail(BaseModel):
    code:    str
    message: str
    field:   Optional[str] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail

# Paginated response envelope
class PaginatedResponse(BaseModel):
    count:    int
    next:     Optional[str]
    previous: Optional[str]
    results:  List[Any]