from app import app, manager
from flask_migrate import MigrateCommand

@manager.command
def runserver():
    app.run(host = '0.0.0.0')

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
