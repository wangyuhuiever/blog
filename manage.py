import os, sys

COV = None
if os.environ.get('BLOG_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


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

@manage.command
def test(coverage=False):
    '''运行测试单元'''
    if coverage and not os.environ.get('BLOG_COVERAGE'):
        os.environ['BLOG_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('覆盖区域：')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML 版本： file://%s/index.html' % covdir)
        COV.erase()

@manage.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()

@manage.command
def deploy():
    '''Run deployment tasks'''
    from flask_migrate import upgrade
    from app.models import Role, User

    upgrade()

    Role.insert_roles()

    User.add_self_follows()

if __name__ == '__main__':
    manage.run()