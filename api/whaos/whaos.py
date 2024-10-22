from flask import Blueprint, render_template

from database.models import Content

whaos_bp = Blueprint('whaos', __name__, url_prefix='/whaos')


@whaos_bp.route('/')
def wh_aos():
    tag = 'codexaos'
    filesaos = Content.query.filter_by(tag=tag).all()
    return render_template('whaos.html', filesaos=filesaos)
