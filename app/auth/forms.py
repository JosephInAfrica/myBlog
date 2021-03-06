from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Required, Length, Email,EqualTo
from ..models import User



class LoginForm(FlaskForm):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	password=PasswordField('Input your password',validators=[Required()])
	remember_me=BooleanField('Keep me logged in.')
	submit=SubmitField('Log in')


class RegisterForm(FlaskForm):
	username=StringField('Name',validators=[Required(),Length(1,64)])
	email=StringField('Email',validators=[Required(),Email(),Length(1,64)])
	password=PasswordField('Input your password',validators=[Required()])
	password2=PasswordField('your password again',validators=[Required(),EqualTo('password',message='passwords has to match')])
	submit=SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already taken.')

class ChangePasswordForm(FlaskForm):
	old_password=PasswordField('Old Passowrd',validators=[Required()])
	password=PasswordField('New Passowrd',validators=[Required(),EqualTo('password2',message='Passwords must match')])
	password2=PasswordField('Confirm your password',validators=[Required()])
	submit=SubmitField('Update password')

	
