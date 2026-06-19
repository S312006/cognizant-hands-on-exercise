-- ================================================
-- HANDS-ON 1: Schema Design & Core SQL
-- Digital Nurture 5.0 | Module 3
-- Name: Sharmi
-- ================================================

-- ================================================
-- STEP 1: Create Database
-- ================================================
CREATE DATABASE college_db;

-- ================================================
-- STEP 2: Create All 5 Tables
-- ================================================

-- Table 1: departments (create first - others depend on it)
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    dept_name     VARCHAR(100) NOT NULL,
    hod_name      VARCHAR(100),
    budget        DECIMAL(12, 2)
);

-- Table 2: students
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT REFERENCES departments(department_id),
    enrollment_year INT
);

-- Table 3: courses
CREATE TABLE courses (
    course_id     SERIAL PRIMARY KEY,
    course_name   VARCHAR(150) NOT NULL,
    course_code   VARCHAR(20) UNIQUE,
    credits       INT,
    department_id INT REFERENCES departments(department_id)
);

-- Table 4: enrollments
CREATE TABLE enrollments (
    enrollment_id   SERIAL PRIMARY KEY,
    student_id      INT REFERENCES students(student_id),
    course_id       INT REFERENCES courses(course_id),
    enrollment_date DATE,
    grade           CHAR(2)
);

-- Table 5: professors
CREATE TABLE professors (
    professor_id  SERIAL PRIMARY KEY,
    prof_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE,
    department_id INT REFERENCES departments(department_id),
    salary        DECIMAL(10, 2)
);

-- ================================================
-- STEP 3: Insert Data into All 5 Tables
-- ================================================

-- Insert Departments
INSERT INTO departments (dept_name, hod_name, budget) VALUES
('Computer Science', 'Dr. Ramesh Kumar', 850000.00),
('Electronics', 'Dr. Priya Nair', 620000.00),
('Mechanical', 'Dr. Suresh Iyer', 540000.00),
('Civil', 'Dr. Ananya Sharma', 430000.00);

-- Insert Students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Arjun', 'Mehta', 'arjun.mehta@college.edu', '2003-04-12', 1, 2022),
('Priya', 'Suresh', 'priya.suresh@college.edu', '2003-07-25', 1, 2022),
('Rohan', 'Verma', 'rohan.verma@college.edu', '2002-11-08', 2, 2021),
('Sneha', 'Patel', 'sneha.patel@college.edu', '2004-01-30', 3, 2023),
('Vikram', 'Das', 'vikram.das@college.edu', '2003-09-14', 1, 2022),
('Kavya', 'Menon', 'kavya.menon@college.edu', '2002-05-17', 2, 2021),
('Aditya', 'Singh', 'aditya.singh@college.edu', '2004-03-22', 4, 2023),
('Deepika', 'Rao', 'deepika.rao@college.edu', '2003-08-09', 1, 2022);

-- Insert Courses
INSERT INTO courses (course_name, course_code, credits, department_id) VALUES
('Data Structures & Algorithms', 'CS101', 4, 1),
('Database Management Systems', 'CS102', 3, 1),
('Object Oriented Programming', 'CS103', 4, 1),
('Circuit Theory', 'EC101', 3, 2),
('Thermodynamics', 'ME101', 3, 3);

-- Insert Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2022-07-01', 'A'), (1, 2, '2022-07-01', 'B'),
(2, 1, '2022-07-01', 'B'), (2, 3, '2022-07-01', 'A'),
(3, 4, '2021-07-01', 'A'), (4, 5, '2023-07-01', NULL),
(5, 1, '2022-07-01', 'C'), (5, 2, '2022-07-01', 'A'),
(6, 4, '2021-07-01', 'B'), (7, 5, '2023-07-01', NULL),
(8, 1, '2022-07-01', 'A'), (8, 3, '2022-07-01', 'B');

-- Insert Professors
INSERT INTO professors (prof_name, email, department_id, salary) VALUES
('Dr. Anand Krishnan', 'anand.k@college.edu', 1, 95000.00),
('Dr. Meena Pillai', 'meena.p@college.edu', 1, 88000.00),
('Dr. Sunil Rajan', 'sunil.r@college.edu', 2, 82000.00),
('Dr. Latha Gopal', 'latha.g@college.edu', 3, 79000.00),
('Dr. Kartik Bose', 'kartik.b@college.edu', 4, 76000.00);

-- ================================================
-- TASK 2: NORMALISATION ANALYSIS
-- ================================================

-- 1NF ANALYSIS:
-- Every column in all tables holds atomic (single) values.
-- Example: first_name and last_name are separate columns in students table.
-- Hypothetical violation: if we stored phone numbers as '9876543210, 8765432109'
-- in one column, that would break 1NF as it has multiple values in one cell.

-- 2NF ANALYSIS:
-- In enrollments table, composite key = (student_id + course_id).
-- 'grade' depends on BOTH student_id AND course_id together.
-- Example: Arjun (student_id=1) got 'A' in Data Structures (course_id=1).
-- grade cannot be determined by student_id alone or course_id alone.
-- So 2NF is satisfied. ✅

-- 3NF ANALYSIS:
-- No transitive dependencies exist in any table.
-- Example: dept_name depends on department_id, not on student_id.
-- So dept_name is stored in departments table only, not in students table.
-- If we stored dept_name in students table:
-- student_id → department_id → dept_name (transitive dependency!) ❌
-- Current design: students stores only department_id. 3NF satisfied. ✅

-- ================================================
-- TASK 3: ALTER TABLE
-- ================================================

-- Step 10: Add phone_number column
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Verify
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'students';

-- Step 11: Add max_seats column
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- Verify
SELECT * FROM courses;

-- Step 12: Add CHECK constraint on grade
ALTER TABLE enrollments
ADD CONSTRAINT chk_grade
CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

-- Step 13: Rename hod_name to head_of_dept
ALTER TABLE departments RENAME COLUMN hod_name TO head_of_dept;

-- Verify
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'departments';

-- Step 14: Drop phone_number column
ALTER TABLE students DROP COLUMN phone_number;

-- Verify
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'students';

-- ================================================
-- HANDS-ON 1 COMPLETE! ✅
-- ================================================