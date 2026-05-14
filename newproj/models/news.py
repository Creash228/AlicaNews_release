from extensions import db
from models.base import BaseModel


class News(BaseModel):
    __tablename__ = 'news'
    
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    is_published = db.Column(db.Boolean, default=True)
    views_count = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200), nullable=True)  # путь к изображению
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    author = db.relationship('User', back_populates='news')
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'title': self.title,
            'content': self.content,
            'is_private': self.is_private,
            'is_published': self.is_published,
            'views_count': self.views_count,
            'author_id': self.author_id,
            'author_name': self.author.name if self.author else None,
            'image': self.image,
        })
        return data