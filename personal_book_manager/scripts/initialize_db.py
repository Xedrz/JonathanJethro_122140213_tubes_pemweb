# initialize_db.py
from sqlalchemy import engine_from_config
from personal_book_manager.models.meta import Base
from personal_book_manager.models import User  # pastikan semua model diimpor
from pyramid.paster import get_appsettings

settings = get_appsettings('development.ini')  # atau 'production.ini'
engine = engine_from_config(settings, 'sqlalchemy.')

Base.metadata.create_all(engine)
