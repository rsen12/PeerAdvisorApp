from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    advisee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    advisor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    pronouns = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    class_year = db.Column(db.Integer())
    internship = db.Column(db.Boolean())
    study_abroad = db.Column(db.Boolean())
    student_research = db.Column(db.Boolean())
    profile_pic = db.Column(db.String(), nullable=True)
    m2u = db.relationship('MajorToUser', backref='user', lazy='dynamic')
    o2u = db.relationship('StudentOrgToUser', backref='user', lazy='dynamic')
    c2u = db.relationship('CourseToUser', backref='user', lazy='dynamic')
    i2u = db.relationship('InterestToUser', backref='user', lazy='dynamic')
    primary_advisor = db.Column(db.Integer, db.ForeignKey('professor.id'))

    advisees = db.relationship('Match', backref='advisee', lazy='dynamic', primaryjoin=id==Match.advisee_id)
    advisors = db.relationship('Match', backref='advisor', lazy='dynamic', primaryjoin=id==Match.advisor_id)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    school = db.Column(db.String(64))
    m2u = db.relationship('MajorToUser', backref='major', lazy='dynamic')

    def __repr__(self):
        return '<Major {}>'.format(self.name)


class MajorToUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(64), unique=True)
    c2u = db.relationship('CourseToUser', backref='course', lazy='dynamic')
    p2c = db.relationship('ProfessorToCourse', backref='course', lazy='dynamic')

    def __repr__(self):
        return '<Course {}>'.format(self.name)


class CourseToUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    department = db.Column(db.String(64))
    p2c = db.relationship('ProfessorToCourse', backref='professor', lazy='dynamic')

    user = db.relationship('User', backref='professor', lazy='dynamic')

    def __repr__(self):
        return '<Professor {}>'.format(self.name)


class ProfessorToCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prof_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    i2u = db.relationship('InterestToUser', backref='interest', lazy='dynamic')

    def __repr__(self):
        return '<Interest {}>'.format(self.name)


class InterestToUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey('interest.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Org(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    o2u = db.relationship('StudentOrgToUser', backref='org', lazy='dynamic')

    def __repr__(self):
        return '<Student Org {}>'.format(self.name)


class StudentOrgToUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_id = db.Column(db.Integer, db.ForeignKey('org.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

