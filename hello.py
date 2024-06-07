from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/message', methods=['GET'])
def get_message():
    return jsonify({'message': 'Helloooo'})

if __name__ == '__main__':
    app.run(debug=True,port=3000)
