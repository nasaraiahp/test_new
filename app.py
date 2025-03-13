from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import datetime
from database import init_db, db_session
from models import FileRecord
from config import UPLOAD_FOLDER, EXPIRATION_DAYS

app = Flask(__name__)
init_db()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    file_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_FOLDER, file_id)
    file.save(save_path)

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=EXPIRATION_DAYS)
    new_file = FileRecord(file_id=file_id, filename=filename, expiration=expiration_date, downloads=0, max_downloads=5)
    db_session.add(new_file)
    db_session.commit()

    return jsonify({'file_id': file_id, 'download_link': f'/download/{file_id}'}), 201

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    file_record = db_session.query(FileRecord).filter_by(file_id=file_id).first()
    
    if not file_record:
        return jsonify({'error': 'File not found'}), 404

    if file_record.expiration < datetime.datetime.utcnow():
        return jsonify({'error': 'File expired'}), 403
    
    if file_record.downloads >= file_record.max_downloads:
        return jsonify({'error': 'Download limit reached'}), 403

    file_record.downloads += 1
    db_session.commit()
    
    return send_from_directory(UPLOAD_FOLDER, file_id, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
