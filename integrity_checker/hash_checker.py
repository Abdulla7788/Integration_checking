# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__, template_folder='templates')

def compute_hash(file_data):
    """Compute SHA-256 hash of the given file data."""
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest()

@app.route('/')
def home():
    """Serve the hash.html file when the home route is accessed."""
    return render_template('hash.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_data = file.read()

    if not file_data:
        return jsonify({'error': 'Empty file uploaded'}), 400

    calculated_hash = compute_hash(file_data)

    return jsonify({'hash': calculated_hash})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
