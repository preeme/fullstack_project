from flask import Blueprint, redirect, render_template, url_for, request, flash, jsonify
from project.models import User, Location
from project.users.forms import UserForm, LoginForm
from project import db
from sqlalchemy.exc import IntegrityError
from functools import wraps
from flask_login import login_user, logout_user, current_user, login_required

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder = 'templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.login'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/')
def index():
    return render_template('users/home.html')
@users_blueprint.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['username'], form.data['password'], form.data['email'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            flash("Username already taken!")
            render_template('users/signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('users/signup.html', form=form)

@users_blueprint.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            logged_in_user = User.authenticate(form.username.data, form.password.data)
            if logged_in_user:
                login_user(logged_in_user)
                flash("You are now logged in!")
                return redirect(url_for('locations.new', user_id=logged_in_user.id))
        flash("Invalid Login")
    return render_template('users/login.html', form=form)

@users_blueprint.route('/<int:id>/edit')
@login_required
@ensure_correct_user
def edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)
    return render_template('users/edit.html', form=form, user=user)

@users_blueprint.route('/<int:id>', methods=["GET", "PATCH", "DELETE"])
@ensure_correct_user
@login_required
def show(id):
    user = User.query.get(id)
    form = UserForm(obj=user)
    if request.method == b"PATCH" and form.validate():
        user.username = form.data['username']
        user.password = form.data['password']
        user.email = form.data['email']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index.html'))
    return redirect(url_for('users.edit', form=form, id=user.id))
    if request.method == b"DELETE":
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for('users.signup'))
    return redirect('users/index.html')

@users_blueprint.route('/logout')
@login_required
def logout():
    flash("Logged out!")
    logout_user()
    return redirect(url_for('users.login'))

@users_blueprint.route('/data', methods=["GET"])
def data():
    user_locations = Location.query.all()
    locations = []
    for l in user_locations:
        locations.append(dict(lat=l.lat, lng=l.lng))
    return jsonify(locations)
