from flask import Blueprint, redirect, render_template, url_for, request, flash, jsonify
from flask_login import current_user, login_required
from project import db
from project.models import Location, User
from functools import wraps

locations_blueprint = Blueprint(
  'locations',
  __name__,
  template_folder = 'templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('user_id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.login'))
        return fn(*args, **kwargs)
    return wrapper

@locations_blueprint.route('/', methods=["GET","POST"])
@login_required
def index(user_id):
    if request.method == 'POST':
        new_location = Location(request.form.get('lat'), request.form.get('lng'), current_user.id)
        db.session.add(new_location)
        db.session.commit()
        return jsonify()
    return render_template('locations/index.html')

@locations_blueprint.route('/new')
@login_required
@ensure_correct_user
def new(user_id):
    return render_template('locations/new.html')

@locations_blueprint.route('/data', methods=["GET"])
def data(user_id):
    user_locations = User.query.get(user_id).locations
    locations = []
    for l in user_locations:
        locations.append(dict(lat=l.lat, lng=l.lng))
    return jsonify(locations)
