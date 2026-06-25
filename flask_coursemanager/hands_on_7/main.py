from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional

# -------------------------------
# Models
# -------------------------------
class Course(BaseModel):
    id: int
    name: str
    code: str

class CourseResponse(BaseModel):
    id: int
    name: str
    code: str

class Student(BaseModel):
    id: int
    name: str
    email: str

class Enrollment(BaseModel):
    id: int
    student_id: int
    course_id: int

# -------------------------------
# Fake DB (in-memory)
# -------------------------------
courses_db: List[Course] = []
students_db: List[Student] = []
enrollments_db: List[Enrollment] = []

# -------------------------------
# FastAPI App with Metadata
# -------------------------------
app = FastAPI(
    title="Course Management API",
    description="API for managing courses, students, and enrollments",
    version="1.0.0",
    contact={"name": "Your Name", "email": "your@email.com"}
)

# -------------------------------
# Helper Functions
# -------------------------------
def get_course_by_id(course_id: int) -> Optional[Course]:
    for course in courses_db:
        if course.id == course_id:
            return course
    return None

def get_student_by_id(student_id: int) -> Optional[Student]:
    for student in students_db:
        if student.id == student_id:
            return student
    return None

# -------------------------------
# Courses CRUD
# -------------------------------
@app.post(
    "/api/courses/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course",
    response_description="The created course details",
    tags=["Courses"]
)
def create_course(course: Course):
    courses_db.append(course)
    return course

@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
def list_courses():
    return courses_db

@app.get("/api/courses/{id}", response_model=CourseResponse, tags=["Courses"])
def get_course(id: int):
    course = get_course_by_id(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/api/courses/{id}", response_model=CourseResponse, tags=["Courses"])
def update_course(id: int, updated_course: Course):
    course = get_course_by_id(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.name = updated_course.name
    course.code = updated_course.code
    return course

@app.delete("/api/courses/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(id: int):
    course = get_course_by_id(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    courses_db.remove(course)
    return None  # DELETE returns no body

@app.get("/api/courses/{id}/students/", response_model=List[Student], tags=["Courses"])
def get_course_students(id: int):
    course = get_course_by_id(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    enrolled_students = [
        student for enrollment in enrollments_db if enrollment.course_id == id
        for student in students_db if student.id == enrollment.student_id
    ]
    return enrolled_students

# -------------------------------
# Students CRUD
# -------------------------------
@app.post("/api/students/", response_model=Student, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: Student):
    students_db.append(student)
    return student

@app.get("/api/students/", response_model=List[Student], tags=["Students"])
def list_students():
    return students_db

@app.put("/api/students/{id}", response_model=Student, tags=["Students"])
def update_student(id: int, updated_student: Student):
    student = get_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.name = updated_student.name
    student.email = updated_student.email
    return student

@app.delete("/api/students/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(id: int):
    student = get_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db.remove(student)
    return None

# -------------------------------
# Enrollments CRUD + Background Task
# -------------------------------
def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")

@app.post("/api/enrollments/", response_model=Enrollment, status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
def create_enrollment(enrollment: Enrollment, background_tasks: BackgroundTasks):
    student = get_student_by_id(enrollment.student_id)
    course = get_course_by_id(enrollment.course_id)
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    enrollments_db.append(enrollment)
    background_tasks.add_task(send_confirmation_email, student.email)
    return enrollment

@app.get("/api/enrollments/", response_model=List[Enrollment], tags=["Enrollments"])
def list_enrollments():
    return enrollments_db

@app.delete("/api/enrollments/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Enrollments"])
def delete_enrollment(id: int):
    enrollment = next((e for e in enrollments_db if e.id == id), None)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    enrollments_db.remove(enrollment)
    return None
