from app import app, db, bcrypt
from flask import render_template, flash, redirect
from forms import RegistrationForm, LoginForm
from models import Equipment, User
from flask_login import login_user, current_user, logout_user, login_required
from models import Cable
from forms import AddEquipmentForm, AddCableForm

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
    logout_user();
    return redirect("/");

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title="Account")

@app.route("/inventory")
@login_required
def inventory():
    cables = Cable.query.all()
    equipment = Equipment.query.all()
    return render_template('inventory.html', title="Inventaris", equipment=equipment, cables=cables)

@app.route("/equipment/add")
@login_required
def equipment_add():
    form = AddEquipmentForm()
    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            brand=form.brand.data,
            category=form.category.data
        )

        try:
            db.session.add(equipment)
            db.session.commit()

            flash("Apparatuur toegevoegd!", "success")
            return redirect("/inventory")
        except:
            flash("Niet gelukt om apparatuur toe te voegen!", "danger")

    return render_template("equipment/add.html", title="Voeg Equipment Toe", form=form)

@app.route("/cable/add")
@login_required
def cable_add():
    form = AddCableForm()
    if form.validate_on_submit():
        cable = Cable(
            name=form.name.data,
            brand=form.brand.data,
            category=form.category.data,
            length=form.length.data,
            conn_a=form.conn_a.data,
            conn_b=form.conn_b.data
        )

        try:
            db.session.add(cable)
            db.session.commit()

            flash("Kabel toegevoegd!", "success")
            return redirect("/inventory")
        except:
            flash("Niet gelukt om de kabel toe te voegen!", "danger")

    return render_template("cable/add.html", title="Voeg Cable Toe", form=form)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title="404"), 404