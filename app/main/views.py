from flask import render_template,url_for,redirect,session
from . import main
from .form import nameForm

@main.route('/',methods=['GET','POST'])
def index():
	form=nameForm()
	if form.validate_on_submit():
		session['name']=form.name.data
		return redirect(url_for('main.index'))
	return render_template('index.html',form=form,name=session.get('name') or 'Stranger')


