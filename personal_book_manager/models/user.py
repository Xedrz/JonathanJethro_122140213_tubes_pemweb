from .meta import Base
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import bcrypt

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    password_hash = Column(Text)

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True)
    jti = Column(String(255), unique=True)


