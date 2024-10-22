from flask import Blueprint, render_template

from database.models import Content

bl_bp = Blueprint('bl', __name__, url_prefix='/bl')


@bl_bp.route('/')
def bl():
    tag40k = 'wh40'
    books40k = Content.query.filter_by(tag=tag40k).all()
    tagaos = 'whaos'
    booksaos = Content.query.filter_by(tag=tagaos).all()
    return render_template('black_library.html', books40k=books40k, booksaos=booksaos)
