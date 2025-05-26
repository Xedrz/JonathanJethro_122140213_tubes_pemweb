from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from ..models import Book, BookStatus
from ..services.api import OpenLibraryService
from personal_book_manager.views.auth import require_auth
from sqlalchemy.exc import IntegrityError
import logging
import transaction
from datetime import date

logger = logging.getLogger(__name__)


def parse_book_status(status_str):
    try:
        return BookStatus[status_str.upper()]
    except KeyError:
        raise ValueError(f"Status tidak valid: {status_str}. Gunakan salah satu: {[s.name for s in BookStatus]}")


# Endpoint untuk mendapatkan buku-buku yang dimiliki oleh user yang terautentikasi
from sqlalchemy import or_

@view_config(route_name='get_books', renderer='json', request_method='GET')
def get_books(request):
    search_query = request.params.get('query', '')  # Mendapatkan query dari parameter request
    logger.info(f"Mengambil buku dengan query: {search_query}")

    if search_query:  # Jika ada query pencarian
        # Cari buku berdasarkan judul atau penulis
        books = request.dbsession.query(Book).filter(
            or_(
                Book.title.ilike(f'%{search_query}%'),  # Pencarian berdasarkan judul
                Book.author.ilike(f'%{search_query}%')  # Pencarian berdasarkan penulis
            )
        ).all()
    else:
        # Jika tidak ada query pencarian, ambil semua buku
        books = request.dbsession.query(Book).all()

    return [book.to_dict() for book in books]  # Mengembalikan data buku dalam format JSON



# Endpoint untuk mencari buku berdasarkan judul
@view_config(route_name='book_search', renderer='json')
def book_search(request):
    query_param = request.params.get('q', '')
    if not query_param:
        return {'books': []}

    books = request.dbsession.query(Book).filter(
        Book.title.ilike(f'%{query_param}%')
    ).all()

    return {'books': [book.to_dict() for book in books]}


@view_config(route_name='book_add', request_method='POST', renderer='json')
def book_add(request):
    session = request.dbsession
    try:
        data = request.json_body

        # Validasi status
        status = data.get('status')
        if not status or status not in [e.value for e in BookStatus]:
            return Response("Invalid status value", status=400)

        # Membuat book baru tanpa user_id
        book = Book(
            openlibrary_id=data['openlibrary_id'],
            title=data['title'],
            author=data['author'],
            published_date=data['published_date'],
            cover_url=data['cover_url'],
            description=data['description'],
            pages=data['pages'],
            status=BookStatus(status),  # Konversi string ke enum
            rating=data['rating'],
            notes=data['notes'],
            user_id=None  # Tidak mengisi user_id
        )
        session.add(book)

        with transaction.manager:
            session.add(book)
        
        return Response("Book added successfully", status=201)
    
    except IntegrityError as e:
        session.rollback()
        return Response(f"Error: {str(e)}", status=400)



# Endpoint untuk mendapatkan daftar buku sesuai status tertentu
@view_config(route_name='book_list', renderer='json')
@require_auth
def book_list(request):
    status = request.params.get('status')
    query = request.dbsession.query(Book).filter(Book.user_id == request.user_id)

    if status:
        try:
            query = query.filter_by(status=parse_book_status(status))
        except ValueError:
            return {'books': []}

    books = query.order_by(Book.title).all()
    return {'books': [book.to_dict() for book in books]}

# Endpoint untuk mendapatkan detail buku
@view_config(route_name='book_detail', renderer='json')
@require_auth
def book_detail(request):
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).filter_by(id=book_id, user_id=request.user_id).first()

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    return {'book': book.to_dict()}

# Endpoint untuk mengupdate data buku (status, rating, notes)
@view_config(route_name='book_update', request_method='PUT', renderer='json')
@require_auth
def book_update(request):
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).filter_by(id=book_id, user_id=request.user_id).first()

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    try:
        json_data = request.json_body

        if 'status' in json_data:
            book.status = parse_book_status(json_data['status'])
        if 'rating' in json_data:
            book.rating = float(json_data['rating']) if json_data['rating'] else None
        if 'notes' in json_data:
            book.notes = json_data['notes']

        request.dbsession.commit()
        return {'success': True, 'book': book.to_dict()}

    except Exception as e:
        logger.error(f"Error saat mengupdate buku: {e}")
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'error': str(e)})


# Endpoint untuk menghapus buku
@view_config(route_name='book_delete', request_method='DELETE', renderer='json')
def book_delete(request):
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).filter_by(id=book_id).first()

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    try:
        request.dbsession.delete(book)
        # Jangan commit secara manual di sini!
        return {'success': True, 'message': 'Buku berhasil dihapus'}
    except Exception as e:
        logger.error(f"Error saat menghapus buku: {e}")
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'error': str(e)})


    
@view_config(route_name='book_interact', request_method='PATCH')
@require_auth
def book_interact(request):
    session = request.dbsession
    book_id = request.matchdict.get('id')
    data = request.json_body
    try:
        book = session.query(Book).filter_by(id=book_id, user_id=request.user_id).first()
        if not book:
            return Response("Book not found", status=404)

        # User hanya boleh mengubah rating & status
        if 'rating' in data:
            book.rating = data['rating']
        if 'status' in data and data['status'] in [e.value for e in BookStatus]:
            book.status = BookStatus(data['status'])
        book.updated_at = date.today()
        session.commit()
        return Response("Updated successfully", status=200)
    except Exception as e:
        session.rollback()
        return Response(f"Error: {str(e)}", status=400)


# Endpoint untuk mencari buku di OpenLibrary berdasarkan query
@view_config(route_name='openlibrary_search', renderer='json', request_method='GET')
def openlibrary_search(request):
    query_param = request.params.get('q', '')
    if not query_param:
        return {'books': []}
    books = OpenLibraryService.search_books(query_param)  # Menyearch buku berdasarkan query
    return {'books': books}

