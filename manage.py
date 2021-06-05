from app import app, manager
from flask_migrate import MigrateCommand

@manager.command
def runserver():
    app.run()

@manager.command
def runserver_secure():
    app.run(ssl_context = "adhoc")

@manager.command
def get_app():
    return app

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
