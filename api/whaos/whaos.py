from flask import Blueprint, render_template


whaos_bp = Blueprint('whaos', __name__, url_prefix='/whaos')


@whaos_bp.route('/')
def wh_aos():
    return render_template('whaos.html')
