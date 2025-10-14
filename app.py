from flask import Flask, jsonify
from flask_cors import CORS
from FACE import Face_recog_code  # Import the function from big.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run-python')
def run_python():
    result = Face_recog_code()  # Call the function from big.py
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(port=5000, debug=True)