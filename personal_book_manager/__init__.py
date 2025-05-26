from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.response import Response
from sqlalchemy import engine_from_config
from .models import DBSession, Base
from .views.books import openlibrary_search


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    
    # 1. Konfigurasi koneksi database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    # 2. Include eksternal Pyramid
    config.add_route('openlibrary_search', '/openlibrary/search') 
    config.include('pyramid_tm')
    config.include('pyramid_retry')
    config.include('.models')
    config.include('.routes')

    # 3. Middleware CORS — ditambahkan ke semua response
    def add_cors_headers_response_callback(event):
        def cors_headers(request, response):
            response.headers.update({
                'Access-Control-Allow-Origin': 'http://localhost:3000', 
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true',
            })
        event.request.add_response_callback(cors_headers)

    config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    # 4. View handler khusus untuk menangani semua OPTIONS request di semua route
    def global_options_view(request):
        return Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': 'http://localhost:3000',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true',
            }
        )

    # 5. Tambahkan route catch-all untuk menangani OPTIONS request pada semua route
    config.add_route('cors_options_preflight', '/*subpath')
    config.add_view(global_options_view, route_name='cors_options_preflight', request_method='OPTIONS')

    # 6. Scan views dan kembalikan aplikasi
    config.scan()
    return config.make_wsgi_app()
