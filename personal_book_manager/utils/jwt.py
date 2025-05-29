import jwt
from pyramid.httpexceptions import HTTPUnauthorized
from personal_book_manager.security import get_secret_key

ALGORITHM = 'HS256'

def verify_jwt(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPUnauthorized("Missing Authorization header")

    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        raise HTTPUnauthorized("Invalid Authorization header")

    token = parts[1]
    try:
        
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPUnauthorized("Token expired")
    except jwt.InvalidTokenError:
        raise HTTPUnauthorized("Invalid token")
