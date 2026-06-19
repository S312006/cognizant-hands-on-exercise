-- ================================================
-- HANDS-ON 4: Query Optimisation
-- Indexes, EXPLAIN & N+1 Problem
-- Digital Nurture 5.0 | Module 3
-- Name: Sharmi
-- ================================================

-- ================================================
-- TASK 1: BASELINE PERFORMANCE — NO INDEXES
-- ================================================

-- Step 48: Run EXPLAIN on the query
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- EXPLANATION OF EXPLAIN OUTPUT:
-- EXPLAIN shows HOW PostgreSQL plans to execute the query
-- It does NOT actually run the query
-- It shows estimated cost, rows, and scan types

-- Step 49: Run EXPLAIN ANALYZE (actually executes query)
EXPLAIN ANALYZE
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- BASELINE ANALYSIS COMMENTS:
-- Before adding indexes, PostgreSQL uses:
-- Seq Scan on students → reads ALL rows to find enrollment_year = 2022
-- Seq Scan on courses  → reads ALL rows to find matching courses
-- Seq Scan on enrollments → reads ALL rows
-- This is slow for large datasets!
-- Cost increases linearly with table size

-- Step 50: Note estimated cost
-- Look for "cost=X..Y" in EXPLAIN output
-- X = startup cost
-- Y = total cost
-- Lower cost = better performance ✅

-- ================================================
-- TASK 2: ADD INDEXES AND COMPARE PLANS
-- ================================================

-- Step 51: B-Tree index on students.enrollment_year
CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

-- What this does:
-- Creates a sorted index on enrollment_year
-- Instead of scanning ALL students
-- PostgreSQL jumps directly to year 2022 rows ✅

-- -----------------------------------------------

-- Step 52: Composite UNIQUE index on enrollments
CREATE UNIQUE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

-- What this does:
-- 1. Speeds up JOIN queries on student_id + course_id
-- 2. PREVENTS duplicate enrollments automatically!
-- Test duplicate prevention:
INSERT INTO enrollments (student_id, course_id, enrollment_date)
VALUES (1, 1, '2024-01-01');
-- Expected: ERROR - duplicate key value! ✅

-- -----------------------------------------------

-- Step 53: Index on courses.course_code
CREATE INDEX idx_courses_course_code
ON courses(course_code);

-- What this does:
-- Speeds up queries that filter by course_code
-- Example: WHERE course_code = 'CS101'

-- -----------------------------------------------

-- Step 54: Re-run EXPLAIN and compare
EXPLAIN ANALYZE
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- AFTER INDEX ANALYSIS COMMENTS:
-- Before indexes: Seq Scan (reads all rows)
-- After indexes:  Index Scan (jumps to matching rows)
-- Cost should be LOWER after adding indexes
-- Seq Scan → Index Scan on students table ✅

-- -----------------------------------------------

-- Step 55: Partial index for NULL grades
CREATE INDEX idx_enrollments_null_grade
ON enrollments(student_id)
WHERE grade IS NULL;

-- What this does:
-- Only indexes rows where grade IS NULL
-- Much smaller index than full table index
-- Super fast for finding unevaluated enrollments!

-- Test partial index
EXPLAIN ANALYZE
SELECT * FROM enrollments WHERE grade IS NULL;

-- ================================================
-- TASK 2 SUMMARY — INDEX TYPES
-- ================================================

-- INDEX TYPE    | WHAT IT DOES
-- B-Tree        | Default. Good for =, <, >, BETWEEN, ORDER BY
-- Composite     | Covers multiple columns together
-- Unique        | Prevents duplicate values
-- Partial       | Only indexes rows matching a condition

-- ================================================
-- TASK 3: N+1 PROBLEM
-- ================================================
-- For this task we write Python code
-- Save this as n_plus_one.py in orm/ subfolder