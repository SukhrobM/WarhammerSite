import os

from flask import (Blueprint, request, render_template, flash,
                   url_for, send_from_directory, redirect)
from flask_ckeditor import CKEditor, upload_fail, upload_success

from database.models import db, Articles
from database.forms import ArticleForm


article_bp = Blueprint('article', __name__, url_prefix='/article')
ckeditor = CKEditor()


@article_bp.route('/', methods=['POST', 'GET'])
def new_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        article = Articles(title=form.title.data, intro=form.intro.data, content=form.content.data, tag=form.tag.data)
        form.title.data = ''
        form.intro.data = ''
        form.content.data = ''
        form.tag.data = ''
        try:
            db.session.add(article)
            db.session.commit()
            flash('Статья добавлена')
            return render_template('article.html', form=form)
        except Exception as e:
            db.session.rollback()
            flash(f'Не получилось добавить статью: {str(e)}')
            return render_template('article.html', form=form)

    else:
        print(form.errors)
        return render_template('article.html', form=form)


@article_bp.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_article(id):
    form = ArticleForm()
    edit = Articles.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        edit.title = request.form['title']
        edit.intro = request.form['intro']
        edit.content = request.form['content']
        edit.tag = request.form['tag']
        try:
            db.session.commit()
            flash('Статья обновлена')
            return render_template('article.html', form=form)
        except Exception as e:
            db.session.rollback()
            flash(f'Не получилось обновить статью: {str(e)}')
            return render_template('article.html', form=form)
    else:
        form.title.data = edit.title
        form.intro.data = edit.intro
        form.content.data = edit.content
        form.tag.data = edit.tag
        return render_template('article.html', form=form)


@article_bp.route('/<int:id>')
def get_exact_article(id):
    article = Articles.query.get_or_404(id)
    return render_template('exact_article.html', article=article)


@article_bp.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_article(id):
    article_to_delete = Articles.query.get_or_404(id)
    next_url = request.args.get('next') or request.referrer or url_for('home.home')
    try:
        db.session.delete(article_to_delete)
        db.session.commit()
        flash('Статья удалена')
        return redirect(request.referrer)
    except Exception:
        flash('Произошла ошибка при удалении статьи')
        return redirect(next_url)


@article_bp.route('/upload_image', methods=['POST', 'GET'])
def upload_image():
    file = request.files.get('upload')
    extension = file.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'jpeg', 'png', 'gif']:
        return upload_fail(message='Неверный формат изображения')
    file.save(os.path.join('upload', file.filename))
    url = url_for('article.uploaded_files', filename=file.filename)
    return upload_success(url, filename=file.filename)


@article_bp.route('/upload/<path:filename>')
def uploaded_files(filename):
    path = 'upload'
    return send_from_directory(path, filename)
