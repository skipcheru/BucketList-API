import os
from app import create_app, db
from app.models import User,  BucketList, Item
from flask_script import Manager, Shell, prompt_bool
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, BucketList=BucketList, Item=Item)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop db?"):
        db.drop_all()


@manager.command
def initdb():
    db.create_all()


cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    cov = coverage.coverage(
        branch=True, include='app/*?views.py', omit='app/models.py')
    cov.start()


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        cov.erase()

if __name__ == '__main__':
    manager.run()
