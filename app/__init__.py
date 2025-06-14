from pathlib import Path
import os
from flask import Flask
from werkzeug.utils import secure_filename
from .database.db import db, DATABASE_URL

# Config
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1000 * 1000
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# App
app = Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

db.init_app(app)

from . import forms
from .routes.main import bp as main_bp
from .routes.actividad import bp as actividad_bp

# Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(actividad_bp)