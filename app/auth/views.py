from flask import render_template,request,redirect,url_for,flash
from flask_login import login_user,logout_user,current_user,login_required
from .forms import LoginForm,RegisterForm
from . import auth
from ..models import User
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
		flash('Now you can login')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html',form=form)
