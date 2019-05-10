from ...util.helpers import *
import os
from flask import Blueprint, session, escape, render_template, Flask, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import login_manager, app
from flask_login import login_user, login_required, logout_user, current_user
from config import S3_BUCKET

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    # breakpoint()

    submitted_username = request.form.get('username')
    submitted_email = request.form.get('email')
    submitted_password = request.form.get('password')

    user = User.get_or_none(
        User.username == submitted_username and User.email == submitted_email)

    if user:
        flash('Account already exists. Please Login.')
        return redirect(url_for('users.new'))
    else:
        user = User(
            username=submitted_username,
            email=submitted_email,
            hashed_password=generate_password_hash(submitted_password)
        )
        if user.save():
            flash('Successfully saved in database')
            return redirect(url_for('users.new'))
        else:
            flash('Unable to create new user!')
            return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/login', methods=['GET'])
def login():
    return render_template('users/login.html')


@users_blueprint.route('/login', methods=['POST'])
def authenticate():

    submitted_username = request.form.get('username')
    password_to_check = request.form.get('password')

    user = User.get_or_none(User.username == submitted_username)

    if user and check_password_hash(user.hashed_password, password_to_check):
        login_user(user)  # logs in user and create cookie
        flash('Successfully Logged In')
        # return redirect(url_for('users.edit', id = user.id))
        return redirect(url_for('users.index'))

    flash('Please Check Your Login Details and Try Again')
    return redirect(url_for('users.login'))

    # if not user or not check_password_hash(user.hashed_password, password_to_check):
    #     flash('Please Check Your Login Details and Try Again')
    #     return redirect(url_for('users.login'))

    # login_user(user) #logs in user and create cookie
    # flash('Successfully Logged In')
    # return redirect(url_for('users.index'))
    # if user:
    #     hashed_password = user.hashed_password
    #     result = check_password_hash(hashed_password, password_to_check)
    #     if result:
    #         login_user(user) #logs in user and create cookie
    #         flash('Successfully Logged In')
    #         return redirect(url_for('users.index'))
    #     else:
    #         flash('Wrong Password')
    #         return render_template('users/login.html')
    # else:
    #     flash('Wrong Username')
    #     return render_template('users/login.html')


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('users/profile.html', user=user)
    else:
        return render_template('users/404.html')


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('users/index.html')
    # return 'You are not logged in'
    # return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    if user.id == current_user.id:
        return render_template('users/update.html', user=user)
    else:
        return render_template('users/404.html')


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    email = request.form.get('email')
    newPassword = request.form.get('newPassword')
    description = request.form.get('description')
    oldPassword = request.form.get('oldPassword')

    user = User.get_by_id(id)

    if check_password_hash(user.hashed_password, oldPassword):

        if not email:
            email = user.email

        if newPassword:
            newPasswordHash = generate_password_hash(newPassword)
        else:
            newPasswordHash = user.hashed_password

        if description == 'None':
            description = user.description

        # update the values
        u = User.update(
            email=email,
            hashed_password=newPasswordHash,
            description=description
        ).where(User.id == user.id)

        if u.execute():
            flash('New details successfully updated in database')
            return redirect(url_for('users.show', username=user.username))
        else:
            flash('New details could not be updated.')
            # do something else
            return redirect(url_for('users.edit', id=user.id))
    else:
        flash('Password could not be validated')
        # redirect or flash message
        return redirect(url_for('users.show', username=user.username))


@users_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template('home.html')


@users_blueprint.route('/<id>/edit-photo', methods=['GET'])
@login_required
def edit_photo(id):
    user = User.get_by_id(id)

    if user.id == current_user.id:
        return render_template('users/update_photo.html', user=user)
    else:
        return render_template('users/404.html')


@users_blueprint.route('/<id>/update-photo', methods=['POST'])
@login_required
def update_photo(id):
    
    user = User.get_by_id(id)

    if user.id == current_user.id:
        # A
        if "user_file" not in request.files:
            return "No user_file key in request.files"
        # B
        file = request.files["user_file"]
        """
            These attributes are also available

            file.filename               # The actual name of the file
            file.content_type
            file.content_length
            file.mimetype

        """
        # C.
        if file.filename == "":
            return "Please select a file"
        # D.
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            
            if upload_file_to_s3(file, S3_BUCKET):
                u = User.update(profile_photo_path = file.filename).where(User.id == user.id)
                if u.execute():
                    return redirect(url_for('users.show', username=user.username))
                else:
                    flash('New profile photo could not be updated.')
                    return redirect(url_for('users.edit_photo', id=user.id))
        else:
            return redirect(url_for('users.edit_photo', id=user.id))

# A. We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it’s not there, we return an error message.

# B. If the key is in the object, we save it in a variable called file.

# C. We check the filename attribute on the object and if it’s empty, it means the user sumbmitted an empty form, so we return an error message.

# D. Finally we check that there is a file and that it has an allowed filetype (this is what the allowed_file function does, you can check it out in the flask docs).

# If both tests pass, we sanitize the filename using the secure_filename helper function provided by the werkzeurg.security module. Next, we upload the file to our s3 bucket using our own helper function, we store the return value (ie the generated presigned url for the file) in a variable o called output. We end by returning the generated url to the user.

# Note: if one of the tests fail, we just redirect the user to the home page, similar to a refresh
