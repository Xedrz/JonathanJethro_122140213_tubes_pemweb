import jwt
from datetime import datetime, timedelta
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.threadlocal import get_current_registry
from jwt import ExpiredSignatureError, InvalidTokenError

ALGORITHM = 'HS256'

def get_secret_key():
    settings = get_current_registry().settings
    return settings.get("jwt.secret", "default-fallback-secret")

def create_token(user_id):
    exp = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": str(user_id),
        "jti": f"{user_id}-{datetime.utcnow().isoformat()}",
        "exp": exp
    }
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)

def get_payload(token):
    try:
        return jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPUnauthorized(json_body={"error": "Token expired"})
    except InvalidTokenError:
        raise HTTPUnauthorized(json_body={"error": "Invalid token"})

def require_auth(view_func):
    def wrapper(request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise HTTPUnauthorized(json_body={'error': 'Authorization header missing or invalid'})

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
            request.user_id = int(payload['sub'])
        except ExpiredSignatureError:
            raise HTTPUnauthorized(json_body={'error': 'Token expired'})
        except InvalidTokenError:
            raise HTTPUnauthorized(json_body={'error': 'Invalid token'})

        return view_func(request)
    return wrapper
