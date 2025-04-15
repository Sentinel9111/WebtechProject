from models import User

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    submit = SubmitField("Log in")

def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError("Gebruik een andere gebruikersnaam.")

def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError("Gebruik een ander email adres.")

class RegistrationForm(FlaskForm):
    username = StringField(
        "Gebruikersnaam", validators=[DataRequired(), Length(min=2, max=20), validate_username]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), validate_email])
    password = PasswordField("Wachtwoord", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Bevestig wachtwoord", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Registreer")

class AddEquipmentForm(FlaskForm):
    name = StringField(
        "Naam", validators=[DataRequired(), Length(min=1, max=100)]
    )
    brand = StringField("Merk", validators=[DataRequired(), Length(min=1, max=100)])
    category = SelectField("Categorie", validators=[DataRequired()])
    submit = SubmitField("Voeg toe")

class AddCategoryForm(FlaskForm):
    name = StringField(
        "Naam", validators=[DataRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Voeg toe")
