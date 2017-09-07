from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/hoops'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
# You also need to tell flask_login where it should redirect
# someone to if they try to access a private route.
login_manager.login_view = "users.login"
# You can also change the default message when someone
# gets redirected to the login page. The default message is
# "Please log in to access this page."
login_manager.login_message = "Please log in!"

from project.users.views import users_blueprint
from project.models import User
from project.locations.views import locations_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(locations_blueprint, url_prefix='/users/<int:user_id>/locations')

@app.route('/')
def root():
    return render_template('users/home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
