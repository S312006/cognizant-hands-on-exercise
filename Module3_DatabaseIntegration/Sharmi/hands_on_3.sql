-- ================================================
-- HANDS-ON 3: Advanced SQL
-- Subqueries, Views & Transactions
-- Digital Nurture 5.0 | Module 3
-- Name: Sharmi
-- ================================================

-- ================================================
-- TASK 1: SUBQUERIES
-- ================================================

-- Step 35: Find students enrolled in MORE courses
-- than the average enrollments per student
SELECT
    students.first_name,
    students.last_name,
    COUNT(enrollments.course_id) AS course_count
FROM students
JOIN enrollments ON enrollments.student_id = students.student_id
GROUP BY students.student_id, students.first_name, students.last_name
HAVING COUNT(enrollments.course_id) > (
    -- Non-correlated subquery: calculates average enrollments
    SELECT AVG(enrollment_count)
    FROM (
        SELECT COUNT(course_id) AS enrollment_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
);

-- Expected Output:
-- Students enrolled in 2 or more courses

-- -----------------------------------------------

-- Step 36: Courses where ALL students got 'A'
SELECT course_name
FROM courses
WHERE course_id NOT IN (
    -- Find courses where any student did NOT get 'A'
    SELECT course_id
    FROM enrollments
    WHERE grade != 'A'
);

-- Expected Output:
-- Courses where every student got A grade

-- -----------------------------------------------

-- Step 37: Professor with highest salary in each department
SELECT
    p1.prof_name,
    p1.salary,
    departments.dept_name
FROM professors p1
JOIN departments ON departments.department_id = p1.department_id
WHERE p1.salary = (
    -- Correlated subquery: finds max salary per department
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p1.department_id
);

-- Expected Output:
-- One professor per department with highest salary

-- -----------------------------------------------

-- Step 38: Departments where average salary exceeds 85000
SELECT
    dept_name,
    avg_salary
FROM (
    -- Derived table: calculate avg salary per department
    SELECT
        departments.dept_name,
        ROUND(AVG(professors.salary), 2) AS avg_salary
    FROM departments
    JOIN professors ON professors.department_id = departments.department_id
    GROUP BY departments.dept_name
) AS dept_salary_table
WHERE avg_salary > 85000;

-- Expected Output:
-- Only Computer Science department (avg > 85000)

-- ================================================
-- TASK 2: VIEWS
-- ================================================

-- Step 39: Create view for student enrollment summary
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    students.first_name || ' ' || students.last_name AS full_name,
    departments.dept_name,
    COUNT(enrollments.course_id) AS courses_enrolled,
    ROUND(AVG(
        CASE
            WHEN enrollments.grade = 'A' THEN 4
            WHEN enrollments.grade = 'B' THEN 3
            WHEN enrollments.grade = 'C' THEN 2
            WHEN enrollments.grade = 'D' THEN 1
            WHEN enrollments.grade = 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students
JOIN departments ON departments.department_id = students.department_id
LEFT JOIN enrollments ON enrollments.student_id = students.student_id
GROUP BY
    students.first_name,
    students.last_name,
    departments.dept_name;

-- Verify view
SELECT * FROM vw_student_enrollment_summary;

-- -----------------------------------------------

-- Step 40: Create view for course statistics
CREATE VIEW vw_course_stats AS
SELECT
    courses.course_name,
    courses.course_code,
    COUNT(enrollments.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE
            WHEN enrollments.grade = 'A' THEN 4
            WHEN enrollments.grade = 'B' THEN 3
            WHEN enrollments.grade = 'C' THEN 2
            WHEN enrollments.grade = 'D' THEN 1
            WHEN enrollments.grade = 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses
LEFT JOIN enrollments ON enrollments.course_id = courses.course_id
GROUP BY courses.course_name, courses.course_code;

-- Verify view (should return 5 rows)
SELECT * FROM vw_course_stats;

-- -----------------------------------------------

-- Step 41: Query view to find students with GPA above 3.0
SELECT *
FROM vw_student_enrollment_summary
WHERE gpa > 3.0;

-- -----------------------------------------------

-- Step 42: Try to UPDATE through view (will fail!)
-- UPDATE vw_student_enrollment_summary
-- SET dept_name = 'Electronics'
-- WHERE full_name = 'Arjun Mehta';

-- ANALYSIS COMMENT:
-- Multi-table views are NOT updatable because:
-- 1. View joins multiple tables (students + departments + enrollments)
-- 2. PostgreSQL cannot determine which table to update
-- 3. View also uses GROUP BY and aggregate functions
-- 4. Only simple single-table views without aggregates are updatable

-- -----------------------------------------------

-- Step 43: Drop views and recreate with CHECK OPTION
DROP VIEW vw_student_enrollment_summary;
DROP VIEW vw_course_stats;

-- Recreate simple single-table view WITH CHECK OPTION
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    student_id,
    first_name,
    last_name,
    email,
    enrollment_year
FROM students
WHERE enrollment_year = 2022
WITH CHECK OPTION;

-- WITH CHECK OPTION means:
-- If you try to INSERT/UPDATE a row through this view
-- where enrollment_year != 2022, it will be REJECTED!

-- Verify
SELECT * FROM vw_student_enrollment_summary;

-- ================================================
-- TASK 3: STORED PROCEDURES AND TRANSACTIONS
-- ================================================

-- Step 44: Create function to enroll a student
-- Checks for duplicate enrollment before inserting
CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT,
    p_course_id INT,
    p_enrollment_date DATE
)
RETURNS VOID AS $$
BEGIN
    -- Check if student is already enrolled
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id
        AND course_id = p_course_id
    ) THEN
        RAISE EXCEPTION 'Student % is already enrolled in course %',
            p_student_id, p_course_id;
    END IF;

    -- Insert enrollment record
    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (p_student_id, p_course_id, p_enrollment_date);

    RAISE NOTICE 'Student % successfully enrolled in course %',
        p_student_id, p_course_id;
END;
$$ LANGUAGE plpgsql;

-- Test function (should work)
SELECT fn_enroll_student(3, 1, '2024-01-01');

-- Test duplicate (should give error)
SELECT fn_enroll_student(1, 1, '2024-01-01');

-- -----------------------------------------------

-- Step 45: Create log table first
CREATE TABLE department_transfer_log (
    log_id        SERIAL PRIMARY KEY,
    student_id    INT,
    old_dept_id   INT,
    new_dept_id   INT,
    transfer_date DATE DEFAULT CURRENT_DATE
);

-- Create function to transfer student between departments
CREATE OR REPLACE FUNCTION fn_transfer_student(
    p_student_id  INT,
    p_new_dept_id INT
)
RETURNS VOID AS $$
DECLARE
    v_old_dept_id INT;
BEGIN
    -- Get current department
    SELECT department_id INTO v_old_dept_id
    FROM students
    WHERE student_id = p_student_id;

    -- Update student department
    UPDATE students
    SET department_id = p_new_dept_id
    WHERE student_id = p_student_id;

    -- Log the transfer
    INSERT INTO department_transfer_log
        (student_id, old_dept_id, new_dept_id)
    VALUES
        (p_student_id, v_old_dept_id, p_new_dept_id);

    RAISE NOTICE 'Student % transferred from dept % to dept %',
        p_student_id, v_old_dept_id, p_new_dept_id;
END;
$$ LANGUAGE plpgsql;

-- Test transfer (move Arjun from CS to Electronics)
SELECT fn_transfer_student(1, 2);

-- Verify
SELECT student_id, first_name, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log;

-- -----------------------------------------------

-- Step 46: Test transaction with error
BEGIN;
    UPDATE students SET department_id = 2 WHERE student_id = 1;
    INSERT INTO department_transfer_log (student_id, old_dept_id, new_dept_id)
    VALUES (1, 1, 999); -- 999 does not exist! Will cause error
ROLLBACK; -- Both statements undone! ✅

-- Verify student still has original department
SELECT student_id, first_name, department_id FROM students WHERE student_id = 1;

-- -----------------------------------------------

-- Step 47: SAVEPOINT test
BEGIN;
    -- First enrollment insert
    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (3, 2, '2024-01-01');

    -- Set savepoint after first insert
    SAVEPOINT my_savepoint;

    -- Second enrollment insert (will fail - duplicate)
    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (1, 1, '2024-01-01'); -- already exists!

    -- Rollback only to savepoint (keeps first insert)
    ROLLBACK TO SAVEPOINT my_savepoint;

COMMIT; -- Only first insert is saved! ✅

-- Verify first insert saved
SELECT * FROM enrollments WHERE student_id = 3 AND course_id = 2;

-- ================================================
-- HANDS-ON 3 COMPLETE! ✅
-- ================================================