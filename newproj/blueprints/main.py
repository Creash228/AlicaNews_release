from flask import Blueprint, render_template
from extensions import db
from services.news_service import NewsService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    news_list = NewsService.get_all_public(db.session, limit=20)
    return render_template('index.html', news_list=news_list)