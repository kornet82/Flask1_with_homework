import sqlite3
import random
import flask
import os
from flask import Flask, jsonify, request, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path

BASE_DIR = Path(__file__).parent
PATH_TO_DB = BASE_DIR / "main.db"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,

        }


# Остановился на 28-02-2022 1:10 - подключение миграций, что то идет не так

class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author_id = author.id
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "text": self.text
        }


# Остановился на 25_02_2022 1:45

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(PATH_TO_DB)
#     return db
#
#
# # Закончил -25.02.2022 в 47-18
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()



# AUTORS

@app.route("/authors")
def get_authors():
    autors_obj = AuthorModel.query.all()
    authors_dict = []
    for author in autors_obj:
        authors_dict.append(author.to_dict())
    return jsonify(authors_dict), 200


@app.route("/authors", methods=['POST'])
def create_authors():
    data = request.json
    # quote = QuoteModel(data["author"], data["text"])
    try:
        author = AuthorModel(**data)

    except TypeError:
        if data.get("author") == None:
            return f"Please add Author", 400
        return f"required data", 400
    db.session.add(author)
    db.session.commit()
    # quote = request.json
    # # print("data = ", data)
    # quote["id"] = quotes[-1]["id"] + 1
    # quotes.append(quote)
    # connection = sqlite3.connect(PATH_TO_DB)
    # connection = get_db()
    # cursor = connection.cursor()
    # quote = request.json
    # query = f"INSERT INTO quotes (author, text) VALUES ('{quote['author']}', '{quote['text']}');"
    # cursor.execute(query)
    # connection.commit()
    # quote["id"] = cursor.lastrowid
    # cursor.close()
    return jsonify(author.to_dict()), 201


# QUOTES


@app.route("/quotes")
def get_quotes():
    quotes_obj = QuoteModel.query.all()
    quotes_dict = []
    for quote in quotes_obj:
        quotes_dict.append(quote.to_dict())
    # # connection = sqlite3.connect(PATH_TO_DB)
    # connection = get_db()
    # cursor = connection.cursor()
    # query = "SELECT * FROM quotes"
    # cursor.execute(query)
    # sql_data = cursor.fetchall()
    # keys = ("id", "author", "text")
    # quotes = []
    # # print(f"{sql_data=}")
    # for el in sql_data:
    #     quote = to_dict(el, keys)
    #     quotes.append(quote)
    #     cursor.close()
    return jsonify(quotes_dict), 200


# остановился на 1-32 24-02-2022

@app.route('/quotes/<int:quote_id>')
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        f'Post {quote_id} not found', 404
    return jsonify(quote.to_dict())
    # show the post with the given id, the id is an integer
    # for i in range(len(quotes)):
    #     if i == quote_id:
    #         return jsonify(quotes[quote_id - 1])
    # return flask.abort(404)
    # return f'Post {quote_id} not found',404
    # connection = sqlite3.connect(PATH_TO_DB)
    # connection = get_db()
    # cursor = connection.cursor()
    # query = f"SELECT * FROM quotes WHERE id={quote_id}"
    # cursor.execute(query)
    # sql_data = cursor.fetchone()
    # if sql_data is None:
    #     return f'Post {quote_id} not found', 404
    # keys = ("id", "author", "text")
    # quote = to_dict(sql_data, keys)
    # cursor.close()
    # return jsonify(quote)


# @app.route('/quotes/count')
# def count():
#     return {'count': len(quotes)}
#
#
# @app.route('/quotes/random')
# def get_random_quote():
#     random_id = random.randint(0, len(quotes) - 1)
#     return quotes[random_id]


@app.route("/authors/<int:author_id>/quotes", methods=['POST'])
def create_quote(author_id):
    data = request.json
    author = AuthorModel.query.get(author_id)
    try:
        quote = QuoteModel(author, **data)
        print(quote)  # эквивалент quote = QuoteModel(author=data["author"], text=data["text"])
    except AttributeError:
        if author is None:
            return f"Author with ID {author_id} not found", 400
        if data.get("text") == None:
            return f"Please add text", 400
        return f"required data", 400
    db.session.add(quote)
    db.session.commit()
    # quote = request.json
    # # print("data = ", data)
    # quote["id"] = quotes[-1]["id"] + 1
    # quotes.append(quote)
    # connection = sqlite3.connect(PATH_TO_DB)
    # connection = get_db()
    # cursor = connection.cursor()
    # quote = request.json
    # query = f"INSERT INTO quotes (author, text) VALUES ('{quote['author']}', '{quote['text']}');"
    # cursor.execute(query)
    # connection.commit()
    # quote["id"] = cursor.lastrowid
    # cursor.close()
    return jsonify(quote.to_dict()), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    data = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return f"Quote with id {quote_id} not found", 404
    # quote.author = data["author"]
    # quote.text = data["text"]
    for key, value in data.items():
        setattr(quote, key, value)

    db.session.commit()

    # ЧЕРЕЗ СПИСКИ
    # for quote in quotes:
    #     if quote["id"] == quote_id:
    #         if new_data.get("author") is not None:
    #             quote["author"] = new_data["author"]
    #         if new_data.get("text") is not None:
    #             quote["text"] = new_data["text"]
    #         if new_data.get("rate") is not None:
    #             quote["rate"] = new_data["rate"]
    #         return jsonify(quote)
    # return flask.abort(404)
    # connection = sqlite3.connect(PATH_TO_DB)

    # SQLite3
    # connection = get_db()
    # cursor = connection.cursor()
    # quote = request.json
    # query = f"UPDATE quotes SET author=('{quote['author']}'), text=('{quote['text']}') WHERE id={quote_id};"
    # cursor.execute(query)
    # connection.commit()
    # quote["id"] = quote_id
    # cursor.close()
    return jsonify(quote.to_dict()), 200


@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote_by_id(quote_id):
    # ЧЕРЕЗ СПИСКИ
    # delete quote with id
    # for quote in quotes:
    #     if quote["id"] == quote_id:
    #         quotes.remove(quote)
    #         print(quotes)
    #         return f"Quote with id {quote_id} is deleted.", 200
    # return f"Quote with id {quote_id} not found", 404
    # connection = sqlite3.connect(PATH_TO_DB)

    # SQLite3
    # connection = get_db()
    # cursor = connection.cursor()
    # query = f"DELETE FROM quotes WHERE id={quote_id};"
    # cursor.execute(query)
    # connection.commit()
    # cursor.close()

    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        return f"Quote with ID {quote_id} not found", 404
    db.session.delete(quote)
    db.session.commit()
    return f'Post {quote_id} deleted', 200


@app.route("/quotes/filter", methods=['GET'])
def get_quotes_by_filter():
    quotes_by_filter = QuoteModel.query.filter_by(author='Alex').all()
    quotes_dict_by_filter = []
    for quote in quotes_by_filter:
        quotes_dict_by_filter.append(quote.to_dict())
    return jsonify(quotes_dict_by_filter)


# Помогли из чата!!!
# @app.route("/quotes/filter", methods=['GET'])
# def get_quotes_by_filter():
#     quotes_by_filter = QuoteModel.query.filter_by(author='Alex').all()
#     return jsonify([quote.to_dict() for quote in quotes_by_filter])


if __name__ == "__main__":
    app.run(debug=True)
