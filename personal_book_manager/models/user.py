from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .meta import Base
import bcrypt

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    # Fungsi untuk meng-hash password sebelum disimpan ke database
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # Fungsi untuk memverifikasi password
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    # Relasi 1-to-many dengan buku
    books = relationship("Book", back_populates="user")
