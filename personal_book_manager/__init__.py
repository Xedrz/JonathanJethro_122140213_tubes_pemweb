from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.response import Response
from sqlalchemy import engine_from_config
from .models import DBSession, Base

def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    # Konfigurasi engine dan session database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    config.include('pyramid_retry')
    config.include('.models')
    config.include('.routes')

    # Middleware CORS
    def add_cors_headers_response_callback(event):
        def cors_headers(request, response):
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            })
            return response
        event.request.add_response_callback(cors_headers)

    config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    # Menangani request OPTIONS (preflight CORS)
    config.add_route('options', '/{path:.*}')
    config.add_view(lambda r: Response(status=200), route_name='options', request_method='OPTIONS')

    config.scan()
    return config.make_wsgi_app()
