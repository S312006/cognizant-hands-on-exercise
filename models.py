# ============================================================
# Digital Nurture 5.0 - Module 3 - Hands-On 6 [Advanced]
# SQLAlchemy ORM - Model Definitions
#
# NOTE: is_active (Student) and CourseSchedule are Hands-On 7
# additions - added here directly with a comment marker so the
# file matches whatever state Alembic's autogenerate should see.
# If you want a true "before" version for Hands-On 7 Task 2,
# comment out the two marked blocks before running the first
# `alembic revision --autogenerate`.
# ============================================================

from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey,
    Date, DateTime, Numeric, Boolean, Time
)
from sqlalchemy.orm import declarative_base, relationship

# ---- Connection ----
# PostgreSQL:
DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/college_db_orm"
# MySQL alternative:
# DATABASE_URL = "mysql+mysqlconnector://root:YOUR_PASSWORD@localhost:3306/college_db_orm"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name = Column(String(100), nullable=False)
    hod_name = Column(String(100))
    budget = Column(Numeric(12, 2))

    students = relationship("Student", back_populates="department")
    courses = relationship("Course", back_populates="department")
    professors = relationship("Professor", back_populates="department")


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)
    is_active = Column(Boolean, default=True)  # Hands-On 7, Task 2

    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(150), nullable=False)
    course_code = Column(String(20), unique=True)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course")  # Hands-On 7


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade = Column(String(2))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, primary_key=True, autoincrement=True)
    prof_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary = Column(Numeric(10, 2))

    department = relationship("Department", back_populates="professors")


# ---- Hands-On 7, Task 2, Step 5: new table CourseSchedule ----
class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    day_of_week = Column(String(10))
    start_time = Column(Time)
    end_time = Column(Time)

    course = relationship("Course", back_populates="schedules")


if __name__ == "__main__":
    # Hands-On 6, Task 1, Step 5: auto-create all tables
    Base.metadata.create_all(engine)
    print("All tables created successfully in college_db_orm.")
