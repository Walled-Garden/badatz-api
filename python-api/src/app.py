from pathlib import Path
from typing import TypedDict

import psycopg2
from psycopg2.extras import DictCursor

import os
import dotenv
import sys


sys.path.append(str((Path(__file__).parent / "deps").absolute()))
dotenv.load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# PostgreSQL connection configuration load from environment variables
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_port = os.environ.get("DB_PORT")


class JsonData(TypedDict):
    launch_id: str
    path: int


@app.route("/test_items", methods=["POST"])
def get_test_items():
    json_data: JsonData = request.json
    if "launch_id" not in json_data:
        return jsonify({"error": "'launch_id' is required in body"})

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )

    _path = json_data["path"] if "path" in json_data else 1
    _launch_id = json_data["launch_id"]

    # Create a cursor object using the connection
    cursor = conn.cursor(cursor_factory=DictCursor)

    # Your SQL query
    sql_query = f"""SELECT * FROM public.test_item
                    WHERE (NLEVEL("test_item"."path") = {_path} AND "test_item"."launch_id" = {_launch_id})"""

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all rows from the query result
    rows = cursor.fetchall()
    data = [dict(row) for row in rows]

    return jsonify(data)


@app.route("/")
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
