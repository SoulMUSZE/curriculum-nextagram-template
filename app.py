import os
import config
from flask import Flask
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
# app.secret_key = os.getenv('SECRET_KEY')

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

# @app.route("/sign_up", methods = ['GET'])
# def sign_up():
#     return render_template('signup.html')

# @app.route("/store_form", methods = ['POST'])#endpoint
# def store_form():
#     s = Store(name = request.form.get('name'))

#     if s.save():
#         flash('Successfully saved in database')
#         return redirect(url_for('store'))
#     else:
#         return render_template('store.html', name=request.args['name'])
