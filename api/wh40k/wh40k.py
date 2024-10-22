from flask import Blueprint, render_template
from database.models import Content


wh40k_bp = Blueprint('wh40k', __name__, url_prefix='/wh40k')


@wh40k_bp.route('/')
def wh_40k():
    tag40k = 'codex40k'
    files40k = Content.query.filter_by(tag=tag40k).all()
    return render_template('wh40k.html', files40k=files40k)
