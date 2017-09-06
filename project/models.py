from project import db, bcrypt
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    #first_name = db.Column(db.Text)
    #last_name = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    locations = db.relationship('Location', backref='user', cascade='all,delete')

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.email = email

    @classmethod
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username = username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user
        return False

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, lat,long,user_id):
        self.lat = lat
        self.long = long
        self.user_id = user_id
