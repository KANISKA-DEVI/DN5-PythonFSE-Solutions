# ============================================================
# Student Service — owns all student/enrollment data (port 5002)
# Calls Course Service to verify course exists before enrolling
# ============================================================
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

COURSE_SERVICE_URL = "http://localhost:5001"

students_db    = {
    1: {"id": 1, "first_name": "Arjun",  "last_name": "Mehta",  "email": "arjun@college.edu"},
    2: {"id": 2, "first_name": "Priya",  "last_name": "Suresh", "email": "priya@college.edu"},
    3: {"id": 3, "first_name": "Rohan",  "last_name": "Verma",  "email": "rohan@college.edu"},
}
enrollments_db = []


@app.route('/api/students/', methods=['GET'])
def get_students():
    return jsonify(list(students_db.values()))


@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": f"Student {student_id} not found"}), 404
    return jsonify(student)


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    """
    Enrollment requires verifying the course exists in Course Service.
    This is synchronous inter-service communication using HTTP.
    """
    student = students_db.get(student_id)
    if not student:
        return jsonify({"error": f"Student {student_id} not found"}), 404

    data      = request.get_json() or {}
    course_id = data.get('course_id')
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    # Call Course Service to verify the course exists
    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}", timeout=5)
        if response.status_code == 404:
            return jsonify({"error": f"Course {course_id} not found in Course Service"}), 404
        course = response.json()
    except requests.ConnectionError:
        # Course Service is unavailable — return 503
        return jsonify({
            "error": "Course Service is currently unavailable. Please try again later.",
            "service": "course_service"
        }), 503
    except requests.Timeout:
        return jsonify({"error": "Course Service timed out"}), 504

    # Create enrollment
    enrollment = {
        "student_id":  student_id,
        "course_id":   course_id,
        "course_name": course.get('name'),
        "student_name": f"{student['first_name']} {student['last_name']}"
    }
    enrollments_db.append(enrollment)

    return jsonify({
        "message":    "Enrollment successful",
        "enrollment": enrollment
    }), 201


@app.route('/api/enrollments/', methods=['GET'])
def get_enrollments():
    return jsonify(enrollments_db)


if __name__ == '__main__':
    print("Student Service running on port 5002")
    app.run(port=5002, debug=True)