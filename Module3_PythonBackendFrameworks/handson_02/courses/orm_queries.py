# ============================================================
# Hands-On 2: Django ORM Queries Demo
# Run with: python manage.py shell < courses/orm_queries.py
# OR paste each block into: python manage.py shell
# ============================================================
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')
django.setup()

from django.db.models import Count, Avg, F
from courses.models import Department, Course, Student, Enrollment

# --- Insert sample data ---
dept_cs, _ = Department.objects.get_or_create(name='Computer Science', defaults={'head_of_dept':'Dr. Ramesh Kumar', 'budget':850000})
dept_ec, _ = Department.objects.get_or_create(name='Electronics',      defaults={'head_of_dept':'Dr. Priya Nair',   'budget':620000})

course1, _ = Course.objects.get_or_create(code='CS101', defaults={'name':'Data Structures & Algorithms', 'credits':4, 'department':dept_cs})
course2, _ = Course.objects.get_or_create(code='CS102', defaults={'name':'Database Management Systems',  'credits':3, 'department':dept_cs})
course3, _ = Course.objects.get_or_create(code='EC101', defaults={'name':'Circuit Theory',               'credits':3, 'department':dept_ec})

s1, _ = Student.objects.get_or_create(email='arjun@college.edu',  defaults={'first_name':'Arjun',  'last_name':'Mehta',  'department':dept_cs, 'enrollment_year':2022})
s2, _ = Student.objects.get_or_create(email='priya@college.edu',  defaults={'first_name':'Priya',  'last_name':'Suresh', 'department':dept_cs, 'enrollment_year':2022})
s3, _ = Student.objects.get_or_create(email='rohan@college.edu',  defaults={'first_name':'Rohan',  'last_name':'Verma',  'department':dept_ec, 'enrollment_year':2021})

Enrollment.objects.get_or_create(student=s1, course=course1, defaults={'grade':'A'})
Enrollment.objects.get_or_create(student=s1, course=course2, defaults={'grade':'B'})
Enrollment.objects.get_or_create(student=s2, course=course1, defaults={'grade':'B'})
Enrollment.objects.get_or_create(student=s3, course=course3, defaults={'grade':'A'})

print("Data inserted.")

# Query 17: Filter with double underscore (ForeignKey traversal)
cs_courses = Course.objects.filter(department__name='Computer Science')
print(f"\nCS Courses: {list(cs_courses)}")

# Query 18: annotate — count courses per department
dept_counts = Department.objects.annotate(course_count=Count('courses'))
for d in dept_counts:
    print(f"{d.name}: {d.course_count} courses")

# Query 19: select_related — single SQL JOIN query
students = Student.objects.select_related('department').all()
for s in students:
    print(f"{s.first_name} — {s.department.name}")

# Query 20: F() — increase all budgets by 10% in the database
Department.objects.update(budget=F('budget') * 1.1)
print("\nBudgets increased by 10%")
for d in Department.objects.all():
    print(f"  {d.name}: {d.budget}")