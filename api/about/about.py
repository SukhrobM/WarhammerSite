from flask import Blueprint, render_template
from database.models import Articles


aboutus_bs = Blueprint('about_us', __name__, url_prefix='/about_us')


@aboutus_bs.route('/')
def about_us():
    tag = 'О нас'
    articles = Articles.query.filter_by(tag=tag).all()
    return render_template('about_us.html', articles=articles)
