from flask_restful import Resource, reqparse
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from flask import Flask
from base import Read, Book
from flask import Flask
from webargs import fields
from flask_apispec import marshal_with
from marshmallow import Schema
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

api = Api()

app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

parser = reqparse.RequestParser()
parser.add_argument("subname", type=str)
parser.add_argument("name", type=str)
parser.add_argument("patronymic", type=str)
parser.add_argument("phone", type=int)
parser.add_argument("author", type=str)
parser.add_argument("name_book", type=str)
parser.add_argument("tour_package_id", type=str)


# {
#     "subname": "Иванов",
#     "name": "Иван",
#     "patronymic": "Иванович",
#     "phone": 89000000,
#     "author": "Иван",
#     "name_book": "Ваня",
#     "tour_package_id": 1
# }


class BoksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book

class ReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Read

    books_dates = ma.Nested(BoksSchema, many=True)

class Main(Resource):
    @marshal_with(ReadSchema(many=True))
    def get(self, reader_id):
        if reader_id == 0:
            return Read.query.all()
        else:
            return db.session.query(Read).join(Book, Read.id == Book.tour_package_id).filter(Book.tour_package_id == reader_id).all()

    @marshal_with(ReadSchema(many=True))
    def post(self, reader_id):
        args = parser.parse_args()
        if reader_id == 0:
            add_cell_Readers = Read(
                subname = args['subname'],
                name = args['name'], 
                patronymic = args['patronymic'], 
                phone = args['phone'])

            db.session.add(add_cell_Readers)
            db.session.commit()
            return db.session.query(Read).filter(Read.phone == add_cell_Readers.phone).all()
        else:
            u = Book(author = args['author'], name_book = args['name_book'], tour_package_id = args['tour_package_id'])
            db.session.add(u)
            db.session.commit()
            return db.session.query(Read).filter(Book.tour_package_id == u.tour_package_id).all()

    @marshal_with(ReadSchema(many=True))
    def delete(self, reader_id):
        list = []
        for it in db.session.query(Read).join(Book, Read.id == Book.tour_package_id).filter(Read.id == reader_id):
            list.append(it)
            db.session.delete(it)
            db.session.commit()
            return list

api.add_resource(Main, "/book/reader/<int:reader_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)