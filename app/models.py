from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


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


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    unit = db.Column(db.String(8))
    quantity = db.Column(db.Float)
    room = db.Column(db.String(20), index=True)

    def __repr__(self):
        return 'Nome {}>'.format(self.name)

    def set_name(self, name):
        self.name = name

    def set_unit(self, unit):
        self.unit = unit

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_room(self, room):
        self.room = room

    def decrease_quantity(self, quantity):
        self.quantity = self.quantity - quantity
        return self.quantity


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # deve ser substituido por uma chave estrangeira na prox versao
    item_name = db.Column(db.String(50), index=True)
    date = db.Column(db.String(50))
    # date = db.Column(db.DateTime, default=datetime.utcnow)
    orderer = db.Column(db.String(50), index=True)
    quantity = db.Column(db.Float)
    addit_info = db.Column(db.String(140))

    def set_item_name(self, item_name):
        self.item_name = item_name

    def set_orderer(self, orderer):
        self.orderer = orderer

    def set_date(self, date):
        self.date = date

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_addit_info(self, addit_info):
        self.addit_info = addit_info
