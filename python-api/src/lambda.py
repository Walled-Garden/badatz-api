from typing import TypedDict

import psycopg2
from psycopg2.extras import DictCursor

import awsgi


import os
import dotenv

dotenv.load_dotenv()

from flask import Flask, request, jsonify

app = Flask(__name__)
client = app.test_client()

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


def handler(event, context):
    return awsgi.response(app, event, context)


# def get_items
# def lambda_handler(event, context):
#
#
#     try:
#
#         # Convert the rows to a list of dictionaries
#         results = []
#         for row in rows:
#             # Convert each row to a dictionary
#             results.append(
#                 {
#                     "column1": row[0],
#                     "column2": row[1],
#                     # Add more columns as needed
#                 }
#             )
#
#         # Commit the transaction
#         conn.commit()
#
#         # Close cursor and connection
#         cursor.close()
#         conn.close()
#
#         # Return the queried results
#         return {"statusCode": 200, "body": json.dumps(results)}
#
#     except Exception as e:
#         # If an error occurs, return an error response
#         return {"statusCode": 500, "body": json.dumps(str(e))}


if __name__ == "__main__":
    # lambda_handler(None, None)
    app.run(debug=True)
