from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    # def validate(self, username, password):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is None or not user.check_password(password.data):
    #         raise ValidationError('Invalid username or password')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    gender = StringField('Gender')
    age = StringField('Age')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_surname(self, surname):
        user = User.query.filter_by(username=surname.data).first()
        if user is not None:
            raise ValidationError('Please use a different surname.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
