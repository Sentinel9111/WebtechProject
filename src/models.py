from app import db, login_manager

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User('{self.id}', {self.username}', '{self.email}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Job('{self.id}', '{self.name}', '{self.description}')"

class UserJob(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)

    def __init__(self, user_id, job_id):
        self.user_id = user_id
        self.job_id = job_id

    def __repr__(self):
        return f"UserJob('{self.user_id}', '{self.job_id}')"

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('equipment', lazy=True))

    def __init__(self, name, brand, category_id):
        self.name = name
        self.brand = brand
        self.category_id = category_id

    def __repr__(self):
        return f"Equipment('{self.id}', '{self.name}', '{self.brand}', '{self.category_id}')"

class Cable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    length = db.Column(db.Float, nullable=False)
    conn_a_id = db.Column(db.Integer, db.ForeignKey('connector.id'), nullable=False)
    conn_b_id = db.Column(db.Integer, db.ForeignKey('connector.id'), nullable=False)

    def __init__(self, name, category_id, length, conn_a_id, conn_b_id):
        self.name = name
        self.category_id = category_id
        self.length = length
        self.conn_a_id = conn_a_id
        self.conn_b_id = conn_b_id

    def __repr__(self):
        return f"Cable('{self.id}', '{self.name}', '{self.category_id}', '{self.length}', '{self.conn_a_id}', '{self.conn_b_id}')"

class EquipmentJob(db.Model):
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), primary_key=True, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)

    def __init__(self, equipment_id, job_id):
        self.equipment_id = equipment_id
        self.job_id = job_id

    def __repr__(self):
        return f"EquipmentJob('{self.equipment_id}', '{self.job_id}')"

class CableJob(db.Model):
    cable_id = db.Column(db.Integer, db.ForeignKey('cable.id'), primary_key=True, nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)

    def __init__(self, cable_id, job_id):
        self.cable_id = cable_id
        self.job_id = job_id

    def __repr__(self):
        return f"CableJob('{self.cable_id}', '{self.job_id}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category('{self.id}', '{self.name}')"

class Connector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_male = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, is_male):
        self.name = name
        self.is_male = is_male

    def __repr__(self):
        return f"Connector('{self.id}', '{self.name}', '{self.is_male}')"
