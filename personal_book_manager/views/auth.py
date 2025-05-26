from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized
from ..models import User
from sqlalchemy import or_
from personal_book_manager.security import create_token
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError
from personal_book_manager.security import get_secret_key
import bcrypt
from pyramid.response import Response

ALGORITHM = 'HS256'


@view_config(route_name='register', renderer='json', request_method=['POST', 'OPTIONS'])
def register(request):
    if request.method == 'OPTIONS':
        return Response(status=200)

    try:
        data = request.json_body
    except Exception:
        return HTTPBadRequest(json_body={"error": "Invalid JSON"})

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return HTTPBadRequest(json_body={"error": "All fields are required"})

    existing_user = request.dbsession.query(User).filter(
        or_(User.username == username, User.email == email)
    ).first()
    if existing_user:
        return HTTPBadRequest(json_body={"error": "User already exists"})

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, email=email, password_hash=hashed)
    request.dbsession.add(user)
    return {"message": "Registered successfully"}


@view_config(route_name='login', renderer='json', request_method=['POST', 'OPTIONS'])
def login(request):
    if request.method == 'OPTIONS':
        return Response(status=200)

    try:
        data = request.json_body
    except Exception:
        return HTTPBadRequest(json_body={"error": "Invalid JSON"})

    identifier = data.get('username') or data.get('email')
    password = data.get('password')

    if not identifier or not password:
        return HTTPBadRequest(json_body={"error": "Email/Username and password required"})

    user = request.dbsession.query(User).filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if not user or not user.verify_password(password):
        return HTTPUnauthorized(json_body={"error": "Invalid credentials"})

    token = create_token(user.id)
    return {"token": token}


def require_auth(view_func):
    def wrapper(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPUnauthorized(json_body={'error': 'Authorization header missing or invalid'})

        token = auth_header.split(' ')[1]
        try:
            payload = jwt_decode(token, get_secret_key(), algorithms=[ALGORITHM])
            request.user_id = int(payload['sub'])
        except ExpiredSignatureError:
            raise HTTPUnauthorized(json_body={'error': 'Token kadaluarsa'})
        except InvalidTokenError:
            raise HTTPUnauthorized(json_body={'error': 'Token tidak valid'})

        return view_func(request)
    return wrapper
