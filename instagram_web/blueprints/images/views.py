from ...util.helpers import *
import os
from flask import Blueprint, session, escape, render_template, Flask, request, redirect, flash, url_for
from models.user import User
from models.images import Image
# from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import login_manager, app
from flask_login import login_user, login_required, logout_user, current_user
from config import S3_BUCKET

app.config['DROPZONE_REDIRECT_VIEW'] = 'images.results'
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_by_id(user_id)



images_blueprint = Blueprint('images',
                             __name__,
                             template_folder='templates')


@images_blueprint.route('/<id>/share', methods=['GET'])
@login_required
def share(id):
    user = User.get_by_id(id)
    return render_template('images/share.html', user=user)


@images_blueprint.route('/<id>/upload-photos', methods=['POST'])
@login_required
def upload_photos(id):
    if request.method == 'POST':
        
        file_obj = request.files
        print(len(file_obj))
        user=User.get_or_none(User.id == id)
        
        for f in file_obj:
            file = request.files.get(f)
            
            # file.filename = secure_filename(file.filename)

            if upload_file_to_s3(file, S3_BUCKET): 
                image = Image(file_path=file.filename, user=user)
                if image.save():
                    flash(f'Successfully saved image {file.filename} in database')
                    # return redirect(url_for('images.results'))
                else:
                    flash(f'Image {file.filename} could not be saved.')
                    # return redirect(url_for('images.share', id=id))
        return redirect(url_for('images.results', id = user.id))

# @images_blueprint.route('/results/<id>', methods=['GET'])
# @login_required
# def results(id):
#     # user = User.get_by_id(id)
#     user=User.get_or_none(User.id == id)
#     return render_template('/images/results.html', user = user)

@images_blueprint.route('/results', methods=['GET'])
@login_required
def results():
    return render_template('/images/results.html')


