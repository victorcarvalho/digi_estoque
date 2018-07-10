from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    items = db.relationship('Item')
    # items = db.relationship('Item', backref='item_room', lazy='dynamic')

    def __repr__(self):
        return 'Nome {}>'.format(self.name)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    unit = db.Column(db.String(8), index=True)
    quantity = db.Column(db.Float)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return 'Nome {}>'.format(self.name)

    def set_name(self, name):
        self.name = name

    def set_unit(self, unit):
        self.unit = unit

    def set_quantity(self, quantity):
        self.quantity = quantity

    def decrease_quantity(self, quantity):
        self.quantity = self.quantity - quantity
        return self.quantity
