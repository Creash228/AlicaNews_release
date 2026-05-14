import os
from werkzeug.utils import secure_filename
from models.news import News
from sqlalchemy import desc


class NewsService:
    
    @staticmethod
    def get_all_public(session, limit=10):
        return session.query(News).filter(
            News.is_private == False,
            News.is_published == True
        ).order_by(desc(News.created_at)).limit(limit).all()
    
    @staticmethod
    def get_by_id(session, news_id):
        return session.query(News).filter(News.id == news_id).first()
    
    @staticmethod
    def get_by_author(session, author_id, limit=10):
        return session.query(News).filter(
            News.author_id == author_id
        ).order_by(desc(News.created_at)).limit(limit).all()
    
    @staticmethod
    def create(session, title, content, author_id, is_private=False):
        news = News(
            title=title,
            content=content,
            author_id=author_id,
            is_private=is_private,
            is_published=True
        )
        session.add(news)
        session.commit()
        return news
    
    @staticmethod
    def update(session, news_id, title=None, content=None, is_private=None, image=None):
        news = NewsService.get_by_id(session, news_id)
        if news:
            if title:
                news.title = title
            if content:
                news.content = content
            if is_private is not None:
                news.is_private = is_private
            if image is not None:
                news.image = image
            session.commit()
        return news
    
    @staticmethod
    def delete(session, news_id):
        news = NewsService.get_by_id(session, news_id)
        if news:
            session.delete(news)
            session.commit()
            return True
        return False
    
    @staticmethod
    def save_image(file, news_id):
        if file and file.filename:
            filename = secure_filename(f"news_{news_id}_{file.filename}")
            upload_path = '/home/m/maksiy1x/maksiy1x.beget.tech/newproj/static/uploads/'
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            return f'/static/uploads/{filename}'
        return None
