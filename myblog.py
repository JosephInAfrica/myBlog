import os
from app import create_app,db
from config import config
from app.models import User,Role
from flask_migrate import Migrate,upgrade
from dotenv import load_dotenv


dotenv_path=os.path.join(os.path.dirname(__file__),'myblog.env')
# print(dotenv_path)
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print('done loading environs')



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