-- ============================================================
-- Hands-On 3: Subqueries, Views & Transactions
-- ============================================================

-- TASK 1: Subqueries
-- ============================================================

-- Query 35: Students enrolled in MORE courses than the average
SELECT
    s.first_name,
    s.last_name,
    COUNT(e.enrollment_id) AS enrolled_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name
HAVING COUNT(e.enrollment_id) > (
    SELECT AVG(enrollment_count)
    FROM (
        SELECT COUNT(enrollment_id) AS enrollment_count
        FROM enrollments
        GROUP BY student_id
    ) AS avg_table
)
ORDER BY enrolled_count DESC;

-- Query 36: Courses where ALL enrolled students got 'A'
-- (using NOT EXISTS to exclude courses with non-A grades)
SELECT c.course_name, c.course_code
FROM courses c
WHERE EXISTS (
    SELECT 1 FROM enrollments e WHERE e.course_id = c.course_id
)
AND NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
    AND (e.grade <> 'A' OR e.grade IS NULL)
);

-- Query 37: Professor with highest salary in each department (correlated subquery)
SELECT
    p.prof_name,
    p.salary,
    d.dept_name
FROM professors p
JOIN departments d ON p.department_id = d.department_id
WHERE p.salary = (
    SELECT MAX(p2.salary)
    FROM professors p2
    WHERE p2.department_id = p.department_id
)
ORDER BY d.dept_name;

-- Query 38: Departments where avg salary > 85,000 (derived table in FROM)
SELECT dept_name, avg_salary
FROM (
    SELECT
        d.dept_name,
        ROUND(AVG(p.salary), 2) AS avg_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_avg
WHERE avg_salary > 85000;

-- ============================================================
-- TASK 2: Creating and Using Views
-- ============================================================

-- Drop views if they exist (safe re-run)
DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

-- Query 39: View — student enrollment summary with GPA
CREATE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    s.first_name || ' ' || s.last_name AS full_name,
    d.dept_name AS department,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4.0
            WHEN 'B' THEN 3.0
            WHEN 'C' THEN 2.0
            WHEN 'D' THEN 1.0
            WHEN 'F' THEN 0.0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
LEFT JOIN departments d  ON s.department_id = d.department_id
LEFT JOIN enrollments e  ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- Query 40: View — course statistics
CREATE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4.0
            WHEN 'B' THEN 3.0
            WHEN 'C' THEN 2.0
            WHEN 'D' THEN 1.0
            WHEN 'F' THEN 0.0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

-- Query 41: Students with GPA above 3.0
SELECT full_name, department, gpa
FROM vw_student_enrollment_summary
WHERE gpa > 3.0
ORDER BY gpa DESC;

-- Query 42: Try to UPDATE through the view
-- This will fail because the view joins multiple tables
-- UPDATE vw_student_enrollment_summary SET department = 'Maths' WHERE student_id = 1;
-- ERROR: cannot update multi-table view
-- Multi-table views are read-only — PostgreSQL enforces this.
-- You must update the underlying base table directly.
SELECT * FROM vw_course_stats;

-- ============================================================
-- TASK 3: Stored Procedures and Transactions
-- ============================================================

-- Create a log table for department transfers
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id        SERIAL PRIMARY KEY,
    student_id    INT,
    old_dept_id   INT,
    new_dept_id   INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Query 44: Function to enroll a student (PostgreSQL uses functions, not stored procs)
CREATE OR REPLACE FUNCTION fn_enroll_student(
    p_student_id INT,
    p_course_id  INT,
    p_date       DATE
) RETURNS TEXT AS $$
BEGIN
    -- Check for duplicate enrollment
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        RETURN 'ERROR: Student is already enrolled in this course.';
    END IF;

    -- Insert the enrollment
    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (p_student_id, p_course_id, p_date);

    RETURN 'SUCCESS: Student enrolled successfully.';
END;
$$ LANGUAGE plpgsql;

-- Test the function:
SELECT fn_enroll_student(1, 3, '2022-07-01');  -- Should succeed (new enrollment)
SELECT fn_enroll_student(1, 1, '2022-07-01');  -- Should return ERROR (duplicate)

-- Query 45: Transaction — Transfer student between departments
BEGIN;

    -- Step 1: Log the transfer BEFORE making the change
    INSERT INTO department_transfer_log (student_id, old_dept_id, new_dept_id)
    SELECT student_id, department_id, 2
    FROM students
    WHERE student_id = 1;

    -- Step 2: Update the student's department
    UPDATE students
    SET department_id = 2
    WHERE student_id = 1;

COMMIT;

-- Verify the transfer
SELECT first_name, last_name, department_id FROM students WHERE student_id = 1;
SELECT * FROM department_transfer_log;

-- Query 47: SAVEPOINT demonstration
BEGIN;

    -- Insert first enrollment record
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (2, 2, CURRENT_DATE, 'A');

    -- Create a savepoint after the first insert
    SAVEPOINT after_first_insert;

    -- Attempt a second insert that we will deliberately roll back
    INSERT INTO enrollments (student_id, course_id, enrollment_date, grade)
    VALUES (2, 4, CURRENT_DATE, 'B');

    -- Rollback to the savepoint (only the second insert is undone)
    ROLLBACK TO SAVEPOINT after_first_insert;

    -- The first insert is still pending — commit it
COMMIT;

-- Verify: student 2 should have the first new enrollment but NOT the second
SELECT * FROM enrollments WHERE student_id = 2 ORDER BY enrollment_id;