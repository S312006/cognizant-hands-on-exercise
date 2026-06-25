from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import engine, get_db

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title='Course Management API',
    description='API for managing courses',
    version='1.0'
)

# COURSE ENDPOINTS
@app.get('/api/courses/',
         response_model=List[schemas.CourseResponse],
         tags=['Courses'])
def get_courses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(models.Course).offset(skip).limit(limit).all()


@app.post('/api/courses/',
          response_model=schemas.CourseResponse,
          status_code=201,
          tags=['Courses'])
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    new_course = models.Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}',
         response_model=schemas.CourseResponse,
         tags=['Courses'])
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


@app.put('/api/courses/{course_id}',
         response_model=schemas.CourseResponse,
         tags=['Courses'])
def update_course(
    course_id: int,
    course_data: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    for key, value in course_data.dict(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}',
            status_code=204,
            tags=['Courses'])
def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    course = db.query(models.Course).filter(
        models.Course.id == course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    db.delete(course)
    db.commit()
    return None


# DEPARTMENT ENDPOINTS
@app.get('/api/departments/',
         response_model=List[schemas.DepartmentResponse],
         tags=['Departments'])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.post('/api/departments/',
          response_model=schemas.DepartmentResponse,
          status_code=201,
          tags=['Departments'])
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db)
):
    new_department = models.Department(**department.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


# STUDENT ENDPOINTS
@app.get('/api/students/',
         response_model=List[schemas.StudentResponse],
         tags=['Students'])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.post('/api/students/',
          response_model=schemas.StudentResponse,
          status_code=201,
          tags=['Students'])
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


# ENROLLMENT ENDPOINTS
@app.get('/api/enrollments/',
         response_model=List[schemas.EnrollmentResponse],
         tags=['Enrollments'])
def get_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()


@app.post('/api/enrollments/',
          response_model=schemas.EnrollmentResponse,
          status_code=201,
          tags=['Enrollments'])
def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db)
):
    new_enrollment = models.Enrollment(**enrollment.dict())
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment