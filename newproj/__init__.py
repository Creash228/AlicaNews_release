from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv('/home/m/maksiy1x/maksiy1x.beget.tech/newproj/.env')

app = Flask(__name__, static_folder='static', static_url_path='/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from extensions import db, login_manager

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.news import news_bp
from alice import alice_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')
app.register_blueprint(alice_bp, url_prefix='/alice')

with app.app_context():
    db.create_all()