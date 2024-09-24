import os

from flask import Flask, url_for

from resourses.models import db, login_manager
from user_verify import user_bp
from categories import (home_bp, whaos_bp, wh40k_bp, bl_bp,
                        gallery_bp, guides_bp, info_bp, aboutus_bs, codexes_bp)


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wh.db'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
app.config['CSRF_KEYS'] = True
app.config['SECRET_KEY'] = ''

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
app.register_blueprint(whaos_bp)
app.register_blueprint(wh40k_bp)
app.register_blueprint(bl_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(guides_bp)
app.register_blueprint(info_bp)
app.register_blueprint(aboutus_bs)
app.register_blueprint(codexes_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
