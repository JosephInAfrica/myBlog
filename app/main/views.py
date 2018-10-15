from flask import render_template,url_for,redirect,session
from . import main
from .form import nameForm
from ..decorators import admin_required,permission_required
from ..models import Permission
from flask_login import login_required


@main.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return 'for admins only!'


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return 'For comment moderators!'

@main.route('/user/<username>')
def user(username):
	user=User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('user.html',user=user)
