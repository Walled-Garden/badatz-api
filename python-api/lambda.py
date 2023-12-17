import psycopg2
import json

import os
import dotenv

dotenv.load_dotenv()

from flask import Flask

app = Flask(__name__)
client = app.test_client()


@app.route("/")
def index():
    return json.dumps({"name": "alice", "email": "alice@outlook.com"})


# def get_items
def lambda_handler(event, context):
    # PostgreSQL connection configuration load from environment variables
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT")

    try:
        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )

        # Create a cursor object using the connection
        cursor = conn.cursor()

        # Your SQL query
        sql_query = """SELECT * FROM public.test_item
                        WHERE (NLEVEL("test_item"."path") = 1 AND "test_item"."launch_id" = 1135)"""

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        results = []
        for row in rows:
            # Convert each row to a dictionary
            results.append(
                {
                    "column1": row[0],
                    "column2": row[1],
                    # Add more columns as needed
                }
            )

        # Commit the transaction
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return the queried results
        return {"statusCode": 200, "body": json.dumps(results)}

    except Exception as e:
        # If an error occurs, return an error response
        return {"statusCode": 500, "body": json.dumps(str(e))}


if __name__ == "__main__":
    lambda_handler(None, None)
