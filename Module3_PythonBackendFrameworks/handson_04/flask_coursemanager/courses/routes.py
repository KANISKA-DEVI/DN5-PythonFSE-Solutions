from flask import Blueprint, jsonify, request

# Blueprint — groups all /api/courses routes
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory data store for this exercise (no DB yet — added in HO5)
courses_store = [
    {'id': 1, 'name': 'Data Structures & Algorithms', 'code': 'CS101', 'credits': 4},
    {'id': 2, 'name': 'Database Management Systems',  'code': 'CS102', 'credits': 3},
    {'id': 3, 'name': 'Object Oriented Programming',  'code': 'CS103', 'credits': 4},
]
next_id = 4

def make_success_response(data, status_code=200):
    """Always return a consistent JSON envelope."""
    return jsonify({'status': 'success', 'data': data}), status_code

def make_error_response(message, status_code=400):
    return jsonify({'status': 'error', 'message': message}), status_code


# GET /api/courses/ — list all courses
@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_success_response(courses_store)


# POST /api/courses/ — create a new course
@courses_bp.route('/', methods=['POST'])
def create_course():
    global next_id
    data = request.get_json()

    if data is None:
        return make_error_response('Request body must be JSON with Content-Type: application/json')

    # Validate required fields
    required = ['name', 'code', 'credits']
    missing  = [f for f in required if f not in data]
    if missing:
        return make_error_response(f"Missing required fields: {', '.join(missing)}")

    new_course = {
        'id':      next_id,
        'name':    data['name'],
        'code':    data['code'],
        'credits': data['credits'],
    }
    courses_store.append(new_course)
    next_id += 1

    return make_success_response(new_course, 201)


# GET /api/courses/<id>/ — get one course
@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        return make_error_response(f'Course with id {course_id} not found', 404)
    return make_success_response(course)


# PUT /api/courses/<id>/ — update a course
@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        return make_error_response(f'Course with id {course_id} not found', 404)

    data = request.get_json()
    if data is None:
        return make_error_response('Request body must be JSON')

    course.update({k: v for k, v in data.items() if k in ['name', 'code', 'credits']})
    return make_success_response(course)


# DELETE /api/courses/<id>/ — delete a course
@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global courses_store
    original_len  = len(courses_store)
    courses_store = [c for c in courses_store if c['id'] != course_id]

    if len(courses_store) == original_len:
        return make_error_response(f'Course with id {course_id} not found', 404)

    return jsonify({'status': 'success', 'message': f'Course {course_id} deleted'}), 200