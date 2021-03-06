import os
from app import create_app,db
from config import config
from app.models import User,Role
from flask_migrate import Migrate,upgrade



app=create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate=Migrate(app,db)

@app.shell_context_processor
def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)

def deploy():
	upgrade()
	Role.insert_roles()
	User.add_self_follows()



if __name__=='__main__':
	app.run()