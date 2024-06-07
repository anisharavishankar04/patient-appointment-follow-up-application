from flask import Flask, jsonify

app = Flask(__name__)

# Define the education content about appointment follow-ups
education_content = """
Here are some reasons why follow-ups after appointments are important:
- Ensures that patients receive necessary post-appointment care instructions
- Helps in monitoring patient progress and addressing any concerns
- Improves patient satisfaction and loyalty to the healthcare provider
- Reduces the likelihood of missed appointments and improves appointment adherence

Remember, effective follow-ups can greatly contribute to the overall success of patient care.
"""

@app.route('/education/appointment-follow-ups', methods=['GET'])
def get_education_content():
    return jsonify({'content': education_content})

if __name__ == '__main__':
    app.run(debug=True)
