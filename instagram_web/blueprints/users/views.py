import os
from flask import Blueprint, session, escape, render_template, Flask, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager
from flask_login import login_user, login_required, logout_user

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

    user = User.get_or_none(User.username == submitted_username and User.email == submitted_email)

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
        login_user(user) #logs in user and create cookie
        flash('Successfully Logged In')
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
    pass


@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    return render_template('users/index.html')
    # return 'You are not logged in'
    # return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@users_blueprint.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template('home.html')