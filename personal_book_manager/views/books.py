from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from ..models import Book, BookStatus
from personal_book_manager.views.auth import require_auth
from sqlalchemy.exc import IntegrityError
import logging
from datetime import datetime
import os
import uuid
import shutil


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
logger = logging.getLogger(__name__)


def parse_book_status(status_str):
    try:
        return BookStatus[status_str.upper()]
    except KeyError:
        raise ValueError(f"Status tidak valid: {status_str}. Gunakan salah satu: {[s.name for s in BookStatus]}")


# Endpoint untuk mendapatkan buku-buku yang dimiliki oleh user yang terautentikasi
from sqlalchemy import or_

@view_config(route_name='get_books', renderer='json', request_method='GET')
@require_auth
def get_books(request):
    try:
        search_query = request.params.get('query', '')
        query = request.dbsession.query(Book).filter(Book.user_id == request.user_id)

        if search_query:
            query = query.filter(
                or_(
                    Book.title.ilike(f'%{search_query}%'),
                    Book.author.ilike(f'%{search_query}%')
                )
            )

        # Selalu urutkan berdasarkan judul secara ascending
        books = query.order_by(Book.title.asc()).all()
        
        return {
            'success': True,
            'books': [book.to_dict() for book in books]
        }
    except Exception as e:
        logging.error(f"Error fetching books: {str(e)}")
        return {'success': False, 'message': 'Failed to fetch books'}

@view_config(route_name='book_add', request_method='POST', renderer='json')
@require_auth
def book_add(request):
    try:
        # Handle JSON data
        if request.content_type == 'application/json':
            data = request.json_body
        # Handle FormData
        else:
            data = {
                'title': request.POST.get('title', 'Untitled'),
                'author': request.POST.get('author', 'Unknown'),
                'description': request.POST.get('description', ''),
            }

        if not data.get('title'):
            return HTTPBadRequest(json_body={'error': 'Title is required'})

        book = Book(
            title=data.get('title', 'Untitled'),
            author=data.get('author', 'Unknown'),
            description=data.get('description', ''),
            status=BookStatus.UNREAD,
            user_id=request.user_id
        )

        request.dbsession.add(book)
        request.dbsession.flush()
        
        # Handle file upload if exists
        if 'file' in request.POST:
            file = request.POST['file'].file
            filename = request.POST['file'].filename
            if allowed_file(filename):
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"{uuid.uuid4()}.{ext}"
                file_path = os.path.join(UPLOAD_FOLDER, new_filename)
                
                with open(file_path, 'wb') as output_file:
                    shutil.copyfileobj(file, output_file)
                
                book.cover_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        
        return {'success': True, 'book': book.to_dict()}
    except Exception as e:
        logger.error(f"Error adding book: {str(e)}", exc_info=True)
        request.dbsession.rollback()
        return HTTPBadRequest(json_body={'error': 'Failed to add book'})


@view_config(route_name='book_search', renderer='json', request_method='GET')
@require_auth
def book_search(request):
    query_param = request.params.get('q', '').strip()
    
    if not query_param:
        return {'books': []}

    # Pencarian buku di database lokal berdasarkan judul
    books = request.dbsession.query(Book).filter(Book.title.ilike(f'%{query_param}%')).all()
    
    result = []
    for book in books:
        result.append({
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'isbn': book.isbn,  # Ganti jika ISBN atau field lain yang diinginkan
        })
    return {'books': result}


# Endpoint untuk mendapatkan daftar buku sesuai status tertentu
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@view_config(route_name='upload_cover', request_method='POST', renderer='json')
@require_auth
def upload_cover(request):
    try:
        book_id = request.matchdict['id']
        book = request.dbsession.query(Book).filter(
            Book.id == book_id,
            Book.user_id == request.user_id
        ).first()

        if not book:
            return HTTPNotFound(json_body={'error': 'Book not found'})

        file = request.POST['file'].file
        filename = request.POST['file'].filename

        if not allowed_file(filename):
            return HTTPBadRequest(json_body={'error': 'File type not allowed'})

        # Buat direktori upload jika belum ada
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Generate nama file unik
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4()}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)

        # Simpan file
        with open(file_path, 'wb') as output_file:
            shutil.copyfileobj(file, output_file)

        # Simpan URL cover ke database
        book.cover_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        request.dbsession.flush()

        return {
            'success': True,
            'cover_url': book.cover_url,
            'message': 'Cover uploaded successfully'
        }
    except Exception as e:
        logger.error(f"Error uploading cover: {str(e)}", exc_info=True)
        return HTTPBadRequest(json_body={'error': 'Failed to upload cover'})

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
    try:
        book_id = int(request.matchdict['id'])
        book = request.dbsession.query(Book).filter(
            Book.id == book_id,
            Book.user_id == request.user_id
        ).first()

        if not book:
            return HTTPNotFound(json_body={'error': 'Book not found'})

        data = request.json_body

        # Update status
        if 'status' in data:
            try:
                book.status = BookStatus[data['status'].upper()]
            except KeyError:
                return HTTPBadRequest(json_body={
                    'error': f'Invalid status: {data["status"]}. Use UNREAD, READING, or FINISHED'
                })

        # Update rating
        if 'rating' in data:
            try:
                rating = float(data['rating'])
                if rating < 0 or rating > 5:
                    return HTTPBadRequest(json_body={'error': 'Rating must be between 0 and 5'})
                book.rating = rating
            except (ValueError, TypeError):
                return HTTPBadRequest(json_body={'error': 'Rating must be a number'})

        # Update description
        if 'description' in data:
            book.description = data['description']

        return {
            'success': True,
            'book': book.to_dict(),
            'message': 'Book updated successfully'
        }
    except Exception as e:
        logger.error(f"Error updating book: {str(e)}", exc_info=True)
        return HTTPBadRequest(json_body={'error': str(e)})

@view_config(route_name='book_delete', request_method='DELETE', renderer='json')
@require_auth
def book_delete(request):
    try:
        book_id = int(request.matchdict['id'])
        book = request.dbsession.query(Book).filter(
            Book.id == book_id,
            Book.user_id == request.user_id
        ).first()

        if not book:
            return HTTPNotFound(json_body={'error': 'Book not found'})

        request.dbsession.delete(book)
        return {'success': True, 'message': 'Book deleted successfully'}
    except Exception as e:
        logger.error(f"Error deleting book: {str(e)}", exc_info=True)
        return HTTPBadRequest(json_body={'error': 'Failed to delete book'})
    
@view_config(route_name='books_options', request_method='OPTIONS')
def books_options(request):
    return Response(
        headers={
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }
    )

@view_config(route_name='books_id_options', request_method='OPTIONS')
def books_id_options(request):
    return Response(
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }
    )
    
@view_config(route_name='books_add_options', request_method='OPTIONS')
def books_add_options(request):
    return Response(
        headers={
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }
    )
    
@view_config(request_method='OPTIONS')
def cors_options_view(request):
    response = Response()
    response.headers.update({
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '86400',
    })
    return response

