from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True)
    jti = Column(String(255), unique=True, nullable=False)
    revoked_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<RevokedToken(id={self.id}, jti='{self.jti}', revoked_at={self.revoked_at})>"
