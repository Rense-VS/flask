import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

with open("config.json") as json_file:
    data = json.load(json_file)

base = declarative_base()
engine = sa.create_engine(data["SQLALCHEMY_DATABASE_URI"])
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)


def set_db_cnn(app):
    db = SQLAlchemy(app)
    # db.create_all()

    return db


db = base


class Readers(base):
    __tablename__ = "readers"

    id = sa.Column(sa.Integer, primary_key=True)
    subname = sa.Column(sa.String(50), nullable=True)
    name = sa.Column(sa.String(50), nullable=True)
    patronymic = sa.Column(sa.String(50), nullable=True)
    phone = sa.Column(sa.Integer())
    date = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __init__(self, subname, name, patronymic, phone):
        self.subname = subname
        self.name = name
        self.patronymic = patronymic
        self.phone = phone

    def __repr__(self):
        return f"<readers {self.id}>"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Books(base):
    __tablename__ = "books"

    id = sa.Column(sa.Integer, primary_key=True)
    author = sa.Column(sa.String(50), nullable=True)
    name_book = sa.Column(sa.String(100))
    book_reader_id = sa.Column(sa.Integer, sa.ForeignKey("readers.id"))

    def __init__(self, author, name_book, book_reader_id):
        self.author = author
        self.name_book = name_book
        self.book_reader_id = book_reader_id

    def __repr__(self):
        return f"<books {self.id}>"


base.metadata.create_all()
