from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)
DB = "../database/hostel.db"

def connect_db():
    return sqlite3.connect(DB)

@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    conn.close()
    return jsonify(rooms)

@app.route('/complaints', methods=['POST'])
def add_complaint():
    data = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (resident_id, description) VALUES (?, ?)", 
                   (data['resident_id'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Complaint submitted"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

