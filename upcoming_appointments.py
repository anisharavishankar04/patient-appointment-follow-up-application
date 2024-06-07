from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)

# In-memory storage for example purposes
users = {'admin': {'password': generate_password_hash('adminpass'), 'email': 'admin@example.com'}}
patients = {'patient1': {'password': generate_password_hash('patientpass'), 'email': 'patient1@example.com'}}
upcoming_appointments = []

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'userId' not in data or 'password' not in data:
        return jsonify({'error': 'User ID and password are required'}), 400

    user_id = data.get('userId')
    password = data.get('password')
    
    if user_id in users and check_password_hash(users[user_id]['password'], password):
        session['user'] = user_id
        return jsonify({'token': 'abc', 'email': users[user_id]['email']}), 200
    elif user_id in patients and check_password_hash(patients[user_id]['password'], password):
        session['user'] = user_id
        return jsonify({'token': 'abc', 'email': patients[user_id]['email']}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/upcoming-appointments', methods=['GET'])
def get_upcoming_appointments():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user']
    if user_id in patients:
        patient_email = patients[user_id]['email']
        patient_appointments = [appointment for appointment in upcoming_appointments if appointment['patient'] == patient_email]
        return jsonify(patient_appointments), 200
    else:
        return jsonify({'error': 'No upcoming appointments'}), 404

@app.route('/api/add-appointment', methods=['POST'])
def add_appointment():
    if 'user' not in session:
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
        "location": data['location'],
        "patient": session['user']  # Associate the appointment with the logged-in patient
    }
    upcoming_appointments.append(new_appointment)
    return jsonify({'message': 'Appointment added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
