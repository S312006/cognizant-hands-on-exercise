from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# TABLE 1 - Department
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    head_of_dept = Column(String(200))
    budget = Column(Float)

    # Relationships
    courses = relationship('Course', back_populates='department')
    students = relationship('Student', back_populates='department')


# TABLE 2 - Course
class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Relationship
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')


# TABLE 3 - Student
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    enrollment_year = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Relationship
    department = relationship('Department', back_populates='students')
    enrollments = relationship('Enrollment', back_populates='student')


# TABLE 4 - Enrollment
class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrollment_date = Column(String(20))
    grade = Column(String(2), nullable=True)

    # Relationships
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')