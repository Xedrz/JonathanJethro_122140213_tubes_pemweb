from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from ..models import Book, BookStatus
from ..services.api import OpenLibraryService
import datetime
from personal_book_manager.utils.jwt import verify_jwt

@view_config(route_name='protected', renderer='json')
def protected_view(request):
    payload = verify_jwt(request)
    user_id = payload.get("sub")
    return {"message": f"Hello, user {user_id}!"}


def parse_book_status(value):
    """Mengubah input string menjadi enum BookStatus dari nama atau nilai"""
    try:
        return BookStatus[value]  
    except KeyError:
        for status in BookStatus:
            if status.value == value:  
                return status
    raise ValueError(f"Status tidak valid: {value}")

@view_config(route_name='book_search', renderer='json')
def book_search(request):
    """Mencari buku di koleksi pribadi berdasarkan judul"""
    query_param = request.params.get('q', '')
    if not query_param:
        return {'books': []}
    
    books = request.dbsession.query(Book).filter(Book.title.ilike(f'%{query_param}%')).all()
    return {'books': [book.to_dict() for book in books]}

@view_config(route_name='book_add', request_method='POST', renderer='json')
def book_add(request):
    """Menambahkan buku ke koleksi pribadi"""
    try:
        json_data = request.json_body

        if 'openlibrary_id' not in json_data or 'title' not in json_data:
            return HTTPBadRequest(json_body={'error': 'OpenLibrary ID dan title wajib diisi'})

        existing = request.dbsession.query(Book).filter_by(
            openlibrary_id=json_data['openlibrary_id']).first()
        if existing:
            return HTTPBadRequest(json_body={'error': 'Buku sudah ada di koleksi'})

        # Dapatkan detail lengkap dari OpenLibrary jika diperlukan
        if not all(key in json_data for key in ['author', 'cover_url']):
            ol_book = OpenLibraryService.get_book_details(json_data['openlibrary_id'])
            if ol_book:
                json_data.update(ol_book)

        status_enum = parse_book_status(json_data.get('status', 'Want to Read'))

        book = Book(
            openlibrary_id=json_data['openlibrary_id'],
            title=json_data['title'],
            author=json_data.get('author'),
            published_date=datetime.datetime.strptime(json_data['published_date'], '%Y-%m-%d').date()
                if json_data.get('published_date') else None,
            cover_url=json_data.get('cover_url'),
            description=json_data.get('description'),
            pages=json_data.get('pages'),
            status=status_enum,
            rating=float(json_data['rating']) if 'rating' in json_data else None,
            notes=json_data.get('notes')
        )

        request.dbsession.add(book)
        return {'success': True, 'book': book.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='book_list', renderer='json')
def book_list(request):
    """Mendapatkan daftar buku pribadi"""
    status = request.params.get('status')
    query = request.dbsession.query(Book)

    if status:
        try:
            status_enum = parse_book_status(status)
            query = query.filter_by(status=status_enum)
        except ValueError:
            return {'books': []}

    books = query.order_by(Book.title).all()
    return {'books': [book.to_dict() for book in books]}

@view_config(route_name='book_detail', renderer='json')
def book_detail(request):
    """Mendapatkan detail buku pribadi"""
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).get(book_id)

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    return {'book': book.to_dict()}

@view_config(route_name='book_update', request_method='PUT', renderer='json')
def book_update(request):
    """Mengupdate data buku pribadi"""
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).get(book_id)

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    try:
        json_data = request.json_body

        if 'status' in json_data:
            try:
                book.status = parse_book_status(json_data['status'])
            except ValueError:
                return HTTPBadRequest(json_body={'error': 'Status tidak valid'})
        if 'rating' in json_data:
            book.rating = float(json_data['rating']) if json_data['rating'] else None
        if 'notes' in json_data:
            book.notes = json_data['notes']

        return {'success': True, 'book': book.to_dict()}

    except Exception as e:
        return HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='book_delete', request_method='DELETE', renderer='json')
def book_delete(request):
    """Menghapus buku dari koleksi pribadi"""
    book_id = request.matchdict['id']
    book = request.dbsession.query(Book).get(book_id)

    if not book:
        return HTTPNotFound(json_body={'error': 'Buku tidak ditemukan'})

    request.dbsession.delete(book)
    return {'success': True, 'message': 'Buku berhasil dihapus'}

