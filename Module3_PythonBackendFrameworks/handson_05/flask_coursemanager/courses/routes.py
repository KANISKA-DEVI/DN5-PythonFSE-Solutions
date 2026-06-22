from flask import Blueprint, jsonify, request
from extensions import db
from courses.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@courses_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify({'status': 'success', 'data': [c.to_dict() for c in courses]})


@courses_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'JSON body required'}), 400

    missing = [f for f in ['name', 'code', 'credits'] if f not in data]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing fields: {missing}'}), 400

    course = Course(name=data['name'], code=data['code'], credits=data['credits'],
                    department_id=data.get('department_id'))
    db.session.add(course)
    db.session.commit()
    return jsonify({'status': 'success', 'data': course.to_dict()}), 201


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({'status': 'success', 'data': course.to_dict()})


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data   = request.get_json() or {}
    for field in ['name', 'code', 'credits']:
        if field in data:
            setattr(course, field, data[field])
    db.session.commit()
    return jsonify({'status': 'success', 'data': course.to_dict()})


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'status': 'success', 'message': f'Course {course_id} deleted'})


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_enrolled_students(course_id):
    course   = Course.query.get_or_404(course_id)
    students = Student.query.join(Enrollment).filter(Enrollment.course_id == course_id).all()
    return jsonify({'status': 'success', 'data': [s.to_dict() for s in students]})