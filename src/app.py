import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# app.config['WTF_CSRF_ENABLED'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@app.before_request
def create_tables():
    db.create_all()

from routes import *
from models import db

if __name__ == "__main__":
    app.run(debug=True)

# hydra -l hydra@example.com -x 3:3:a -V -I -s 5000 127.0.0.1 http-post-form "/login:email=^USER^&password=^PASS^:Inloggen mislukt."
# hydra -l hydra@example.com -x 8:16:aA1 -I -s 5000 127.0.0.1 http-post-form "/login:email=^USER^&password=^PASS^:Inloggen mislukt."
# hydra -l hydra@example.com -P /Users/bascammans/Downloads/rockyou_first10000.txt -I -s 5000 127.0.0.1 http-post-form "/login:email=^USER^&password=^PASS^:Inloggen mislukt."
