from flask import Blueprint, render_template

from database.models import Content

codex_bp = Blueprint('codexes', __name__, url_prefix='/codexes')


@codex_bp.route('/')
def codex():
    tag40k = 'codex40k'
    files40k = Content.query.filter_by(tag=tag40k).all()
    tagaos = 'codexaos'
    filesaos = Content.query.filter_by(tag=tagaos).all()
    return render_template('codexes.html', files40k=files40k, filesaos=filesaos)
