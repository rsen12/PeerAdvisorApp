from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, PasswordField, BooleanField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class Advisor(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    class_yr = StringField('Class Year', validators=[DataRequired()])
    internship = SelectField('Internship?', validators=[DataRequired()], coerce=int)
    study_abroad = SelectField('Study Abroad?', validators=[DataRequired()], coerce=int)
    research_exp = SelectField('Research Experience?', validators=[DataRequired()], coerce=int)
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