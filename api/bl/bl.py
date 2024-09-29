from flask import Blueprint, render_template


bl_bp = Blueprint('bl', __name__, url_prefix='/bl')


@bl_bp.route('/')
def bl():
    return render_template('black_library.html')