Aplikasi Web Manajemen Buku Pribadi dengan Fitur Rating dan Status Buku
# BukuKu - Personal Book Manager API

## Deskripsi

BukuKu adalah aplikasi backend berbasis Python dengan framework Pyramid untuk manajemen buku pribadi.  
Aplikasi ini menyediakan RESTful API untuk menyimpan, mengambil, mengubah, dan menghapus data buku.  
Fitur utama mencakup pengelolaan status baca buku menggunakan enum (`WANT_TO_READ`, `READING`, `FINISHED`), rating, serta catatan pribadi.

API ini cocok digunakan sebagai backend aplikasi web atau mobile untuk membantu pengguna mengelola koleksi buku pribadi secara terstruktur dan transparan.

---

## Fitur

- **CRUD Buku**  
  - Create (Tambah buku baru)  
  - Read (Ambil data buku tunggal atau daftar semua buku)  
  - Update (Ubah data buku)  
  - Delete (Hapus buku dari database)  
- **Enum Status Buku**  
  Status baca buku menggunakan enum yang konsisten:  
  - `WANT_TO_READ` (ingin dibaca)  
  - `READING` (sedang dibaca)  
  - `FINISHED` (sudah selesai dibaca)  
- **Validasi data input** untuk menjaga integritas data  
- **Timestamp otomatis** untuk pencatatan waktu pembuatan dan pembaruan data  
- **Integrasi dengan OpenLibrary API** (opsional, jika ada) untuk pencarian buku dan import data  
- **Dukungan database PostgreSQL** dengan migrasi schema menggunakan Alembic

---

## Dependensi

- Python 3.8+  
- Pyramid (web framework)  
- SQLAlchemy (ORM)  
- Psycopg2 (PostgreSQL driver)  
- Alembic (migrasi database)  
- Gunicorn (untuk deployment, optional)  
- Requests (jika ada integrasi OpenLibrary API)

---

