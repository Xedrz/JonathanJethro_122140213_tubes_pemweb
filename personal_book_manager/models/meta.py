from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import threading

# Buat scoped session
DBSession = scoped_session(sessionmaker())
Base = declarative_base()

# Untuk thread safety 
thread_local = threading.local()
