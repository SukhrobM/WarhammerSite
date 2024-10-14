import os

from flask import (Blueprint, render_template, current_app, send_from_directory,
                   request, flash)
from werkzeug.utils import secure_filename


gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@gallery_bp.route('/')
def gallery():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', files=files)


@gallery_bp.route('/upload', methods=['POST', 'GET'])
def upload_to_gallery():
    if request.method == 'POST':
        file = request.files['file']

        if 'file' not in request.files:
            flash('Нет файла для загрузки')
            return render_template('upload.html')

        elif file.filename == '':
            flash('Файл не выбран')
            return render_template('upload.html')

        elif file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash(f'Файл {filename} успешно загружен')
            return render_template('upload.html')
    return render_template('upload.html')


@gallery_bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
