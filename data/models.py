from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.DateTime(), unique=False, nullable=False)
    flight = db.Column(db.String(10), unique=False, nullable=False)
    fullname = db.Column(db.String(120), unique=False, nullable=False)
    id_number = db.Column(db.String(12), unique=False, nullable=False)
    passport_number = db.Column(db.String(12), unique=False, nullable=False)
    birth_date = db.Column(db.DateTime(), unique=False, nullable=False)
    citizenship = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)
    before_arrival = db.Column(db.String(120), unique=False, nullable=False)
    region = db.Column(db.String(120), unique=False, nullable=False)
    residence = db.Column(db.String(120), unique=False, nullable=False)
    work_place = db.Column(db.String(120), unique=False, nullable=False)
    found = db.Column(db.Boolean(), unique=False, nullable=False)
    hospitalized = db.Column(db.Boolean(), unique=False, nullable=False)
    hospital = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'{self.id}. {self.fullname}'

    def get(self, key):
        if isinstance(getattr(self, key), bool):
            return 'Да' if getattr(self, key) else 'Нет'
        elif isinstance(getattr(self, key), datetime):
            # print(getattr(self, key).strftime("%d.%m.%Y"))
            return getattr(self, key).strftime("%d.%m.%Y")
        return str(getattr(self, key))