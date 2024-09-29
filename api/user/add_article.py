import os

from flask import (Blueprint, request, render_template, flash, current_app,
                   url_for, jsonify, send_from_directory)
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename

from database.models import db, Articles
from database.forms import ArticleForm


article_bp = Blueprint('article', __name__, url_prefix='/article')
ckeditor = CKEditor()


@article_bp.route('/', methods=['POST', 'GET'])
def new_article():
    form = ArticleForm()
    if request.form == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        content = request.form['content']
        tag = request.form['tag']

        article = Articles(title=title, intro=intro, content=content, tag=tag)

        try:
            db.session.add(article)
            db.session.commit()
            flash('Статья добавлена')
            return render_template('article.html')
        except Exception:
            db.session.rollback()
            flash('Не получилось добавить статью')
            return render_template('article.html', form=form)
        finally:
            db.session.close()
    else:
        return render_template('article.html', form=form)


@article_bp.route('/upload_image', methods=['POST', 'GET'])
def upload_image():
    if 'upload' in request.files:
        image = request.files['upload']
        file_name = secure_filename(image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)

        try:
            image.save(filepath)
            file_url = url_for('uploaded_file', filename=file_name)
            return jsonify({'url': file_url})
        except Exception:
            return jsonify({'error': 'Файл не загрузился'})
    return jsonify({'error': {'message': 'Файл не найден'}})


@article_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
