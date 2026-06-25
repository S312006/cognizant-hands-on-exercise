from pydantic import BaseModel
from typing import Optional, List


# ─────────────────────────────
# DEPARTMENT SCHEMAS
# ─────────────────────────────

class DepartmentCreate(BaseModel):
    name: str
    head_of_dept: str
    budget: float

class DepartmentResponse(BaseModel):
    id: int
    name: str
    head_of_dept: str
    budget: float

    class Config:
        from_attributes = True


# ─────────────────────────────
# COURSE SCHEMAS
# ─────────────────────────────

class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int
    department_id: int

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int

    class Config:
        from_attributes = True


# ─────────────────────────────
# STUDENT SCHEMAS
# ─────────────────────────────

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    department_id: int

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    enrollment_year: int
    department_id: int

    class Config:
        from_attributes = True


# ─────────────────────────────
# ENROLLMENT SCHEMAS
# ─────────────────────────────

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: str
    grade: Optional[str] = None

    class Config:
        from_attributes = True