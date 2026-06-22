from pydantic import BaseModel
from typing   import Optional, List


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


class CourseResponse(BaseModel):
    id:            int
    name:          str
    code:          str
    credits:       int
    department_id: Optional[int] = None

    class Config:
        from_attributes = True   # Allows reading from ORM objects


class DepartmentResponse(BaseModel):
    id:      int
    name:    str
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True