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

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["SECRET_KEY"] = "SPGKRPOKGBOGKTOKBOHK"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///base.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api()

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
            return db.session.query(Read).join(Book, Read.id == Book.tour_package_id).all()

    def post(self, reader_id):

        args = parser.parse_args()

        add_cell_Readers = Read(
            subname = args['subname'],
            name = args['name'], 
            patronymic = args['patronymic'], 
            phone = args['phone'])

        db.session.add(add_cell_Readers)
        db.session.commit()
        u = Book(author = args['author'], name_book = args['name_book'], tour_package_id = args['tour_package_id'])
        db.session.add( u)
        db.session.commit()

        return "Пользователь успешно добавлен"

    def delete(self, reader_id):
        reader_dell = db.session.query(Read).filter_by(id = reader_id).first()
        db.session.delete(reader_dell)
        db.session.commit()
        return "Успешно удален"

api.add_resource(Main, "/book/reader/<int:reader_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
