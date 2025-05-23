from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:5432@localhost:5432/bookdb')

try:
    with engine.connect() as conn:
        print("Koneksi berhasil!")
except Exception as e:
    print("Koneksi gagal:", e)
