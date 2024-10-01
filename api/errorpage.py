from flask import Blueprint, render_template

error_bp = Blueprint('error', __name__)


@error_bp.app_errorhandler(404)
def page_not_found(e):
    error_code = 404
    return render_template('error.html', error_code=error_code), 404


@error_bp.app_errorhandler(500)
def page_not_found(e):
    error_code = 500
    return render_template('error.html', error_code=error_code), 500
