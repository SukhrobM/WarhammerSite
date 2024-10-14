from flask import Blueprint, render_template
from database.models import Articles


info_bp = Blueprint('info', __name__, url_prefix='/info')


@info_bp.route('/')
def info():
    tag = 'events'
    articles = Articles.query.filter_by(tag=tag).all()
    return render_template('info.html', articles=articles)
