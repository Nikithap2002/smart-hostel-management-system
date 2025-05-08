from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = './database/hostel.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# ------------------- Home Page -------------------
@app.route('/')
def home():
    return render_template('index.html')

# ------------------- Admin Page -------------------
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

# ------------------- Student Page -------------------
@app.route('/student')
def student_dashboard():
    return render_template('student.html')

# ------------------- Register (for Student) -------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'student')", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Username already exists'}), 400
    finally:
        conn.close()

    return jsonify({'message': 'Student registered successfully!'})

# ------------------- Login (for both Admin and Student) -------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'role': user['role'], 'user_id': user['user_id']})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# ------------------- View Available Rooms (Student) -------------------
@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    rooms = conn.execute("SELECT room_id, room_number, capacity - current_occupancy AS available_slots FROM rooms").fetchall()
    conn.close()

    room_list = [list(row) for row in rooms]
    return jsonify(room_list)

# ------------------- Pay Hostel Fee (Student) -------------------
@app.route('/pay-fee', methods=['POST'])
def pay_fee():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (user_id, amount) VALUES (?, ?)", (user_id, amount))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Payment successful!'})

# ------------------- File Complaint (Student) -------------------
@app.route('/complaints', methods=['POST'])
def file_complaint():
    data = request.get_json()
    user_id = data['user_id']
    description = data['description']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO complaints (user_id, description) VALUES (?, ?)", (user_id, description))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Complaint filed successfully!'})

# ------------------- View All Complaints (Admin) -------------------
@app.route('/complaints', methods=['GET'])
def view_complaints():
    conn = get_db_connection()
    complaints = conn.execute("SELECT c.complaint_id, u.username, c.description, c.status, c.date_filed FROM complaints c JOIN users u ON c.user_id = u.user_id").fetchall()
    conn.close()

    complaint_list = [dict(row) for row in complaints]
    return jsonify(complaint_list)

# ------------------- Update Complaint Status (Admin) -------------------
@app.route('/update-complaint-status', methods=['POST'])
def update_complaint_status():
    data = request.json
    complaint_id = data['complaint_id']
    new_status = data['status']

    conn = get_db_connection()
    cursor = conn.cursor()

    if new_status == "Approved":
        cursor.execute("DELETE FROM complaints WHERE complaint_id = ?", (complaint_id,))
        message = "Complaint processed and removed."
    else:
        cursor.execute("UPDATE complaints SET status = ? WHERE complaint_id = ?", (new_status, complaint_id))
        message = "Status updated."

    conn.commit()
    conn.close()

    return jsonify({"message": message})

@app.route('/payments', methods=['GET'])
def view_payments():
    conn = get_db_connection()

    # Check table schema if needed for debugging
    columns = conn.execute("PRAGMA table_info(residents)").fetchall()
    for col in columns:
        print(col)

    # Query to fetch payments, including residents' name and status (if required)
    payments = conn.execute('''
        SELECT 
            p.payment_id, 
            r.name AS username, 
            p.amount, 
            p.payment_date 
        FROM payments p
        JOIN residents r ON p.resident_id = r.resident_id
    ''').fetchall()
    
    conn.close()

    # Convert the results into a list of dictionaries
    payment_list = [dict(row) for row in payments]

    # Return the payment list as a JSON response
    return jsonify(payment_list)

# ------------------- Main -------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
