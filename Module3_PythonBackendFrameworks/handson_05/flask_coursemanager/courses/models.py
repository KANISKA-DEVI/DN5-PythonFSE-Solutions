from extensions import db


class Department(db.Model):
    __tablename__ = 'departments'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget       = db.Column(db.Numeric(12, 2))
    courses      = db.relationship('Course',  back_populates='department', lazy='dynamic')
    students     = db.relationship('Student', back_populates='department', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'head_of_dept': self.head_of_dept, 'budget': float(self.budget or 0)}


class Course(db.Model):
    __tablename__ = 'courses'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    code          = db.Column(db.String(20), unique=True)
    credits       = db.Column(db.Integer, default=3)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department    = db.relationship('Department', back_populates='courses')
    enrollments   = db.relationship('Enrollment', back_populates='course', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code, 'credits': self.credits, 'department_id': self.department_id}


class Student(db.Model):
    __tablename__   = 'students'
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    department_id   = db.Column(db.Integer, db.ForeignKey('departments.id'))
    enrollment_year = db.Column(db.Integer)
    department      = db.relationship('Department', back_populates='students')
    enrollments     = db.relationship('Enrollment', back_populates='student', lazy='dynamic')

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'department_id': self.department_id}


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id            = db.Column(db.Integer, primary_key=True)
    student_id    = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id     = db.Column(db.Integer, db.ForeignKey('courses.id'))
    grade         = db.Column(db.String(2))
    student       = db.relationship('Student', back_populates='enrollments')
    course        = db.relationship('Course',  back_populates='enrollments')

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id, 'course_id': self.course_id, 'grade': self.grade}