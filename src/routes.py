from app import app, db, bcrypt
from forms import AddEquipmentForm, AddCategoryForm, AddCableForm, AddConnectorForm, RegistrationForm, LoginForm, AddJobForm
from models import Equipment, User, Cable, Category, Connector, Job

from flask import render_template, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@login_required
def index():
    jobs = Job.query.all()
    cables = Cable.query.all()
    equipment = Equipment.query.all()
    return render_template('index.html', title="Inventaris", equipment=equipment, cables=cables, jobs=jobs)

@app.errorhandler(Exception)
def handle_error(e):
    code = getattr(e, 'code', 500)
    return render_template("error.html", code=code, message=str(e)), code

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

@app.route("/equipment/add", methods=['GET', 'POST'])
@login_required
def equipment_add():
    form = AddEquipmentForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        equipment = Equipment(
            name=form.name.data,
            brand=form.brand.data,
            category_id=form.category.data,
            count=form.count.data
        )

        try:
            db.session.add(equipment)
            db.session.commit()

            flash("Apparatuur toegevoegd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om apparatuur toe te voegen!", "danger")

    return render_template("equipment.html", title="Voeg apparatuur toe", form=form)

@app.route('/equipment/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def equipment_edit(id):
    equipment = Equipment.query.get_or_404(id)
    form = AddEquipmentForm(obj=equipment)
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.submit.label.text = "Werk bij"

    if form.validate_on_submit():
        equipment.name = form.name.data
        equipment.brand = form.brand.data
        equipment.category_id = form.category.data
        equipment.count = form.count.data

        try:
            db.session.commit()

            flash("Apparatuur bijgewerkt!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om apparatuur bij te werken!", "danger")

    return render_template("equipment.html", title="Bewerk apparatuur", form=form, equipment_id=id)

@app.route("/equipment/<int:id>/delete")
@login_required
def equipment_delete(id):
    Equipment.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Apparatuur verwijderd!", "success")
    return redirect("/")

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
            return redirect("/")
        except:
            flash("Niet gelukt om een categorie toe te voegen!", "danger")

    return render_template("category.html", title="Voeg een categorie toe", form=form)

@app.route("/category/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def category_edit(id):
    category = Category.query.get_or_404(id)
    form = AddCategoryForm(obj=category)
    form.submit.label.text = "Werk bij"

    if form.validate_on_submit():
        category.name = form.name.data

        try:
            db.session.commit()

            flash("Categorie bijgewerkt!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de categorie bij te werken!", "danger")

    return render_template("category.html", title="Bewerk een categorie", form=form, category_id=id)

@app.route("/category/<int:id>/delete")
@login_required
def category_delete(id):
    Category.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Categorie verwijderd!", "success")
    return redirect("/")

@app.route("/cable/add", methods=['GET', 'POST'])
@login_required
def cable_add():
    form = AddCableForm()
    form.conn_a.choices = [(conn.id, f'{conn.name} ({conn.gender_label()})') for conn in Connector.query.all()]
    form.conn_b.choices = [(conn.id, f'{conn.name} ({conn.gender_label()})') for conn in Connector.query.all()]
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        cable = Cable(
            conn_a_id=form.conn_a.data,
            conn_b_id=form.conn_b.data,
            length=form.length.data,
            category_id=form.category.data,
            count=form.count.data
        )

        try:
            db.session.add(cable)
            db.session.commit()

            flash("Kabel toegevoegd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de kabel toe te voegen!", "danger")

    return render_template("cable.html", title="Voeg een kabel toe", form=form)

@app.route("/cable/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def cable_edit(id):
    cable = Cable.query.get_or_404(id)
    form = AddCableForm(obj=cable)
    form.conn_a.choices = [(conn.id, f'{conn.name} ({conn.gender_label()})') for conn in Connector.query.all()]
    form.conn_b.choices = [(conn.id, f'{conn.name} ({conn.gender_label()})') for conn in Connector.query.all()]
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    form.submit.label.text = "Werk bij"

    if form.validate_on_submit():
        cable.conn_a_id = form.conn_a.data
        cable.conn_b_id = form.conn_b.data
        cable.length = form.length.data
        cable.category_id = form.category.data
        cable.count = form.count.data

        try:
            db.session.commit()

            flash("Kabel gewijzigd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de kabel te wijzigen!", "danger")

    return render_template("cable.html", title="Bewerk kabel", form=form, cable_id=id)

@app.route("/cable/<int:id>/delete")
@login_required
def cable_delete(id):
    Cable.query.filter_by(id=id).delete()
    db.session.commit()

    flash("Kabel verwijderd!", "success")
    return redirect("/")

@app.route("/connector/add", methods=['GET', 'POST'])
@login_required
def connector_add():
    form = AddConnectorForm()

    if form.validate_on_submit():
        connector = Connector(
            name=form.name.data,
            is_male=form.is_male.data
        )

        try:
            db.session.add(connector)
            db.session.commit()

            flash("Connector toegevoegd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de connector toe te voegen!", "danger")

    return render_template("connector.html", title="Voeg een connector toe", form=form)

@app.route("/connector/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def connector_edit(id):
    connector = Connector.query.get_or_404(id)
    form = AddConnectorForm(obj=connector)
    form.submit.label.text = "Werk bij"

    if form.validate_on_submit():
        connector.name = form.name.data
        connector.is_male = form.is_male.data

        try:
            db.session.commit()

            flash("Connector gewijzigd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de connector te wijzigen!", "danger")

    return render_template("connector.html", title="Bewerk connector", form=form, connector_id=id)

@app.route("/connector/<int:id>/delete")
@login_required
def connector_delete(id):
    try:
        Connector.query.filter_by(id=id).delete()
        db.session.commit()

        flash("Connector verwijderd!", "success")
        return redirect("/")
    except:
        flash("Niet gelukt om de connector te verwijderen!", "danger")

@app.route("/job/add", methods=['GET', 'POST'])
@login_required
def job_add():
    form = AddJobForm()

    if form.validate_on_submit():
        job = Job(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )

        try:
            db.session.add(job)
            db.session.commit()

            flash("Klus toegevoegd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om een klus toe te voegen!", "danger")

    return render_template("job.html", title="Voeg een klus toe", form=form)

@app.route("/job/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def job_edit(id):
    job = Job.query.get_or_404(id)
    form = AddJobForm(obj=job)
    form.submit.label.text = "Werk bij"

    equipment = Equipment.query.all()

    if form.validate_on_submit():
        job.name = form.name.data
        job.description = form.description.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        try:
            db.session.commit()

            flash("Klus gewijzigd!", "success")
            return redirect("/")
        except:
            flash("Niet gelukt om de klus te wijzigen!", "danger")

    return render_template("job.html", title="Bewerk de klus", form=form, job_id=id, equipment=equipment)

@app.route("/job/<int:id>/delete")
@login_required
def job_delete(id):
    try:
        Job.query.filter_by(id=id).delete()
        db.session.commit()

        flash("Klus verwijderd!", "success")
        return redirect("/")
    except:
        flash("Niet gelukt om de klus te verwijderen!", "danger")


