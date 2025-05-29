from sqlalchemy import Column, Integer, String, Text, Date, Enum, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .meta import Base
import enum
from sqlalchemy.exc import IntegrityError


class BookStatus(enum.Enum):
    UNREAD = "UNREAD"
    READING = "READING"
    FINISHED = "FINISHED"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    description = Column(Text, nullable=True)
    cover_url = Column(String(512), nullable=True)  
    status = Column(Enum(BookStatus), default=BookStatus.UNREAD)
    rating = Column(Float, default=0.0)


    # Relasi ke User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship("User", back_populates="books")

    def to_dict(self):
        return {
        'id': self.id,
        'title': self.title,
        'author': self.author,
        'description': self.description,
        'cover_url': self.cover_url,
        'status': self.status.value if self.status else 'UNREAD',
        'rating': self.rating if self.rating is not None else 0,
        }

# Fungsi untuk memastikan status valid
def is_valid_status(status):
    try:
        BookStatus(status)  # Coba untuk mengonversi string ke enum
        return True
    except ValueError:
        return False

