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
    description = db.Column(db.String(5000), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    def __init__(self, name, description, start_date, end_date):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"Job('{self.id}', '{self.name}', '{self.description}', '{self.start_date}', '{self.end_date}')"

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', foreign_keys=[category_id])
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, name, brand, category_id, count):
        self.name = name
        self.brand = brand
        self.category_id = category_id
        self.count = count

    def __repr__(self):
        return f"Equipment('{self.id}', '{self.name}', '{self.brand}', '{self.category_id}', '{self.count}')"

class Cable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Float, nullable=False)
    conn_a_id = db.Column(db.Integer, db.ForeignKey('connector.id'), nullable=False)
    conn_a = db.relationship('Connector', foreign_keys=[conn_a_id])
    conn_b_id = db.Column(db.Integer, db.ForeignKey('connector.id'), nullable=False)
    conn_b = db.relationship('Connector', foreign_keys=[conn_b_id])
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', foreign_keys=[category_id])
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, conn_a_id, conn_b_id, category_id, length, count):
        self.conn_a_id = conn_a_id
        self.conn_b_id = conn_b_id
        self.length = length
        self.category_id = category_id
        self.count = count

    def __repr__(self):
        return f"Cable('{self.id}', '{self.conn_a_id}', '{self.conn_b_id}', '{self.category_id}', {self.length}, {self.count})"

class EquipmentJob(db.Model):
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), primary_key=True, nullable=False)
    equipment = db.relationship('Equipment', foreign_keys=[equipment_id])
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)
    job = db.relationship('Job', foreign_keys=[job_id])
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, equipment_id, job_id, count):
        self.equipment_id = equipment_id
        self.job_id = job_id
        self.count = count

    def __repr__(self):
        return f"EquipmentJob('{self.equipment_id}', '{self.job_id}')"

class CableJob(db.Model):
    cable_id = db.Column(db.Integer, db.ForeignKey('cable.id'), primary_key=True, nullable=False)
    cable = db.relationship('Cable', foreign_keys=[cable_id])
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), primary_key=True, nullable=False)
    job = db.relationship('Job', foreign_keys=[job_id])
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, cable_id, job_id, count):
        self.cable_id = cable_id
        self.job_id = job_id
        self.count = count

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

    def gender_label(self):
        if self.is_male:
            return 'm'
        else:
            return 'f'
