from models.user import User


class UserService:
    
    @staticmethod
    def get_by_email(session, email):
        return session.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_id(session, user_id):
        return session.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create(session, name, email, password):
        user = User(name=name, email=email)
        user.set_password(password)
        session.add(user)
        session.commit()
        return user
