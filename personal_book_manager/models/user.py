from sqlalchemy import Column, Integer, String
from .meta import Base
import bcrypt

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
