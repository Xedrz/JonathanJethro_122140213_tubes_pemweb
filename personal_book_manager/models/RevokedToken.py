
from sqlalchemy import Column, String
from .meta import Base

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    jti = Column(String, primary_key=True)

    def __repr__(self):
        return f"<RevokedToken(jti='{self.jti}')>"
