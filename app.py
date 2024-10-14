import os

from flask import Flask
from flask_migrate import Migrate

from database.models import db, login_manager
from api.home.home_page import home_bp
from api.user.users import user_bp
from api.user.add_article import ckeditor, article_bp
from api.whaos.whaos import whaos_bp
from api.wh40k.wh40k import wh40k_bp
from api.bl.bl import bl_bp
from api.gallery.gallery import gallery_bp
from api.guides.guide import guides_bp
from api.info.info import info_bp
from api.about.about import aboutus_bs
from api.codex.codex import codex_bp
from api.errorpage import error_bp
from api.content.content import content_bp


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload/gallery')
FILES_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload/files')
ICONS_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload/icons')
app.config['CKEDITOR_FILE_UPLOADER'] = 'article.upload_image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FILES_UPLOAD_FOLDER'] = FILES_UPLOAD_FOLDER
app.config['ICONS_UPLOAD_FOLDER'] = ICONS_UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wh_database.db'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config['CSRF_KEYS'] = True
app.config['SECRET_KEY'] = 'eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IjVUZWFNNlVuSyIsImlhdCI6MTUxNjIzOTAyMn0'

db.init_app(app)
ckeditor.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)
app.register_blueprint(article_bp)
app.register_blueprint(whaos_bp)
app.register_blueprint(wh40k_bp)
app.register_blueprint(bl_bp)
app.register_blueprint(gallery_bp)
app.register_blueprint(guides_bp)
app.register_blueprint(info_bp)
app.register_blueprint(aboutus_bs)
app.register_blueprint(codex_bp)
app.register_blueprint(error_bp)
app.register_blueprint(content_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
