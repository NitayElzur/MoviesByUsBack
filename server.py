from flask import *
import psycopg2
import json

app = Flask(__name__)


def connect_to_database():
    try:
        connection = psycopg2.connect(database='Movies',
                                      user='postgres', password='123',
                                      host='127.0.0.1', port=5433)
        print('connected to database')
    except NameError:
        connection = False
        print(NameError)
    return connection


conn = connect_to_database()


def get_request(req: str):
    cur = conn.cursor()
    cur.execute(req)
    rows = cur.fetchall()

    return rows


def update_request(req: str):
    cur = conn.cursor()
    cur.execute(req)
    conn.commit()


@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Methods'] = '*'
    return response


@app.get('/')
def fetch_all():
    map = []
    for row in get_request('select * from movies order by id asc'):
        map.append({
            'id': row[0],
            'name': row[1],
            'rate': row[2],
            'liked': row[3],
            'genre': row[4]
        })
    return map


@app.get('/sum-of-genres')
def sum_of_genres():
    map = []
    for row in get_request('select genre, count(genre) as amount from movies group by genre order by amount desc'):
        map.append({
            'genre': row[0],
            'amount': row[1]
        })
    return map


@app.patch('/update-like')
def update_like():
    try:
        data = request.json
        update_request(
            f'update movies set liked = {data["value"]} where id = {data["id"]}')
        return 'success'
    except NameError:
        return NameError


@app.post('/add-movie')
def add_movie():
    try:
        data = request.json
        update_request(
            f'insert into movies (id, name, rate, liked, genre) select max(id) + 1, \'{data["name"]}\', {data["rate"]}, {data["liked"]}, \'{data["genre"]}\' from movies;')
        return 'success'
    except NameError:
        return NameError


@app.delete('/delete-movie')
def delete_movie():
    try:
        data = request.json
        update_request(f'delete from movies where id = {data["id"]}')
        return 'success'
    except NameError:
        return NameError


app.run()
