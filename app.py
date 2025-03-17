from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.secret_key = "Banaan"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
