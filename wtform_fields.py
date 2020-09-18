from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User


def invalid_credentials(form, field):
    #  form will be LoginForm
    #  field will be Password

    username_entered = form.username.data
    password_entered = field.data

    #   Checks for valid credentials
    user_object = User.query.filter_by(username = username_entered).first()
    if user_object is None:
        raise ValidationError('Username or password is incorrect')
    elif password_entered != user_object.password:
        raise ValidationError('Username or password is incorrect')


class RegistrationForm(FlaskForm):

    username = StringField('username_label', validators = [
        InputRequired(message = "Username is required"),
        Length(min = 4, max = 25, message = "Username must be between 25 and 4 character")])

    password = PasswordField('password_label', validators = [
        InputRequired(message = "Password is required"),
        Length(min = 6,  message = "Password must be at least 6 characters long")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators = [
        InputRequired(message = "Password confirmation is required"), EqualTo('password', message = "Passwords must match")])

    submit_button = SubmitField()

    def validate_username(self, username):
        user_object = User.query.filter_by(username = username.data).first()
        if user_object:
            raise ValidationError('Username already exists! Select a different username.')


class LoginForm(FlaskForm):

    username = StringField('username_label', validators = [InputRequired(message = 'Username is required')])

    password = PasswordField('pass_label', validators = [InputRequired(message = 'Password is required'), invalid_credentials])

    login_btn = SubmitField('Login')