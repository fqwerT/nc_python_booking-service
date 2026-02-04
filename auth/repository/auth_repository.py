from sqlalchemy.orm import Session

from auth.model.auth_model import User


class AuthRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_email(self, email: str) -> User | None:
        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, email: str, full_name: str, avatar: str, password_hash: str, id:str) -> User:
        user = User(
            email=email,
            full_name=full_name,
            avatar=avatar,
            password_hash=password_hash,
            id=id
    
            
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user