from datetime import datetime

from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField

from models import User

from flask_wtf import FlaskForm
from wtforms.fields import SelectField, IntegerField, DecimalField, StringField, BooleanField, PasswordField, SubmitField, TextAreaField, HiddenField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo, ValidationError

def validate_username(form, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Gebruik een andere gebruikersnaam.")

def validate_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("Gebruik een ander email adres.")

def validate_end_date(form, end_date):
    if end_date.data < form.start_date.data:
        raise ValidationError("Einddatum mag niet eerder zijn dan de startdatum.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20), validate_username])
    email = StringField("Email", validators=[DataRequired(), Email(), validate_email])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    confirm_password = PasswordField("Bevestig wachtwoord", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registreer")

class EquipmentForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired(), Length(min=1, max=100)])
    brand = StringField("Merk", validators=[DataRequired(), Length(min=1, max=100)])
    category = SelectField("Categorie", validators=[DataRequired()])
    count = IntegerField("Aantal", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Voeg toe")

class CableForm(FlaskForm):
    conn_a = SelectField("Connector A", validators=[DataRequired()])
    conn_b = SelectField("Connector B", validators=[DataRequired()])
    length = DecimalField("Lengte (m)", validators=[DataRequired(), NumberRange(min=0, max=1000)])
    category = SelectField("Categorie", validators=[DataRequired()])
    count = IntegerField("Aantal", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Voeg toe")

class CategoryForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Voeg toe")

class ConnectorForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired(), Length(min=1, max=50)])
    is_male = BooleanField("Mannelijk", validators=[])
    submit = SubmitField("Voeg toe")

class JobForm(FlaskForm):
    name = StringField("Naam", validators=[DataRequired(), Length(min=1, max=50)])
    description = TextAreaField("Beschrijving", validators=[Length(max=5000)])
    start_date = DateField("Startdatum", validators=[DataRequired()])
    end_date = DateField("Einddatum", validators=[DataRequired(), validate_end_date])
    submit = SubmitField("Voeg toe")
