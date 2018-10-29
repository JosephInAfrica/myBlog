import os
from app import create_app,db
from config import config
from flask_script import Manager, Shell,Server
from flask_migrate import Migrate,MigrateCommand
from app.models import User,Role

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate=Migrate(app,db)


def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
manager.add_command('runserver',Server(host='localhost',port=8000))


if __name__=='__main__':
	manager.run()