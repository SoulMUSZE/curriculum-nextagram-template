import os
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
app.secret_key = os.getenv('SECRET_KEY')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
#define the default view method to load when user not logged in 
login_manager.login_view = "users.login"

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

