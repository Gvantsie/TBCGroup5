from flask import Flask, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "kascbaSBAJBJ!@#3546"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "home"

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("ამ გვერდზე შესასვლელად საჭიროა ავტორიზაცია", "warning")
    return redirect('login')