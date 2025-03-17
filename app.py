from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.secret_key = "Banaan"

db.init_app(app)
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/loginForm', methods=['GET', 'POST'])
# def loginForm():
#     form = loginForm()
#     if form.validate_on_submit():
#         naam = form.naam.data
#         return redirect(url_for(''))

if __name__ == '__main__':
    app.run(debug=True)
