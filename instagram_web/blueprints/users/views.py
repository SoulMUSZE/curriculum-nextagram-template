import os
from flask import Blueprint, render_template, Flask, request, redirect, flash, url_for
from models.user import User
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    # breakpoint()

    password = request.form.get('password')
    u = User(
        username = request.form.get('username'),
        email = request.form.get('email'),
        hashed_password =  generate_password_hash(password)
    )

    if u.save():
        flash('Successfully saved in database')
        return redirect(url_for('users.new'))
    else:
        flash('Unable to create new user!')
        return render_template('users/new.html', errors = u.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
