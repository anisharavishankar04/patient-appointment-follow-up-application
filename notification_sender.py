from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'supersecretkey'
CORS(app)
app.config['SESSION_TYPE'] = 'filesystem'

# In-memory storage for example purposes
users = {'admin': {'password': generate_password_hash('adminpass'), 'email': 'admin@example.com'}}
patients = {'patient1': {'password': generate_password_hash('patientpass'), 'email': 'patient1@example.com'}}

upcoming_appointments = []
patient_appointments = {}

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

def send_email(recipient, subject, message):
    try:
        # Create SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(patients[recipient]['email'], patients[recipient]['password'])

        # Construct email message
        msg = MIMEMultipart()
        msg['From'] = patients[recipient]['email']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Send email
        server.sendmail(patients[recipient]['email'], recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def notify_upcoming_appointments(email):
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    appointments = patient_appointments.get(email, [])
    for appointment in appointments:
        appointment_date = datetime.strptime(appointment['date'], '%Y-%m-%d')
        if appointment_date == tomorrow:
            # Compose email message
            subject = 'Upcoming Appointment Reminder'
            message = f"Dear patient,\n\nYou have an appointment tomorrow with {appointment['doctor']} at {appointment['time']}.\n\nPlease arrive on time.\n\nBest regards,\nYour Hospital"

            # Send email notification
            if send_email(email, subject, message):
                print(f"Notification email sent to {email} for appointment on {appointment['date']} at {appointment['time']}")
            else:
                print(f"Failed to send notification email to {email}")

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
        return jsonify({'token': 'abc', 'email': patients[user_id]['email']}), 
