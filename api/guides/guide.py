from flask import Blueprint, render_template
from database.models import Articles


guides_bp = Blueprint('guides', __name__, url_prefix='/guides')


@guides_bp.route('/')
def guides():
    tag = 'Гайды'
    articles = Articles.query.filter_by(tag=tag).all()
    return render_template('guides.html', articles=articles)