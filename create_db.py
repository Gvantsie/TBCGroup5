from ext import app, db
from models import Product, Comment, User

with app.app_context():

    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="adminpass", role="Admin")

    db.session.add(admin)
    db.session.commit()
