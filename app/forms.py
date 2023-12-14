from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, DateField, SubmitField, PasswordField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class AdviseeForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    pronouns = StringField('Pronouns')
    primary_advisor = SelectMultipleField(u'Primary Advisor(s)', coerce=int)
    student_orgs = SelectMultipleField(u'Student Organization(s)', coerce=int)
    interests = SelectMultipleField(u'Interest(s)', coerce=int)
    class_year = SelectField(u'Class Year', validators=[DataRequired()], choices=[(2028, '2028'), (2027, '2027'), (2026, '2026'), (2025, '2025'), (2024, '2024'), (2023, '2023')], coerce=int)
    major = SelectMultipleField(u'Major', validators=[DataRequired()], coerce=int)
    courses = SelectMultipleField(u'Courses Interested In', validators=[DataRequired()], coerce=int)
    internship = BooleanField('Internship?')
    study_abroad = BooleanField('Study Abroad?')
    student_research = BooleanField('Research Experience?')
    submit = SubmitField('Submit')


class AdvisorForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    pronouns = StringField('Pronouns')
    primary_advisor = SelectField('Primary Advisor')
    student_orgs = SelectMultipleField('Student Organization(s)', coerce=int)
    interests = SelectMultipleField('Interest(s)', coerce=int)
    # preferred_contact_method = SelectField('Preferred Contact Method', choices=[('email', 'Email'), ('text', 'Text')])
    class_year = SelectField('Class Year', validators=[DataRequired()], choices=[(2028, '2028'), (2027, '2027'), (2026, '2026'), (2025, '2025'), (2024, '2024'), (2023, '2023')], coerce=int)
    major = SelectMultipleField('Major', validators=[DataRequired()], coerce=int)
    minor = SelectMultipleField('Minor', validators=[DataRequired()], coerce=int)
    course = SelectMultipleField('Course Taken', validators=[DataRequired()], coerce=int)
    internship = BooleanField('Internship?')
    study_abroad = BooleanField('Study Abroad?')
    student_research = BooleanField('Research Experience?')
    profile_pic = FileField('Profile Picture',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')