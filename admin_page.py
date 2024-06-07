from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'

# In-memory storage for example purposes
users = {'admin': generate_password_hash('adminpass')}
upcoming_appointments = []
patient_appointments = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get('userId')
    password = data.get('password')

    if user_id in users and check_password_hash(users[user_id], password):
        session['user'] = user_id
        return jsonify({'message': 'Logged in successfully'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/upcoming-appointments', methods=['GET'])
def get_upcoming_appointments():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user']
    if user_id not in patient_appointments:
        return jsonify({'message': 'No upcoming appointments'}), 200

    return jsonify(patient_appointments[user_id])

@app.route('/add-appointment', methods=['POST'])
def add_appointment():
    if 'user' not in session or session['user'] != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'date' not in data or 'time' not in data or 'doctor' not in data or 'location' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    appointment_id = len(upcoming_appointments) + 1
    new_appointment = {
        "id": appointment_id,
        "date": data['date'],
        "time": data['time'],
        "doctor": data['doctor'],
        "location": data['location']
    }
    upcoming_appointments.append(new_appointment)
    
    # Associate the appointment with the patient (if specified)
    patient_id = data.get('patient_id')
    if patient_id:
        if patient_id not in patient_appointments:
            patient_appointments[patient_id] = []
        patient_appointments[patient_id].append(new_appointment)

    return jsonify({'message': 'Appointment added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True,port=3000)
