import os

import flask
import psycopg2
from flask import Flask, render_template

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


def get_db_connection():
    conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            database=os.getenv('DB_NAME'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASS'))
    return conn


@app.route('/v1/health', methods=['GET'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    queries = ['SELECT VERSION();', "SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;"]
    data = []

    for i in queries:
        cur.execute(i)
        data.append(cur.fetchall())

    result = {}
    result.update({"version" : data[0][0][0]})
    result.update({"dota2_db_size": data[1][0][0]})

    result = {"pgsql" : result}

    cur.close()
    conn.close()
    return flask.jsonify(result)


if __name__ == '__main__':
    app.run()
