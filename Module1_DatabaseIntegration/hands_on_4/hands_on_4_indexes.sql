-- ============================================================
-- Hands-On 4: Indexes, EXPLAIN & Query Optimisation
-- ============================================================

-- TASK 1: Baseline Performance — No Indexes
-- ============================================================

-- Query 48: EXPLAIN before adding indexes (baseline)
-- This shows the query plan WITHOUT indexes
EXPLAIN ANALYZE
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

-- Save this output in the comment below after running:
/*
BASELINE EXPLAIN OUTPUT (paste yours here after running):
Example output you might see:
   Hash Join  (cost=28.19..38.70 rows=6 width=344)
     Hash Cond: (e.student_id = s.student_id)
     ->  Seq Scan on enrollments e  (cost=0.00..10.10 rows=10 width=8)
     ->  Hash  (cost=28.00..28.00 rows=15 width=276)
           ->  Seq Scan on students s  (cost=0.00..28.00 rows=15...)
                 Filter: (enrollment_year = 2022)
Note: "Seq Scan" = Full Table Scan — reads every row, slow for large tables.
*/

-- ============================================================
-- TASK 2: Add Indexes and Compare Plans
-- ============================================================

-- Query 51: B-Tree index on students.enrollment_year
CREATE INDEX IF NOT EXISTS idx_students_enrollment_year
    ON students(enrollment_year);

-- Query 52: Composite UNIQUE index on enrollments(student_id, course_id)
-- This also prevents duplicate enrollments
CREATE UNIQUE INDEX IF NOT EXISTS idx_enrollments_student_course
    ON enrollments(student_id, course_id);

-- Query 53: Index on courses.course_code
CREATE INDEX IF NOT EXISTS idx_courses_course_code
    ON courses(course_code);

-- Query 54: Re-run EXPLAIN and compare to baseline
EXPLAIN ANALYZE
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

/*
AFTER INDEX EXPLAIN OUTPUT (paste yours here):
You should now see "Index Scan" instead of "Seq Scan" on students
for the enrollment_year filter — this is faster for large tables.
*/

-- Query 55: Partial index — only index unevaluated enrollments (grade IS NULL)
CREATE INDEX IF NOT EXISTS idx_enrollments_ungraded
    ON enrollments(student_id)
    WHERE grade IS NULL;

-- List all indexes on our tables
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Test the UNIQUE index — this should FAIL with a duplicate key error:
-- INSERT INTO enrollments (student_id, course_id, enrollment_date)
-- VALUES (1, 1, CURRENT_DATE);
-- (Uncomment the line above to test, then comment it back)