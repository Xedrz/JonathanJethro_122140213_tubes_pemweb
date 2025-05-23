from sqlalchemy import Column, Integer, String, Text, Date, Enum, Float
from sqlalchemy.sql import func
from .meta import Base
import enum

class BookStatus(enum.Enum):
    WANT_TO_READ = "WANT_TO_READ"
    READING = "READING"
    FINISHED = "FINISHED"
    

class Book(Base):
    """Model untuk tabel buku pribadi"""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    openlibrary_id = Column(String(255), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    published_date = Column(Date)
    cover_url = Column(String(512))
    description = Column(Text)
    pages = Column(Integer)

    # Tambahkan name="bookstatus" untuk kompatibilitas PostgreSQL
    status = Column(Enum(BookStatus, name="bookstatus", values_callable=lambda x: [e.value for e in x]), nullable=False)

    rating = Column(Float)
    notes = Column(Text)
    created_at = Column(Date, server_default=func.now())
    updated_at = Column(Date, onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'openlibrary_id': self.openlibrary_id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'cover_url': self.cover_url,
            'description': self.description,
            'pages': self.pages,
            'status': self.status.value if self.status else None,
            'rating': self.rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
