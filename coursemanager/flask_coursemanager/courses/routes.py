from flask import Blueprint, request, jsonify
from app import db
from courses.models import Course, Department, Student, Enrollment

# Create Blueprint
# Like Django's urls.py
courses_bp = Blueprint('courses', __name__, url_prefix='/api')


# Hands-On 4, Task 2 - consistent JSON response envelope for SUCCESS responses
def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


# ─────────────────────────────
# COURSE ENDPOINTS
# ─────────────────────────────

# GET all courses / POST create course
@courses_bp.route('/courses/', methods=['GET', 'POST'])
def courses():
    # GET - return all courses
    if request.method == 'GET':
        all_courses = Course.query.all()
        return make_response_json([c.to_dict() for c in all_courses])

    # POST - create new course
    if request.method == 'POST':
        data = request.get_json()

        # Validate required fields
        if not data.get('name') or not data.get('code') or not data.get('credits'):
            return jsonify({'status': 'error', 'message': 'name, code, credits are required!'}), 400

        new_course = Course(
            name=data['name'],
            code=data['code'],
            credits=data['credits'],
            department_id=data['department_id']
        )
        db.session.add(new_course)
        db.session.commit()
        return make_response_json(new_course.to_dict(), 201)


# GET one / PUT update / DELETE course
@courses_bp.route('/courses/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def course_detail(id):
    # Find course or return 404
    course = Course.query.get_or_404(id)

    # GET - return one course
    if request.method == 'GET':
        return make_response_json(course.to_dict())

    # PUT - update course
    if request.method == 'PUT':
        data = request.get_json()
        course.name = data.get('name', course.name)
        course.code = data.get('code', course.code)
        course.credits = data.get('credits', course.credits)
        db.session.commit()
        return make_response_json(course.to_dict())

    # DELETE - delete course
    if request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
        return make_response_json({'message': 'Course deleted!'})


# GET all students enrolled in a specific course (JOIN via Enrollment)
@courses_bp.route('/courses/<int:id>/students/', methods=['GET'])
def course_students(id):
    # Confirm course exists, else 404
    course = Course.query.get_or_404(id)

    # Find all enrollments for this course
    enrollments = Enrollment.query.filter_by(course_id=course.id).all()

    # Pull out the related Student for each enrollment
    students = [Student.query.get(e.student_id) for e in enrollments]

    return make_response_json([s.to_dict() for s in students])


# ─────────────────────────────
# DEPARTMENT ENDPOINTS
# ─────────────────────────────

@courses_bp.route('/departments/', methods=['GET', 'POST'])
def departments():
    if request.method == 'GET':
        all_departments = Department.query.all()
        return make_response_json([d.to_dict() for d in all_departments])

    if request.method == 'POST':
        data = request.get_json()

        if not data.get('name'):
            return jsonify({'status': 'error', 'message': 'name is required!'}), 400

        new_department = Department(
            name=data['name'],
            head_of_dept=data.get('head_of_dept'),
            budget=data.get('budget')
        )
        db.session.add(new_department)
        db.session.commit()
        return make_response_json(new_department.to_dict(), 201)


# GET one / PUT update / DELETE department
@courses_bp.route('/departments/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def department_detail(id):
    department = Department.query.get_or_404(id)

    if request.method == 'GET':
        return make_response_json(department.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        department.name = data.get('name', department.name)
        department.head_of_dept = data.get('head_of_dept', department.head_of_dept)
        department.budget = data.get('budget', department.budget)
        db.session.commit()
        return make_response_json(department.to_dict())

    if request.method == 'DELETE':
        db.session.delete(department)
        db.session.commit()
        return make_response_json({'message': 'Department deleted!'})


# ─────────────────────────────
# STUDENT ENDPOINTS
# ─────────────────────────────

@courses_bp.route('/students/', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        all_students = Student.query.all()
        return make_response_json([s.to_dict() for s in all_students])

    if request.method == 'POST':
        data = request.get_json()

        if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
            return jsonify({'status': 'error', 'message': 'first_name, last_name, email are required!'}), 400

        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            enrollment_year=data.get('enrollment_year'),
            department_id=data['department_id']
        )
        db.session.add(new_student)
        db.session.commit()
        return make_response_json(new_student.to_dict(), 201)


# GET one / PUT update / DELETE student
@courses_bp.route('/students/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def student_detail(id):
    student = Student.query.get_or_404(id)

    if request.method == 'GET':
        return make_response_json(student.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.email = data.get('email', student.email)
        student.enrollment_year = data.get('enrollment_year', student.enrollment_year)
        db.session.commit()
        return make_response_json(student.to_dict())

    if request.method == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        return make_response_json({'message': 'Student deleted!'})


# ─────────────────────────────
# ENROLLMENT ENDPOINTS
# ─────────────────────────────

@courses_bp.route('/enrollments/', methods=['GET', 'POST'])
def enrollments():
    if request.method == 'GET':
        all_enrollments = Enrollment.query.all()
        return make_response_json([e.to_dict() for e in all_enrollments])

    if request.method == 'POST':
        data = request.get_json()

        if not data.get('student_id') or not data.get('course_id'):
            return jsonify({'status': 'error', 'message': 'student_id and course_id are required!'}), 400

        new_enrollment = Enrollment(
            student_id=data['student_id'],
            course_id=data['course_id'],
            enrollment_date=data.get('enrollment_date'),
            grade=data.get('grade')
        )
        db.session.add(new_enrollment)
        db.session.commit()
        return make_response_json(new_enrollment.to_dict(), 201)


# GET one / PUT update / DELETE enrollment
@courses_bp.route('/enrollments/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def enrollment_detail(id):
    enrollment = Enrollment.query.get_or_404(id)

    if request.method == 'GET':
        return make_response_json(enrollment.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        enrollment.student_id = data.get('student_id', enrollment.student_id)
        enrollment.course_id = data.get('course_id', enrollment.course_id)
        enrollment.enrollment_date = data.get('enrollment_date', enrollment.enrollment_date)
        enrollment.grade = data.get('grade', enrollment.grade)
        db.session.commit()
        return make_response_json(enrollment.to_dict())

    if request.method == 'DELETE':
        db.session.delete(enrollment)
        db.session.commit()
        return make_response_json({'message': 'Enrollment deleted!'})