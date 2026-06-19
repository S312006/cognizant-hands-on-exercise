-- ================================================
-- HANDS-ON 2: Writing SQL Queries
-- Digital Nurture 5.0 | Module 3
-- Name: Sharmi
-- ================================================

-- ================================================
-- TASK 1: INSERT, UPDATE AND DELETE
-- ================================================

-- Step 15: Sample data already inserted in Hands-On 1 ✅

-- Step 16: Insert 2 additional students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Sharmi', 'Raja', 'sharmi.raja@college.edu', '2003-05-15', 1, 2022),
('Kiran', 'Kumar', 'kiran.kumar@college.edu', '2003-06-20', 2, 2023);

-- Verify students count (should be 10)
SELECT COUNT(*) AS students_count FROM students;

-- Step 17: Update grade of student_id=5 for course_id=1 from 'C' to 'B'
UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5 AND course_id = 1;

-- Verify update
SELECT * FROM enrollments WHERE student_id = 5 AND course_id = 1;

-- Step 18: Preview NULL grades before deleting
SELECT * FROM enrollments WHERE grade IS NULL;

-- Delete enrollments where grade IS NULL
DELETE FROM enrollments WHERE grade IS NULL;

-- Step 19: Verify row counts
SELECT COUNT(*) AS students_count FROM students;       -- should be 10
SELECT COUNT(*) AS enrollments_count FROM enrollments; -- should be 10 (12 - 2 NULL rows)

-- ================================================
-- TASK 2: SINGLE TABLE QUERIES AND FILTERING
-- ================================================

-- Step 20: All students enrolled in 2022 ordered by last_name
SELECT *
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

-- Step 21: Courses with more than 3 credits sorted by credits descending
SELECT *
FROM courses
WHERE credits > 3
ORDER BY credits DESC;

-- Step 22: Professors with salary between 80000 and 95000
SELECT *
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

-- Step 23: Students whose email ends with '@college.edu'
SELECT *
FROM students
WHERE email LIKE '%@college.edu';

-- Step 24: Count total students per enrollment_year
SELECT
    enrollment_year,
    COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

-- ================================================
-- TASK 3: MULTI TABLE JOINS
-- ================================================

-- Step 25: Student full name + department name
SELECT
    students.first_name || ' ' || students.last_name AS full_name,
    departments.dept_name
FROM students
JOIN departments ON departments.department_id = students.department_id;

-- Step 26: Enrollment + student name + course name (3 table JOIN)
SELECT
    students.first_name || ' ' || students.last_name AS full_name,
    courses.course_name,
    enrollments.grade
FROM enrollments
JOIN students ON students.student_id = enrollments.student_id
JOIN courses ON courses.course_id = enrollments.course_id;

-- Step 27: Students NOT enrolled in any course
SELECT
    students.first_name || ' ' || students.last_name AS full_name
FROM students
LEFT JOIN enrollments ON enrollments.student_id = students.student_id
WHERE enrollments.student_id IS NULL;

-- Step 28: Every course + number of students enrolled
-- (courses with 0 enrollments still appear)
SELECT
    courses.course_name,
    COUNT(enrollments.enrollment_id) AS student_count
FROM courses
LEFT JOIN enrollments ON enrollments.course_id = courses.course_id
GROUP BY courses.course_name
ORDER BY student_count DESC;

-- Step 29: Every department + professors + salaries
-- (departments with no professors still appear)
SELECT
    departments.dept_name,
    professors.prof_name,
    professors.salary
FROM departments
LEFT JOIN professors ON professors.department_id = departments.department_id;

-- ================================================
-- TASK 4: AGGREGATIONS AND GROUPING
-- ================================================

-- Step 30: Total enrollments per course
SELECT
    courses.course_name,
    COUNT(enrollments.enrollment_id) AS enrollment_count
FROM courses
LEFT JOIN enrollments ON enrollments.course_id = courses.course_id
GROUP BY courses.course_name
ORDER BY enrollment_count DESC;

-- Step 31: Average salary of professors per department
SELECT
    departments.dept_name,
    ROUND(AVG(professors.salary), 2) AS avg_salary
FROM departments
JOIN professors ON professors.department_id = departments.department_id
GROUP BY departments.dept_name
ORDER BY avg_salary DESC;

-- Step 32: Departments where total budget exceeds 600000
SELECT
    dept_name,
    budget
FROM departments
WHERE budget > 600000
ORDER BY budget DESC;

-- Step 33: Grade distribution for course CS101
SELECT
    enrollments.grade,
    COUNT(*) AS grade_count
FROM enrollments
JOIN courses ON courses.course_id = enrollments.course_id
WHERE courses.course_code = 'CS101'
GROUP BY enrollments.grade
ORDER BY enrollments.grade;

-- Step 34: Departments where more than 2 students enrolled
SELECT
    departments.dept_name,
    COUNT(enrollments.enrollment_id) AS total_enrollments
FROM departments
JOIN courses ON courses.department_id = departments.department_id
JOIN enrollments ON enrollments.course_id = courses.course_id
GROUP BY departments.dept_name
HAVING COUNT(enrollments.enrollment_id) > 2
ORDER BY total_enrollments DESC;

-- ================================================
-- HANDS-ON 2 COMPLETE! ✅
-- ================================================