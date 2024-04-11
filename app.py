from flask import Flask, request, jsonify
import os
import psycopg2
from dotenv import load_dotenv

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, age INTEGER, email TEXT);"""

INSERT_USER = "INSERT INTO users (name, age, email) VALUES (%s, %s, %s) RETURNING id;"

SELECT_USER = "SELECT id, name, age, email FROM users;"

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)

@app.post('/api/users')
def create_user():
    data = request.get_json()
    name = data["name"]
    age = data["age"]
    email = data["email"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE)
            cursor.execute(INSERT_USER, (name, age, email))
            user_id = cursor.fetchone()[0]
    return {"id": user_id, "mesage": f"User {name} created successfully"}, 201

@app.get('/api/users')
def get_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_USER)
            users = cursor.fetchall()
            users_data = []
            for user in users:
                user_data = {
                    "id": user[0],
                    "name": user[1],
                    "age": user[2],
                    "email": user[3]
                }
                users_data.append(user_data)
    return jsonify(users_data)