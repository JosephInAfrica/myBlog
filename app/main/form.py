from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class nameForm(FlaskForm):
	name=StringField('Your name plaes',validators=[Required()])
	submit=SubmitField('Submit')

