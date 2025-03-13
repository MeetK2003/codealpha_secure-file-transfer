from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
import os
from encryption import encrypt_file, decrypt_file

routes = Blueprint('routes', __name__) 

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@routes.route('/upload', methods=['POST'])
@login_required
def upload():
    if current_user.role != "admin":
        return jsonify({"error": "Permission denied"}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    encrypted_file_path = os.path.join(UPLOAD_FOLDER, f"encrypted_{file.filename}")
    encrypt_file(file_path, encrypted_file_path)  

    return jsonify({"message": "File uploaded and encrypted successfully!"})

@routes.route('/download/<filename>', methods=['GET'])
@login_required
def download(filename):
    if current_user.role not in ["admin", "user"]:
        return jsonify({"error": "Permission denied"}), 403

    encrypted_file_path = os.path.join(UPLOAD_FOLDER, f"encrypted_{filename}")
    decrypted_file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    if not os.path.exists(encrypted_file_path):
        return jsonify({"error": "File not found"}), 404

    decrypt_file(encrypted_file_path, decrypted_file_path)

    return send_file(decrypted_file_path, as_attachment=True)
