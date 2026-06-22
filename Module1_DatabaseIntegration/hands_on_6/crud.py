# ============================================================
# Hands-On 6: SQLAlchemy ORM — CRUD & Eager Loading
# File: crud.py
# Location: C:\DigitalNurture5\Module1_DatabaseIntegration\hands_on_6\
# ============================================================

from datetime import date
from sqlalchemy.orm import joinedload
from models import Department, Student, Course, Enrollment, Professor, SessionLocal

session = SessionLocal()

# ============================================================
# INSERT Operations
# ============================================================

print("\n=== INSERTING DATA ===")

# Insert 3 Departments
dept1 = Department(dept_name="Computer Science", head_of_dept="Dr. Ramesh Kumar", budget=850000.00)
dept2 = Department(dept_name="Electronics",      head_of_dept="Dr. Priya Nair",   budget=620000.00)
dept3 = Department(dept_name="Mechanical",       head_of_dept="Dr. Suresh Iyer",  budget=540000.00)

session.add_all([dept1, dept2, dept3])
session.commit()
print(f"Inserted departments: {dept1}, {dept2}, {dept3}")

# Insert 5 Students
students_data = [
    Student(first_name="Arjun",  last_name="Mehta",  email="arjun.mehta@college.edu",  department_id=dept1.department_id, enrollment_year=2022),
    Student(first_name="Priya",  last_name="Suresh", email="priya.suresh@college.edu", department_id=dept1.department_id, enrollment_year=2022),
    Student(first_name="Rohan",  last_name="Verma",  email="rohan.verma@college.edu",  department_id=dept2.department_id, enrollment_year=2021),
    Student(first_name="Sneha",  last_name="Patel",  email="sneha.patel@college.edu",  department_id=dept3.department_id, enrollment_year=2023),
    Student(first_name="Vikram", last_name="Das",    email="vikram.das@college.edu",   department_id=dept1.department_id, enrollment_year=2022),
]
session.add_all(students_data)
session.commit()
print(f"Inserted {len(students_data)} students")

# Insert 3 Courses
courses_data = [
    Course(course_name="Data Structures & Algorithms", course_code="CS101", credits=4, department_id=dept1.department_id),
    Course(course_name="Database Management Systems",  course_code="CS102", credits=3, department_id=dept1.department_id),
    Course(course_name="Circuit Theory",               course_code="EC101", credits=3, department_id=dept2.department_id),
]
session.add_all(courses_data)
session.commit()
print(f"Inserted {len(courses_data)} courses")

# Insert 4 Enrollments
enrollments_data = [
    Enrollment(student_id=students_data[0].student_id, course_id=courses_data[0].course_id, enrollment_date=date(2022, 7, 1), grade="A"),
    Enrollment(student_id=students_data[0].student_id, course_id=courses_data[1].course_id, enrollment_date=date(2022, 7, 1), grade="B"),
    Enrollment(student_id=students_data[1].student_id, course_id=courses_data[0].course_id, enrollment_date=date(2022, 7, 1), grade="B"),
    Enrollment(student_id=students_data[2].student_id, course_id=courses_data[2].course_id, enrollment_date=date(2021, 7, 1), grade="A"),
]
session.add_all(enrollments_data)
session.commit()
print(f"Inserted {len(enrollments_data)} enrollments")

# ============================================================
# READ Operations
# ============================================================

print("\n=== READING DATA ===")

# Query 83: Students in Computer Science department using JOIN + filter
cs_students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)
print("\nComputer Science students:")
for s in cs_students:
    print(f"  {s}")

# ============================================================
# N+1 Problem Demo — READ with echo=True
# ============================================================

print("\n--- N+1 Problem: Enrollments WITHOUT eager loading ---")
print("(Watch the SQL log above — it will show multiple separate queries)")
enrollments_lazy = session.query(Enrollment).all()
for e in enrollments_lazy:
    # This triggers a separate SQL query per enrollment to get student data
    _ = e.student.first_name  # Lazy loads student
print(f"Loaded {len(enrollments_lazy)} enrollments with N+1 queries")

# ============================================================
# Query 85: UPDATE — change a student's enrollment year
# ============================================================

print("\n=== UPDATE ===")
student_to_update = session.query(Student).filter_by(email="arjun.mehta@college.edu").first()
if student_to_update:
    old_year = student_to_update.enrollment_year
    student_to_update.enrollment_year = 2023
    session.commit()
    print(f"Updated {student_to_update.first_name}'s enrollment year: {old_year} → {student_to_update.enrollment_year}")

# ============================================================
# Query 86: DELETE — remove an enrollment
# ============================================================

print("\n=== DELETE ===")
enrollment_to_delete = session.query(Enrollment).filter_by(
    student_id=students_data[0].student_id,
    course_id=courses_data[1].course_id
).first()

if enrollment_to_delete:
    print(f"Deleting enrollment: {enrollment_to_delete}")
    session.delete(enrollment_to_delete)
    session.commit()
    print("Enrollment deleted successfully")

remaining = session.query(Enrollment).count()
print(f"Remaining enrollments: {remaining}")

# ============================================================
# TASK 3: Eager Loading to Fix N+1
# ============================================================

print("\n=== TASK 3: EAGER LOADING FIX ===")
print("--- Using joinedload (1 query instead of N+1) ---")

# This single query uses JOINs to fetch everything at once
enrollments_eager = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

print("\nAll enrollments with student and course names:")
for e in enrollments_eager:
    print(f"  {e.student.first_name} {e.student.last_name} | {e.course.course_name} | Grade: {e.grade}")

print(f"\nTotal enrollments loaded: {len(enrollments_eager)}")
print("\nComparison:")
print("  Without joinedload: 1 (enrollments) + N (students) + N (courses) queries")
print("  With joinedload:    1 single JOIN query — much faster!")

session.close()
print("\nSession closed.")