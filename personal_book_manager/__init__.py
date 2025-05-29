from pyramid.config import Configurator
from pyramid.events import NewRequest, NewResponse
from pyramid.response import Response
from pyramid.authorization import ACLAuthorizationPolicy  # Tambahkan ini
from sqlalchemy import engine_from_config
from jwt import decode as jwt_decode, InvalidTokenError, ExpiredSignatureError
from pyramid_jwt import JWTAuthenticationPolicy
from personal_book_manager.security import get_secret_key
from .models import DBSession, Base
import logging
from .views.books import cors_options_view



log = logging.getLogger(__name__)

# ---------------- JWT Custom Policy ---------------- #
class CustomJWTAuthenticationPolicy(JWTAuthenticationPolicy):
    def unauthenticated_userid(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt_decode(token, get_secret_key(), algorithms=["HS256"])
                return int(payload.get("sub"))
            except (InvalidTokenError, ExpiredSignatureError):
                return None
        return None

# ---------------- CORS Configuration ---------------- #


def configure_cors(event):
    request = event.request
    response = event.response
    
    # Set CORS headers for all responses
    response.headers.update({
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With',
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '86400',
    })

    # Handle preflight requests
    if request.method == 'OPTIONS':
        response.headers.update({
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        })
        return response
# ---------------- App Factory ---------------- #
def main(global_config, **settings):
    # Koneksi ke database
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Konfigurasi aplikasi Pyramid
    config = Configurator(settings=settings)
    config.include('cornice')
    config.include('pyramid_tm')
    config.include('pyramid_jwt')
    config.include('pyramid_retry')
    config.include('.models')
    config.include('.routes')
    
    config.add_static_view(name='static', path='personal_book_manager:static')
    config.add_tween('personal_book_manager.cors.cors_tween_factory')
    # Konfigurasi JWT Authentication
    jwt_secret = settings.get('jwt.secret')
    authn_policy = CustomJWTAuthenticationPolicy(jwt_secret, algorithm='HS256', auth_type='Bearer')
    config.set_authentication_policy(authn_policy)

    # Konfigurasi Authorization Policy
    authz_policy = ACLAuthorizationPolicy()  # Menambahkan authorization policy
    config.set_authorization_policy(authz_policy)

    # Apply CORS configuration using Cornice

    config.add_subscriber(configure_cors, NewResponse)

    config.add_view(route_name='book_add', request_method='OPTIONS', view=cors_options_view)

    # Menambahkan subscriber untuk JWT Claims ke request
    def add_jwt_user_id(event):
        request = event.request
        request.jwt_claims = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt_decode(token, get_secret_key(), algorithms=["HS256"])
                request.jwt_claims = payload
            except (InvalidTokenError, ExpiredSignatureError):
                pass

    # Menambahkan subscriber di sini menggunakan add_subscriber
    config.add_subscriber(add_jwt_user_id, NewRequest)

    config.scan()
    return config.make_wsgi_app()
