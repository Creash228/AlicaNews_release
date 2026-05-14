from extensions import db
from models.base import BaseModel
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    about = db.Column(db.Text, nullable=True)
    
    news = db.relationship('News', back_populates='author', lazy='dynamic')
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)