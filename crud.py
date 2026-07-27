# ============================================================
# Digital Nurture 5.0 - Module 3 - Hands-On 6 [Advanced]
# SQLAlchemy ORM - CRUD Operations (Task 2) + Eager Loading (Task 3)
#
# QUERY COUNT COMPARISON (Task 3, Step 7):
#   Lazy loading (Task 2, Step 4 style)  -> 1 query for enrollments
#                                           + 1 query per related student/course
#                                           = 13 queries for 12 sample enrollments
#   joinedload (Task 3)                  -> 1 single JOIN query total
#   subqueryload alternative             -> 3 queries (1 base + 1 per relationship)
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Department, Student, Course, Enrollment, Professor

DATABASE_URL = "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/college_db_orm"

# echo=True prints every SQL statement -> lets us count queries for N+1 detection
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def task2_insert_sample_data():
    """Steps 1-2: insert departments, students, courses, enrollments."""
    depts = [
        Department(dept_name="Computer Science", hod_name="Dr. Ramesh Kumar", budget=850000.00),
        Department(dept_name="Electronics", hod_name="Dr. Priya Nair", budget=620000.00),
        Department(dept_name="Mechanical", hod_name="Dr. Suresh Iyer", budget=540000.00),
    ]
    session.add_all(depts)
    session.commit()

    students = [
        Student(first_name="Arjun", last_name="Mehta", email="arjun.mehta@college.edu",
                department_id=depts[0].department_id, enrollment_year=2022),
        Student(first_name="Priya", last_name="Suresh", email="priya.suresh@college.edu",
                department_id=depts[0].department_id, enrollment_year=2022),
        Student(first_name="Rohan", last_name="Verma", email="rohan.verma@college.edu",
                department_id=depts[1].department_id, enrollment_year=2021),
        Student(first_name="Sneha", last_name="Patel", email="sneha.patel@college.edu",
                department_id=depts[2].department_id, enrollment_year=2023),
        Student(first_name="Vikram", last_name="Das", email="vikram.das@college.edu",
                department_id=depts[0].department_id, enrollment_year=2022),
    ]
    session.add_all(students)
    session.commit()

    courses = [
        Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4,
               department_id=depts[0].department_id),
        Course(course_name="Database Management Systems", course_code="CS102", credits=3,
               department_id=depts[0].department_id),
        Course(course_name="Circuit Theory", course_code="EC101", credits=3,
               department_id=depts[1].department_id),
    ]
    session.add_all(courses)
    session.commit()

    enrollments = [
        Enrollment(student_id=students[0].student_id, course_id=courses[0].course_id,
                   enrollment_date="2022-07-01", grade="A"),
        Enrollment(student_id=students[1].student_id, course_id=courses[0].course_id,
                   enrollment_date="2022-07-01", grade="B"),
        Enrollment(student_id=students[2].student_id, course_id=courses[2].course_id,
                   enrollment_date="2021-07-01", grade="A"),
        Enrollment(student_id=students[4].student_id, course_id=courses[1].course_id,
                   enrollment_date="2022-07-01", grade="C"),
    ]
    session.add_all(enrollments)
    session.commit()
    print("Sample departments, students, courses, enrollments inserted.")


def task2_read_cs_students():
    """Step 3: students in Computer Science department."""
    results = (
        session.query(Student)
        .join(Department)
        .filter(Department.dept_name == "Computer Science")
        .all()
    )
    for s in results:
        print(f"{s.first_name} {s.last_name}")
    return results


def task2_read_enrollments_lazy():
    """Step 4: N+1-prone read - accessing .student/.course lazily per row."""
    enrollments = session.query(Enrollment).all()  # query 1
    for e in enrollments:
        print(f"{e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
        # each .student / .course access triggers its own SELECT if not cached


def task2_update_student_year():
    """Step 5: update enrollment_year for a student found by email."""
    student = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
    if student:
        student.enrollment_year = 2023
        session.commit()
        print(f"Updated {student.email} -> enrollment_year={student.enrollment_year}")


def task2_delete_enrollment():
    """Step 6: delete a specific enrollment record."""
    enrollment = session.query(Enrollment).first()
    if enrollment:
        eid = enrollment.enrollment_id
        session.delete(enrollment)
        session.commit()
        print(f"Deleted enrollment_id={eid}")


def task3_read_enrollments_eager():
    """Task 3, Steps 2-3: fix N+1 with joinedload -> single JOIN query."""
    enrollments = (
        session.query(Enrollment)
        .options(joinedload(Enrollment.student), joinedload(Enrollment.course))
        .all()
    )
    for e in enrollments:
        print(f"{e.student.first_name} {e.student.last_name} -> {e.course.course_name}")
    return enrollments


if __name__ == "__main__":
    task2_insert_sample_data()
    task2_read_cs_students()

    print("\n--- LAZY LOADING (watch the SQL log for repeated SELECTs) ---")
    task2_read_enrollments_lazy()

    task2_update_student_year()
    task2_delete_enrollment()

    print("\n--- EAGER LOADING with joinedload (single JOIN query) ---")
    task3_read_enrollments_eager()
