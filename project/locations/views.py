from flask import Blueprint, redirect, render_template, url_for, request, flash, jsonify
from flask_login import current_user
from project import db
from project.models import Location

locations_blueprint = Blueprint(
  'locations',
  __name__,
  template_folder = 'templates'
)

@locations_blueprint.route('/', methods=["GET","POST"])
def index(user_id):
    if request.method == 'POST':
        new_location = Location(request.form.get('lat'), request.form.get('long'), current_user.id)
        db.session.add(new_location)
        db.session.commit()
        return jsonify('All done!')
    return render_template('locations/index.html')

@locations_blueprint.route('/new')
def new(user_id):
    return render_template('locations/new.html')
