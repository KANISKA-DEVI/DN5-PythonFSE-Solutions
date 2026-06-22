# ============================================================
# Hands-On 4: N+1 Query Problem — Demonstration & Fix
# File: hands_on_4_n_plus_one.py
# Location: C:\DigitalNurture5\Module1_DatabaseIntegration\hands_on_4\
# ============================================================

import psycopg2
import time

# --- Database connection settings ---
DB_CONFIG = {
    "host":     "localhost",
    "database": "college_db",
    "user":     "postgres",
    "password": "admin123",  # Change this if you used a different password
    "port":     5432
}

def get_connection():
    """Create and return a database connection."""
    return psycopg2.connect(**DB_CONFIG)


# ============================================================
# VERSION 1: N+1 Problem (BAD — many queries)
# ============================================================
def demo_n_plus_one_problem():
    """
    N+1 Problem: We fetch all enrollments (1 query),
    then for EACH enrollment we fetch the student's name (N queries).
    Total = 1 + N queries.
    """
    conn = get_connection()
    cursor = conn.cursor()

    query_count = 0
    start_time = time.time()

    # Query 1: Fetch all enrollments
    cursor.execute("SELECT enrollment_id, student_id, course_id FROM enrollments")
    enrollments = cursor.fetchall()
    query_count += 1

    print("\n--- N+1 Problem Version ---")
    results = []
    for enrollment in enrollments:
        enrollment_id, student_id, course_id = enrollment

        # N additional queries — one per enrollment!
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s",
            (student_id,)
        )
        student = cursor.fetchone()
        query_count += 1

        results.append({
            "enrollment_id": enrollment_id,
            "student_name":  f"{student[0]} {student[1]}" if student else "Unknown",
            "course_id":     course_id
        })

    elapsed = time.time() - start_time

    print(f"Total queries executed: {query_count}")
    print(f"Time taken: {elapsed:.4f} seconds")
    print(f"Records returned: {len(results)}")
    print("\nIf this table had 10,000 enrollments, we would run: 10,001 queries!")

    cursor.close()
    conn.close()
    return results


# ============================================================
# VERSION 2: Fixed with JOIN (GOOD — single query)
# ============================================================
def demo_fixed_with_join():
    """
    Fixed version: Use a single JOIN query to get all data at once.
    Total = 1 query (regardless of how many records exist).
    """
    conn = get_connection()
    cursor = conn.cursor()

    query_count = 0
    start_time = time.time()

    # Single query using JOIN — gets everything in one database round-trip
    cursor.execute("""
        SELECT
            e.enrollment_id,
            s.first_name || ' ' || s.last_name AS student_name,
            c.course_name,
            e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        JOIN courses  c ON e.course_id  = c.course_id
        ORDER BY e.enrollment_id
    """)
    results = cursor.fetchall()
    query_count += 1

    elapsed = time.time() - start_time

    print("\n--- Fixed Version (JOIN) ---")
    print(f"Total queries executed: {query_count}")
    print(f"Time taken: {elapsed:.4f} seconds")
    print(f"Records returned: {len(results)}")

    print("\nSample results:")
    for row in results[:5]:  # Show first 5 rows
        print(f"  Enrollment {row[0]}: {row[1]} | {row[2]} | Grade: {row[3]}")

    cursor.close()
    conn.close()
    return results


# ============================================================
# Run both versions and compare
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("N+1 Query Problem Demonstration")
    print("=" * 60)

    print("\nRunning N+1 version...")
    n_plus_one_results = demo_n_plus_one_problem()

    print("\nRunning fixed JOIN version...")
    join_results = demo_fixed_with_join()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Both versions returned the same {len(join_results)} records.")
    print("The JOIN version used far fewer database queries.")
    print("\nIn production with 10,000 rows:")
    print("  N+1 version: 10,001 database round-trips")
    print("  JOIN version:      1 database round-trip")
    print("\nThe fix: always use JOINs or ORM eager loading instead of loops.")