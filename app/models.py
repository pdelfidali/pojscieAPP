from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    balance = db.Column(db.Numeric, nullable=False, default=0)
    phone_number = db.Column(db.String, nullable=False)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def __repr__(self):
        return f'{self.id}: {self.username}'


class Ticket(db.Model):
    __tablename__ = 'tickets'
    tid = db.Column(db.Integer, primary_key=True, nullable=False)
    price = db.Column(db.Numeric, nullable=False, default=0)
    uid = db.Column(db.Integer, primary_key=True, nullable=False)
    eid = db.Column(db.Integer, primary_key=True, nullable=False)

    def __repr__(self):
        return f'{self.tid} na {self.eid} dla {self.uid}, cena:{self.price}'


class Event(db.Model):
    __tablename__ = 'events'
    eid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    limit = db.Column(db.Integer, nullable=False, default=0)
    sold = db.Column(db.Integer, nullable=False, default=0)
    lid = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Numeric, nullable=False, default=0)
    soldout = db.Column(db.Boolean, nullable=False, default=0)
    isOver = db.Column(db.Boolean, nullable=False, default=0)
    artists_aid = db.Column(db.Integer, primary_key=True, nullable=False)


class Artist(db.Model):
    __tablename__ = 'artists'
    aid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String)
    about = db.Column(db.String)
