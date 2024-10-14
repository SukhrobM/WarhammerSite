import os

from flask import flash, current_app


def upload_file(file, file_filename):
    file_directory = current_app.config['FILES_UPLOAD_FOLDER']
    files_folder = current_app.config.get('FILES_UPLOAD_FOLDER')
    if not files_folder:
        flash('Отсутствует путь для файлов')
        return False
    try:
        file.save(os.path.join(file_directory, file_filename))
        flash('Файл сохранен')
        return True
    except Exception as e:
        flash(f'Ошибка в загрузке файла {str(e)}')
        return False


def upload_icon(icon, image_filename):
    icon_directory = current_app.config['ICONS_UPLOAD_FOLDER']
    icon_folder = current_app.config.get('ICONS_UPLOAD_FOLDER')
    if not icon_folder:
        flash('Отсутствует путь для иконок')
        return False
    try:
        icon.save(os.path.join(icon_directory, image_filename))
        flash('Иконка добавлена')
        return True
    except Exception as e:
        flash(f'Ошибка в загрузке иконки {str(e)}')
        return False


def updating_file(file, old_file_name, new_file_name):
    file_directory = current_app.config['FILES_UPLOAD_FOLDER']
    try:
        if old_file_name and os.path.exists(os.path.join(file_directory, old_file_name)):
            os.remove(os.path.join(file_directory, old_file_name))
            return True
    except Exception as e:
        flash(f'Ошибка при удалении старого файла {str(e)}')
        return False
    try:
        file.save(os.path.join(file_directory, new_file_name))
        flash('Файл обновлен')
    except Exception as e:
        flash(f'Ошибка при обновлении файла {str(e)}')


def updating_icon(icon, old_icon_name, new_icon_name):
    icon_directory = current_app.config['ICONS_UPLOAD_FOLDER']
    try:
        if old_icon_name and os.path.exists(os.path.join(icon_directory, old_icon_name)):
            os.remove(os.path.join(icon_directory, old_icon_name))
            return True
    except Exception as e:
        flash(f'Ошибка при удалении иконки {str(e)}')
        return False
    try:
        icon.save(os.path.join(icon_directory, new_icon_name))
        flash('Иконка обновлена')
        return True
    except Exception as e:
        flash(f'Ошибка при обновлении иконки {str(e)}')
