import os.path

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from flask import (Blueprint, render_template, request, redirect,
                   flash, current_app, url_for, jsonify, send_from_directory)
from flask_login import login_user, login_required, logout_user

from resourses.models import db, User, Articles
from resourses.forms import FormRegister, FormLogin

user_bp = Blueprint('verify', __name__, url_prefix='/verify')


@user_bp.route('/')
def users_db():
    users = User.query.all()
    return render_template('/users.html', users=users)


@user_bp.route('/subscribe', methods=['POST', 'GET'])
def user_register():
    form = FormRegister()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)
        users = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/')
        except Exception:
            db.session.rollback()
            raise 'Произошла ошибка при регистрации'
        finally:
            db.session.close()

    else:
        return render_template('registration/subscribe.html', form=form)


@user_bp.route('/login', methods=['POST', 'GET'])
def user_login():
    form = FormLogin()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = User.query.filter_by(email=email).first()

            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/home')
            else:
                flash('Неправильные email-адрес или пароль')
        else:
            flash('Заполните необходимые поля')
    else:
        return render_template('registration/login.html', form=form)


@user_bp.route('/logout')
@login_required
def user_logout():
    logout_user()
    return redirect('/')


@user_bp.route('/article', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form.get('title')
        intro = request.form.get('intro')
        content = request.form.get('content')
        tag = request.form.get('tag')

        article = Articles(title=title, intro=intro, content=content, tag=tag)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/verify')
        except Exception:
            db.session.rollback()
            raise 'Произошла ошибка при регистрации'
        finally:
            db.session.close()
    else:
        return render_template('article.html')


@user_bp.route('/upload_image', methods=['POST', 'GET'])
def upload_image():
    if 'upload' in request.files:
        image = request.files.get('upload')
        filename = secure_filename(image.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        try:
            image.save(filepath)
            file_url = url_for('uploaded_file', filename=filename)
            return jsonify({'url': file_url})
        except Exception:
            return jsonify({'error': {'message': 'Файл не загрузился'}})
    return jsonify({'error': {'message': 'Файл не найден'}})


@user_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
