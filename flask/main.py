import json
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_restful import Api, Resource, reqparse
from flask import Flask, jsonify
from base import Books, db, Readers, set_db_cnn
from flask_marshmallow import Marshmallow




app = Flask(__name__)
ma = Marshmallow(app)
with open("config.json") as json_file:
    data = json.load(json_file)

app.config["SECRET_KEY"] = "SPGKRPOKGBOGKTOKBOHK"
app.config["SQLALCHEMY_DATABASE_URI"] = data["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


api = Api()
db = set_db_cnn(app)

parser = reqparse.RequestParser()
parser.add_argument("subname", type=str)
parser.add_argument("name", type=str)
parser.add_argument("patronymic", type=str)
parser.add_argument("phone", type=int)
parser.add_argument("author", type=str)
parser.add_argument("name_book", type=str)
parser.add_argument("book_reader_id", type=str)


# fields = {
#     "date": fields.String,
#     "id": fields.Integer,
#     "name": fields.String,
#     "patronymic": fields.String,
#     "phone": fields.Integer,
#     "subname": fields.String,
# }

#маршмелоу
class PostSchema(ma.Schema):
    class Meta:
        fields = ("subname", "name", "patronymic" , "phone", "author", "name_book", "book_reader_id")

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# Пример запроса
#  {
#         "subname": "Чехов",
#         "name": "Иван",
#         "patronymic": "Петров",
#         "phone": 898887777,
#         "book": "Тихий Дон",
#         "author": "-----",
#         "name_book": "Тихий Дон",
#         "book_reader_id": 2,
#     },

class Main(Resource):
    def get(self, reader_id):
        if reader_id == 1:
            reader_cell2 = db.session.query(Readers, Books).join(Books, Readers.id == Books.book_reader_id).all()
            d = []
            for i in reader_cell2:
                list = posts_schema.dump(i)
                d.append(list)
                print(list)
            return d 
        
        else:
            reader_cell = db.session.query(Readers).filter_by(id=reader_id).first()
            return jsonify(reader_cell.as_dict())
        
    def post(self, reader_id):

        args = parser.parse_args()

        add_cell_Readers = Readers(
            subname = args['subname'],
            name = args['name'], 
            patronymic = args['patronymic'], 
            phone = args['phone'],
            
        )
        
        db.session.add(add_cell_Readers)
        db.session.flush()

        u = Books(author = args['author'], name_book = args['name_book'], book_reader_id = add_cell_Readers.id)
        db.session.add(u)
        db.session.commit()
        return jsonify(add_cell_Readers.as_dict())

    def put(self, reader_id):
        args = parser.parse_args()
        reader_cell = db.session.query(Readers).filter_by(id=reader_id).first()
        if args['subname']:
            reader_cell.subname = args['subname']
        if args['name']:
            reader_cell.name = args['name']
        if args['patronymic']:
            reader_cell.patronymic = args['patronymic']
        if args['phone']:
            reader_cell.phone = args['phone']
        db.session.commit()
        return jsonify(reader_cell.as_dict())

    def delete(self, reader_id):
        reader_dell = db.session.query(Readers).get(reader_id)
        db.session.delete(reader_dell)
        db.session.commit()
        return jsonify(reader_dell.as_dict())


api.add_resource(Main, "/book/reader/<int:reader_id>")
api.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
