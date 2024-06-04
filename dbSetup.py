import bcrypt
import pyotp
from flask_login import UserMixin
from app import database, app
from datetime import datetime
# Written by: Nathan (c2026512)


class User(database.Model, UserMixin):
    __tablename__ = 'Users'

    # Primary key
    id = database.Column(database.Integer, primary_key=True)

    # Login data
    email = database.Column(database.String(100), nullable=False, unique=True)
    password = database.Column(database.String(100), nullable=False)

    # General information
    firstname = database.Column(database.String(100), nullable=False)
    lastname = database.Column(database.String(100), nullable=False)
    role = database.Column(database.String(100), nullable=False, default='user')
    register_date = database.Column(database.DateTime, nullable=False)
    recent_login = database.Column(database.DateTime, nullable=True)

    pin_key = database.Column(database.String(32), nullable=False, default=pyotp.random_base32())

    def __init__(self, email, password, firstname, lastname, role):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.firstname = firstname
        self.lastname = lastname
        self.role = role
        self.register_date = datetime.now()
        self.recent_login = None

    def get_2fa_uri(self):
        return str(pyotp.totp.TOTP(self.pin_key).provisioning_uri(
            name=self.email,
            issuer_name='220011433'
        ))

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)

    def verify_pin(self, pin):
        return pyotp.TOTP(self.pin_key).verify(pin)


class Question(database.Model):
    __tablename__ = 'Question'

    # Primary key
    QID = database.Column(database.Integer, primary_key=True)

    # General information
    question = database.Column(database.String(100), nullable=False)
    real_answer = database.Column(database.String(100), nullable=False)
    fake_answer_1 = database.Column(database.String(100), nullable=False)
    fake_answer_2 = database.Column(database.String(100), nullable=False)
    fake_answer_3 = database.Column(database.String(100), nullable=False)

    def __init__(self, question, real_answer, fake_answer_1, fake_answer_2, fake_answer_3):
        self.question = question
        self.real_answer = real_answer
        self.fake_answer_1 = fake_answer_1
        self.fake_answer_2 = fake_answer_2
        self.fake_answer_3 = fake_answer_3


def init_database():
    with app.app_context():
        database.drop_all()
        database.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     firstname='admin',
                     lastname='admin',
                     role='admin')
        database.session.add(admin)
        database.session.commit()
