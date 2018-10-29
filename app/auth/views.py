# -*- coding: utf-8 -*
from flask import render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,RegisterForm,ChangePasswordForm
from . import auth
from ..models import User
from ..email import send_email
from .. import db


@auth.route('/login',methods=['POST','GET'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		else:
			flash('Password or Email not correct.')
	return render_template('auth/login.html',form=form)



@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have logged out.')
	return redirect(url_for('main.index'))



@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		user=User(username=form.username.data,password=form.password.data,email=form.email.data)
		db.session.add(user)
		token=user.generate_confirmation_token()
		send_email(user.email,'Confirm your account','auth/email/confirm',user=user,token=token)
		flash('A confrimation email has been sent to you.')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html',form=form)



@auth.route('/confirm')
@login_required
def resend_confirmation():
	token=current_user.generate_confirmation_token()
	send_email(current_user.email,'Confirm your account','auth/email/confirm',user=current_user,token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.index'))



@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks.')
	else:
		flash('The confirmation link is valid')
	return redirect(url_for('main.index'))
# 不明白这里的flash 如何运行，如果没有 先载入main.index



@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form=ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password=form.password.data
			db.session.add(current_user)
			flash('Your password has been updated.')
			return redirect(url_for('main.index'))
		else:
			flash('Invalid password')
	return render_template('auth/change_password.html',form=form)



@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5]!='auth.' and request.endpoint!='static':
			return redirect(url_for('auth.unconfirmed'))



@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')




















