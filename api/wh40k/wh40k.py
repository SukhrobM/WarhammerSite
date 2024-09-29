from flask import Blueprint, render_template


wh40k_bp = Blueprint('wh40k', __name__, url_prefix='/wh40k')


@wh40k_bp.route('/')
def wh_40k():
    return render_template('wh40k.html')
