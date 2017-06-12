import os, sys
from imp import reload
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Permission, Post, Follow, Comment

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = create_app(os.getenv('BLOG_CONFIG') or 'default')
manage = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Comment=Comment,
                Permission=Permission, Post=Post, Follow=Follow)
manage.add_command('shell', Shell(make_context=make_shell_context))
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manage.run()