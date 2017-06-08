import os, sys
from imp import reload

from app import create_app
from flask_script import Manager, Shell

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

app = create_app(os.getenv('BLOG_CONFIG') or 'default')
manage = Manager(app)

def make_shell_context():
    return dict(app=app)
manage.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manage.run()