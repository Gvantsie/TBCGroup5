from flask import render_template, flash, session, redirect
from forms import RegisterForm, ProductForm, LoginForm
from ext import app, db
from models import Product, Comment, User
from flask_login import login_user, logout_user, login_required
import os


@app.route("/")
def home():
    # products = Product.query.filter(Product.price > 150, Product.name == "New Puppy").all()
    products = Product.query.all()
    cart_items = len(get_cart_items())
    return render_template("index.html", produktebi=products, role="Admin", cart_items=cart_items)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash("თქვენ წარმატებით დარეგისტრირდით, გაიარეთ ავტორიზაცია", category="success")
        return redirect("/login")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

        flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია", category="success")
        return redirect("/")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)
        image = form.img.data
        directory = os.path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_product.img = image.filename

        db.session.add(new_product)
        db.session.commit()

    return render_template("create_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/")


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/detailed/<int:product_id>")
def detailed(product_id):
    detailed_product = Product.query.get(product_id)
    comment = Comment.query.filter(Comment.product_id == product_id).all()

    return render_template("detailed.html", product=detailed_product, comments=comment)


def get_cart_items():
    return session.get('cart', [])


@app.route("/cart")
@login_required
def cart():
    cart_product_ids = get_cart_items()
    length = len(cart_product_ids)
    if cart_product_ids:
        products = Product.query.filter(Product.id.in_(cart_product_ids)).all()
    else:
        products = []
    return render_template('cart.html', products=products, cart_items=length)


@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(item_id):
    cart = session.get('cart', [])
    cart.append(item_id)

    session['cart'] = cart
    flash("პროდუქტი დამატებულია კალათაში", "success")
    return redirect("/")


@app.route('/remove_from_cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
        session['cart'] = cart
    flash("პროდუქტი წაშლილია კალათიდან", "success")

    return redirect("/cart")
