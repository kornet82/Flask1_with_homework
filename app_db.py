import sqlite3
import flask
from flask import Flask, jsonify, request, g
import random
from pathlib import Path

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

BASE_DIR = Path(__file__).parent
PATH_TO_DB = BASE_DIR / "test.db"


user = {
    "name": "Павел",
    "surname": "Азаров",
    "email": "kornet",

}

# quotes = [
#     {
#         "id": 1,
#         "author": "Rick Cook",
#         "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
#         "rate": 1,
#
#     },
#     {
#         "id": 2,
#         "author": "Waldi Ravens",
#         "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
#         "rate": 1,
#     },
#     {
#         "id": 3,
#         "author": "Mosher’s Law of Software Engineering",
#         "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
#         "rate": 1,
#     },
#     {
#         "id": 4,
#         "author": "Yoggi Berra",
#         "text": "В теории, теория и практика неразделимы. На практике это не так.",
#         "rate": 1,
#     },
#
# ]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(PATH_TO_DB)
    return db
# Закончил -25.02.2022 в 47-18

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def to_dict(data, keys):
    return dict(zip(keys, data))

@app.route("/quotes")
def get_quotes():
    # connection = sqlite3.connect(PATH_TO_DB)
    connection = get_db()
    cursor = connection.cursor()
    query = "SELECT * FROM quotes"
    cursor.execute(query)
    sql_data = cursor.fetchall()
    keys = ("id", "author", "text")
    quotes = []
    # print(f"{sql_data=}")
    for el in sql_data:
        quote = to_dict(el, keys)
        quotes.append(quote)
        cursor.close()
    return jsonify(quotes), 200
# остановился на 1-32 24-02-2022

@app.route('/quotes/<int:quote_id>')
def get_quote_by_id(quote_id):
    # show the post with the given id, the id is an integer
    # for i in range(len(quotes)):
    #     if i == quote_id:
    #         return jsonify(quotes[quote_id - 1])
    # return flask.abort(404)
    # return f'Post {quote_id} not found',404
    # connection = sqlite3.connect(PATH_TO_DB)
    connection = get_db()
    cursor = connection.cursor()
    query = f"SELECT * FROM quotes WHERE id={quote_id}"
    cursor.execute(query)
    sql_data = cursor.fetchone()
    if sql_data is None:
        return f'Post {quote_id} not found', 404
    keys = ("id", "author", "text")
    quote = to_dict(sql_data, keys)
    cursor.close()
    return jsonify(quote)




@app.route('/quotes/count')
def count():
    return {'count': len(quotes)}


@app.route('/quotes/random')
def get_random_quote():
    random_id = random.randint(0, len(quotes) - 1)
    return quotes[random_id]


@app.route("/quotes", methods=['POST'])
def create_quote():
    # quote = request.json
    # # print("data = ", data)
    # quote["id"] = quotes[-1]["id"] + 1
    # quotes.append(quote)
    # connection = sqlite3.connect(PATH_TO_DB)
    connection = get_db()
    cursor = connection.cursor()
    quote = request.json
    query = f"INSERT INTO quotes (author, text) VALUES ('{quote['author']}', '{quote['text']}');"
    cursor.execute(query)
    connection.commit()
    quote["id"] = cursor.lastrowid
    cursor.close()
    return jsonify(quote), 201


@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    # new_data = request.json
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
    connection = get_db()
    cursor = connection.cursor()
    quote = request.json
    query = f"UPDATE quotes SET author=('{quote['author']}'), text=('{quote['text']}') WHERE id={quote_id};"
    cursor.execute(query)
    connection.commit()
    quote["id"] = quote_id
    cursor.close()
    return jsonify(quote), 200

@app.route("/quotes/<int:quote_id>", methods=['DELETE'])
def delete_quote_by_id(quote_id):
    # delete quote with id
    # for quote in quotes:
    #     if quote["id"] == quote_id:
    #         quotes.remove(quote)
    #         print(quotes)
    #         return f"Quote with id {quote_id} is deleted.", 200
    # return f"Quote with id {quote_id} not found", 404
    # connection = sqlite3.connect(PATH_TO_DB)
    connection = get_db()
    cursor = connection.cursor()
    query = f"DELETE FROM quotes WHERE id={quote_id};"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    return f'Post {quote_id} deleted', 200



@app.route("/quotes/filter", methods=['GET'])
def get_quotes_by_filter():
    searchword_author = request.args.get('author', '')
    author_quotes = []
    for quote in quotes:
        if quote["author"] == searchword_author:
            author_quotes.append(quote)
            return jsonify(author_quotes)


if __name__ == "__main__":
    app.run(debug=True)
