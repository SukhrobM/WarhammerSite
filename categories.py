import os.path

from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, request, current_app, send_from_directory, flash, redirect, url_for, \
    jsonify
from resourses.models import Articles


home_bp = Blueprint('home', __name__)


@home_bp.route('/')
@home_bp.route('/home')
def home_page():
    return render_template('home.html')


whaos_bp = Blueprint('whaos', __name__, url_prefix='/whaos')


@whaos_bp.route('/')
def wh_aos():
    return render_template('whaos.html')


wh40k_bp = Blueprint('wh40k', __name__, url_prefix='/wh40k')


@wh40k_bp.route('/')
def wh_40k():
    return render_template('wh40k.html')


bl_bp = Blueprint('bl', __name__, url_prefix='/bl')


@bl_bp.route('/')
def bl():
    return render_template('black_library.html')


codexes_bp = Blueprint('codexes', __name__, url_prefix='/codexes')


@codexes_bp.route('/')
def codexes():
    return render_template('codexes.html')


gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@gallery_bp.route('/')
def gallery():
    files = os.listdir(current_app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', files=files)


@gallery_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@gallery_bp.route('/upload', methods=['POST', 'GET'])
def upload_to_gallery():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Нет файла'

        file = request.files['file']
        if file.filename == '':
            return 'Файл не выбран'

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash(f'Файл {filename} успешно загружен')
            return redirect('/gallery')
    return render_template('upload.html')


guides_bp = Blueprint('guides', __name__, url_prefix='/guides')


@guides_bp.route('/')
def guides():
    return render_template('guides.html')


info_bp = Blueprint('info', __name__, url_prefix='/info')


@info_bp.route('/')
def info():
    tag = 'Полезная информация'
    articles = Articles.query.filter_by(tag=tag).all()
    return render_template('info.html', articles=articles)


aboutus_bs = Blueprint('about_us', __name__, url_prefix='/about_us')


@aboutus_bs.route('/')
def about_us():
    tag = 'О нас'
    articles = Articles.query.filter_by(tag=tag).all()
    return render_template('about_us.html', articles=articles)
