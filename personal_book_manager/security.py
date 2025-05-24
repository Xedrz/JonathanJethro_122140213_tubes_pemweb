from pyramid.httpexceptions import HTTPUnauthorized
import jwt

SECRET_KEY = 'rahasia-super-aman'

def authenticated_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPUnauthorized()

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPUnauthorized(json_body={"error": "Token expired"})
    except jwt.InvalidTokenError:
        raise HTTPUnauthorized(json_body={"error": "Invalid token"})
