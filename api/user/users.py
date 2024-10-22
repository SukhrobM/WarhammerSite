from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from database.models import db, User
from database.forms import FormRegister, FormLogin

user_bp = Blueprint('verify', __name__, url_prefix='/verify')


@user_bp.route('/')
def users_db():
    users = User.query.all()
    return render_template('/users.html', users=users)


@user_bp.route('/regis', methods=['POST', 'GET'])
def user_register():
    form = FormRegister()
    next_url = request.args.get('next') or request.referrer or url_for('home.home')
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        form.username.data = ''
        form.email.data = ''
        form.password.data = ''

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(next_url)
        except Exception as e:
            db.session.rollback()
            flash(f'Произошла ошибка при регистрации: {str(e)}')
            return render_template('/registration/regis.html', form=form)
    else:
        return render_template('registration/regis.html', form=form)


@user_bp.route('/login', methods=['POST', 'GET'])
def user_login():
    form = FormLogin()
    next_url = request.args.get('next') or request.referrer or url_for('home.home')
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        if email and password:
            user = User.query.filter_by(email=email).first()

            if user is None:
                flash('Такого пользователя не существует')
                return render_template('registration/login.html', form=form)
            elif check_password_hash(user.password, password):
                login_user(user)
                return redirect(next_url)
            else:
                flash('Неправильные email-адрес или пароль')
                return render_template('registration/login.html', form=form)
    else:
        return render_template('registration/login.html', form=form)


@user_bp.route('/logout')
@login_required
def user_logout():
    next_page = request.args.get('next')
    logout_user()
    return redirect(next_page or url_for('home.home'))
