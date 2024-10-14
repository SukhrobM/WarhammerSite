import os.path

from flask import (Blueprint, render_template, request, flash, send_from_directory,
                   current_app, url_for, redirect)
from werkzeug.utils import secure_filename

from database.models import db, Content
from database.forms import ContentForm
from api.content.content_functions import upload_file, upload_icon, updating_file, updating_icon


content_bp = Blueprint('content', __name__, url_prefix='/content')


@content_bp.route('/', methods=['POST', 'GET'])
def add_content():
    form = ContentForm()
    title = form.title.data
    web_link = form.web_link.data
    tag = form.tag.data
    icon_filename = ''
    file_filename = ''
    if request.method == 'POST' and form.validate_on_submit():
        file = form.file.data
        if file:
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension in ['pdf']:
                file_filename = secure_filename(f'{title}.{file_extension}')
                if not upload_file(file, file_filename):
                    return render_template('content.html', form=form)
            else:
                flash('Неверный формат файла')
                return render_template('content.html', form=form)
        icon = form.image.data
        if icon:
            icon_extension = icon.filename.split('.')[-1].lower()
            if icon_extension in ['jpg', 'jpeg', 'png', 'gif']:
                icon_filename = secure_filename(f'{title}.{icon_extension}')
                if not upload_icon(icon, icon_filename):
                    return render_template('content.html', form=form)
            else:
                flash('Неверный формат иконки')
        content = Content(title=title, web_link=web_link, tag=tag, icon_name=icon_filename, file_name=file_filename)
        try:
            db.session.add(content)
            db.session.commit()
            flash('Файлы добавлены')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка {str(e)}')
    return render_template('content.html', form=form)


@content_bp.route('/file_upload/<filename>')
def get_uploaded_files(filename):
    file_directory = current_app.config['FILES_UPLOAD_FOLDER']
    return send_from_directory(file_directory, filename)


@content_bp.route('/icon_upload/<filename>')
def get_uploaded_icon(filename):
    icon_directory = current_app.config['ICONS_UPLOAD_FOLDER']
    return send_from_directory(icon_directory, filename)


@content_bp.route('/edit_content/<int:id>', methods=['GET', 'POST'])
def edit_content(id):
    form = ContentForm()
    edit = Content.query.get_or_404(id)
    next_url = request.args.get('next') or request.referrer or url_for('home.home')
    if request.method == 'POST':
        edit.title = request.form['title']
        edit.web_link = request.form['web_link']
        edit.tag = request.form['tag']

        # Замена файла
        file = form.file.data
        if file:
            old_file_name = edit.file_name
            file_extension = file.filename.split('.')[-1].lower()
            new_file_name = secure_filename(f'{edit.title}.{file_extension}')
            if not updating_file(file, old_file_name, new_file_name):
                return render_template('content.html', form=form)
            edit.file_name = new_file_name

        # Замена иконки
        icon = form.image.data
        if icon:
            old_icon_name = edit.icon_name
            icon_extension = icon.filename.split('.')[-1].lower()
            new_icon_name = secure_filename(f'{edit.title}.{icon_extension}')
            if not updating_icon(icon, old_icon_name, new_icon_name):
                return render_template('contnet.html', form=form)
            edit.icon_name = new_icon_name

        # Обновление информации
        try:
            db.session.commit()
            flash('Контент обновлен')
            return render_template('content.html', form=form, next=next_url, delay=True)
        except Exception as e:
            flash(f'Ошибка при обновлении контента {str(e)}')
            return render_template('content.html', form=form)
    else:
        form.title.data = edit.title
        form.web_link.data = edit.web_link
        form.tag.data = edit.tag
        return render_template('content.html', form=form)


@content_bp.route('/delete_content/<int:id>', methods=['POST'])
def delete_content(id):
    file_directory = current_app.config['FILES_UPLOAD_FOLDER']
    icon_directory = current_app.config['ICONS_UPLOAD_FOLDER']
    to_delete = Content.query.get_or_404(id)
    next_url = request.args.get('next') or request.referrer or url_for('home.home')

    try:
        file = to_delete.file_name
        if file and os.path.exists(os.path.join(file_directory, file)):
            os.remove(os.path.join(file_directory, file))

        icon = to_delete.icon_name
        if icon and os.path.exists(os.path.join(icon_directory, icon)):
            os.remove(os.path.join(icon_directory, icon))

        db.session.delete(to_delete)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении контента {str(e)}')

    return redirect(next_url)
