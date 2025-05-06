from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = "dbodilbek.c32geugqgvkj.ap-southeast-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "odil_3taws"
DB_PASS = "operatingsystem"

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/characters', methods=['GET'])
def get_characters():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, guild, class, level, experience, health, is_alive, last_active, mentor_id FROM new_charactes")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([
        {
            "id": row[0],
            "name": row[1],
            "guild": row[2],
            "class": row[3],
            "level": row[4],
            "experience": row[5],
            "health": float(row[6]),
            "is_alive": row[7],
            "last_active": row[8] if row[8] else None,
            "mentor_id": row[9]
        } for row in rows
    ])

@app.route('/characters', methods=['POST'])
def add_character():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO new_charactes (name, guild, class, level, experience, health, is_alive, last_active, mentor_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['name'], data['guild'], data['class'], data['level'],
        data['experience'], data['health'], data['is_alive'],
        data['last_active'], data['mentor_id']
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Character added"}), 201

@app.route('/characters/<int:char_id>', methods=['DELETE'])
def delete_character(char_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM new_charactes WHERE id = %s", (char_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"Character {char_id} deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
