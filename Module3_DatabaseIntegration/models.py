from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    # Task 2: later add is_active column
    # is_active = Column(Boolean, default=True)

class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)

class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String, nullable=False)

class Enrollment(Base):
    __tablename__ = "enrollments"
    enrollment_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    course_id = Column(Integer, ForeignKey("courses.course_id"))

class Professor(Base):
    __tablename__ = "professors"
    professor_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

# Task 2: later add CourseSchedule
# class CourseSchedule(Base):
#     __tablename__ = "course_schedules"
#     schedule_id = Column(Integer, primary_key=True)
#     course_id = Column(Integer, ForeignKey("courses.course_id"))
#     day_of_week = Column(String)
#     start_time = Column(Time)
#     end_time = Column(Time)
