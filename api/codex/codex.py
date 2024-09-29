from flask import Blueprint, render_template


codex_bp = Blueprint('codexes', __name__, url_prefix='/codexes')


@codex_bp.route('/')
def codex():
    return render_template('codexes.html')
