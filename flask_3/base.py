from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Read(db.Model):
    __tablename__ = 'readers'

    id = db.Column(db.Integer, primary_key=True)
    subname = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True)
    patronymic = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.Integer())
    date = db.Column(db.DateTime, default=datetime.utcnow)
    books_dates = db.relationship('Book', backref='reader', lazy='dynamic')

    def __repr__(self):
        info: str = f'Читатель [ФИО: {self.subname} {self.name} {self.patronymic},'f'Телефон: {self.phone}]'
        return info


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    tour_package_id = db.Column(db.Integer, db.ForeignKey('readers.id'))
    author = db.Column(db.String(50))
    name_book = db.Column(db.String(100))

    def __repr__(self):
        return f'Читатель [ID: {self.id}, Автор: {self.author}, Название книги: {self.name_book} , 'f' Номер книги: {self.tour_package_id}]'

db.create_all()