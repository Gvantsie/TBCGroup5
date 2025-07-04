from flask_login import UserMixin
from ext import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    img = db.Column(db.String(), nullable=False, default="default_img.jpg")


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    product_id = db.Column(db.Integer(), db.ForeignKey("products.id"))


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    role = db.Column(db.String())

    def __init__(self, username, password, role="Guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)