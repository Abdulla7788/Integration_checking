# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import hashlib
import logging

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS for frontend communication

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

def compute_hash(file_data):
    """Compute SHA-256 hash of the given file data."""
    hasher = hashlib.sha256()
    hasher.update(file_data)
    return hasher.hexdigest().strip().lower()  # Ensure consistent formatting

@app.route('/')
def home():
    """Serve the HTML page."""
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify_file():
    """Verify file integrity by comparing computed and reference hash."""
    if 'file' not in request.files or 'reference_hash' not in request.form:
        return jsonify({'error': 'File and reference hash are required'}), 400

    file = request.files['file']
    reference_hash = request.form['reference_hash'].strip().lower()  # Normalize hash for comparison

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_data = file.read()
    if not file_data:
        return jsonify({'error': 'Empty file uploaded'}), 400

    calculated_hash = compute_hash(file_data)  # Compute file hash

    logging.debug(f"Reference Hash (Provided): {reference_hash}")
    logging.debug(f"Computed Hash (Generated): {calculated_hash}")

    if calculated_hash == reference_hash:
        logging.info("✅ File Integrity Verified - No changes detected.")
        return jsonify({
            'message': '✅ File Integrity Verified - The file has not been changed.',
            'status': 'success',
            'calculated_hash': calculated_hash
        })
    else:
        logging.warning("❌ File Integrity Compromised - The file has been modified.")
        return jsonify({
            'message': '❌ File Integrity Compromised - The file has been modified or corrupted.',
            'status': 'failure',
            'calculated_hash': calculated_hash
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
