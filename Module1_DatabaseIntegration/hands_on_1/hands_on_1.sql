-- ============================================================
-- Digital Nurture 5.0 | Module 3: Database Integration
-- Hands-On 1: Schema Design, DDL & Normalisation
-- ============================================================

-- TASK 1: Create the Database and Tables
-- Run this in psql after connecting to college_db

-- Step 1: Create departments table first (other tables reference it)
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    dept_name     VARCHAR(100) NOT NULL,
    hod_name      VARCHAR(100),
    budget        DECIMAL(12, 2)
);

-- Step 2: Create students table
CREATE TABLE students (
    student_id      SERIAL PRIMARY KEY,
    first_name      VARCHAR(50) NOT NULL,
    last_name       VARCHAR(50) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT REFERENCES departments(department_id),
    enrollment_year INT
);

-- Step 3: Create courses table
CREATE TABLE courses (
    course_id    SERIAL PRIMARY KEY,
    course_name  VARCHAR(150) NOT NULL,
    course_code  VARCHAR(20) UNIQUE,
    credits      INT,
    department_id INT REFERENCES departments(department_id)
);

-- Step 4: Create enrollments table
CREATE TABLE enrollments (
    enrollment_id   SERIAL PRIMARY KEY,
    student_id      INT REFERENCES students(student_id),
    course_id       INT REFERENCES courses(course_id),
    enrollment_date DATE,
    grade           CHAR(2)
);

-- Step 5: Create professors table
CREATE TABLE professors (
    professor_id  SERIAL PRIMARY KEY,
    prof_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(100) UNIQUE,
    department_id INT REFERENCES departments(department_id),
    salary        DECIMAL(10, 2)
);

-- Verify tables were created
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- ============================================================
-- TASK 2: Verify Normalisation (Analysis as SQL Comments)
-- ============================================================

-- 1NF (First Normal Form) Analysis:
-- Each column holds atomic (single) values.
-- For example, a student has ONE email, ONE department_id.
-- Violation example: if we stored "Physics,Chemistry" in one
-- course_name column, that would BREAK 1NF.
-- Our schema stores one value per column — 1NF is satisfied.

-- 2NF (Second Normal Form) Analysis:
-- All non-key columns depend on the ENTIRE primary key.
-- In enrollments: primary key is enrollment_id (surrogate).
-- Candidate key is (student_id, course_id).
-- grade depends on BOTH student AND course — this is correct.
-- If we stored student first_name in enrollments, that would
-- depend only on student_id, not on the full key — 2NF violation.
-- Our design keeps student data in students table — 2NF is satisfied.

-- 3NF (Third Normal Form) Analysis:
-- No transitive dependencies (non-key column depending on another
-- non-key column rather than directly on the primary key).
-- If we stored dept_name IN the students table, then:
--   student_id → department_id → dept_name
-- dept_name would transitively depend on student_id via dept_id.
-- We removed this by putting dept_name only in departments table.
-- Our design has no transitive dependencies — 3NF is satisfied.

-- ============================================================
-- TASK 3: Alter and Extend the Schema
-- ============================================================

-- Step 10: Add phone_number column to students
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Verify:
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'students' ORDER BY ordinal_position;

-- Step 11: Add max_seats column to courses
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- Step 12: Add CHECK constraint to enrollments for valid grades
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade
    CHECK (grade IN ('A', 'B', 'C', 'D', 'F') OR grade IS NULL);

-- Step 13: Rename hod_name to head_of_dept in departments
-- PostgreSQL syntax:
ALTER TABLE departments RENAME COLUMN hod_name TO head_of_dept;

-- Verify the rename:
SELECT column_name FROM information_schema.columns
WHERE table_name = 'departments';

-- Step 14: Drop the phone_number column (schema rollback)
ALTER TABLE students DROP COLUMN phone_number;

-- Final verification — show all table structures:
\d departments
\d students
\d courses
\d enrollments
\d professors