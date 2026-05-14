from flask import Blueprint, request, jsonify
import logging
from extensions import db
from services.news_service import NewsService

alice_bp = Blueprint('alice', __name__)


@alice_bp.route('/post', methods=['GET', 'POST'])
def webhook():
    
    if request.method == 'GET':
        return jsonify({'status': 'ok'}), 200
    

    req = request.json
    logging.info(f'Alice request: {req}')


    res = {
        'session': req.get('session', {}),
        'version': req.get('version', '1.0'),
        'response': {
            'end_session': False,
            'text': '',
            'tts': ''
        }
    }
    

    command = req.get('request', {}).get('command', '').lower()
    
    
    if 'новости' in command or 'расскажи' in command:
        news_list = NewsService.get_all_public(db.session, limit=5)
        if news_list:
            titles = [f"{i+1}. {n.title}" for i, n in enumerate(news_list)]
            text = "Вот последние новости:\n" + "\n".join(titles)
            tts = "Вот последние новости: " + ", ".join(titles)
        else:
            text = 'Новостей пока нет. Добавьте первую через сайт!'
            tts = 'Новостей пока нет'
    else:
        text = 'Скажите "расскажи новости"'
        tts = 'Скажите рассказать новости'
    
    res['response']['text'] = text
    res['response']['tts'] = tts
    
    return jsonify(res), 200