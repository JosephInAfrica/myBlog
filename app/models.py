from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import UserMixin,AnonymousUserMixin
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app



class Role(db.Model):
	__tablename__='roles'
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(64),unique=True)
	users=db.relationship('User',backref='role',lazy='dynamic')
	default=db.Column(db.Boolean,default=False)
	permissions=db.Column(db.Integer)

	@staticmethod
	def insert_roles():
		roles={
		'User':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES,True),
		'Moderator':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS,False),
		'Administer':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS|Permission.ADMINISTER,False),
		}
		for r in roles:
			role=Role.query.filter_by(name=r).first()
			if role is None:
				role=Role(name=r)
			role.permissions=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()


	def __repr__(self):
		return '<Role %r>'%self.name

class Permission:
	FOLLOW=0x01
	COMMENT=0x02
	WRITE_ARTICLES=0x04
	MODERATE_COMMENTS=0x08
	ADMINISTER=0x80

class User(db.Model,UserMixin):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	email=db.Column(db.String(64),unique=True,index=True)
	username=db.Column(db.String(64),unique=True)
	role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
	password_hash=db.Column(db.String(128))
	confirmed=db.Column(db.Boolean,default=False)

	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		if self.role is None:
			if self.email==current_app.config['ADMIN']:
				self.role=Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				self.role=Role.query.filter_by(default=True).first()


	def generate_confirmation_token(self,expiration=3600):
		s=Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm':self.id})

	def confirm(self,token):
		s=Serializer(current_app.config['SECRET_KEY'])
		try:
			data=s.loads(token)
		except:
			return False
		if data.get('confirm')==self.id:
			self.confirmed=True
			db.session.add(self)
			return True
		else:
			return False

	def can(self,permissions):
		return self.role is not None and (self.role.permissions&permissions)==permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return '<User %r>'%self.username


class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user=AnonymousUser

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))			
