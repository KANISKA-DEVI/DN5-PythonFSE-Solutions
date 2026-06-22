# ============================================================
# Course Service — owns all course data (port 5001)
# ============================================================
from flask import Flask, jsonify, request

app = Flask(__name__)

# Course Service owns its own in-memory data store
# In production this would be its own separate database
courses_db = {
    1: {"id": 1, "name": "Data Structures & Algorithms", "code": "CS101", "credits": 4},
    2: {"id": 2, "name": "Database Management Systems",  "code": "CS102", "credits": 3},
    3: {"id": 3, "name": "Object Oriented Programming",  "code": "CS103", "credits": 4},
}


@app.route('/api/courses/', methods=['GET'])
def get_courses():
    return jsonify(list(courses_db.values()))


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = courses_db.get(course_id)
    if not course:
        return jsonify({"error": f"Course {course_id} not found"}), 404
    return jsonify(course)


@app.route('/api/courses/', methods=['POST'])
def create_course():
    data  = request.get_json()
    new_id = max(courses_db.keys()) + 1
    course = {"id": new_id, **data}
    courses_db[new_id] = course
    return jsonify(course), 201


if __name__ == '__main__':
    print("Course Service running on port 5001")
    app.run(port=5001, debug=True)