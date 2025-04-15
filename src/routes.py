from app import app, db, bcrypt
from forms import AddEquipmentForm, AddCategoryForm, RegistrationForm, LoginForm
from models import Equipment, User, Cable, Category

from flask import render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
    return render_template("index.html", title="Inventarissysteem")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        try:
            db.session.add(user)
            db.session.commit()

            flash(f"Account aangemaakt voor {form.username.data}!", "success")
            return redirect("/")
        except:
            flash("Registreren is mislukt. Heb je al een account?", "danger")

    return render_template("register.html", title="Registreren", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        else:
            flash("Inloggen mislukt. Check je email en wachtwoord!", "danger")

    return render_template("login.html", title="Log in", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route("/inventory")
@login_required
def inventory():
    cables = Cable.query.all()
    equipment = Equipment.query.all()
    print(equipment)
    return render_template('inventory.html', title="Inventaris", equipment=equipment, cables=cables)

@app.route("/equipment/add", methods=['GET', 'POST'])
@login_required
def equipment_add():
    form = AddEquipmentForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            brand=form.brand.data,
            category_id=form.category.data
        )

        try:
            db.session.add(equipment)
            db.session.commit()

            flash("Equipment toegevoegd!", "success")
            return redirect("/inventory")
        except:
            flash("Niet gelukt om equipment toe te voegen!", "danger")

    return render_template("equipment/add.html", title="Voeg Equipment Toe", form=form)

@app.route("/category/add", methods=['GET', 'POST'])
@login_required
def category_add():
    form = AddCategoryForm()

    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
        )

        try:
            db.session.add(category)
            db.session.commit()

            flash("Categorie toegevoegd!", "success")
            return redirect("/inventory")
        except:
            flash("Niet gelukt om categorie toe te voegen!", "danger")

    return render_template("category/add.html", title="Voeg Categorie Toe", form=form)
