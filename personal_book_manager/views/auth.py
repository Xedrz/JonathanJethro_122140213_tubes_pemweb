from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized
from ..models import User, RevokedToken
import bcrypt, jwt, datetime
from sqlalchemy import or_
from personal_book_manager.security import get_payload

SECRET_KEY = 'rahasia-super-aman'
ALGORITHM = 'HS256'

@view_config(route_name='register', renderer='json', request_method='POST')
def register(request):
    data = request.json_body
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

@view_config(route_name='login', renderer='json', request_method='POST')
def login(request):
    data = request.json_body
    identifier = data.get('username') or data.get('email')
    password = data.get('password')

    if not identifier or not password:
        return HTTPBadRequest(json_body={"error": "Email/Username and password required"})

    user = request.dbsession.query(User).filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()
    if not user or not user.verify_password(password):
        return HTTPUnauthorized(json_body={"error": "Invalid credentials"})

    jti = f"{user.id}-{datetime.datetime.utcnow().isoformat()}"
    payload = {
        "sub": user.id,
        "jti": jti,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}

@view_config(route_name='logout', request_method='POST', renderer='json')
def logout(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return HTTPBadRequest(json_body={"error": "Missing or invalid Authorization header"})

    token = auth_header.replace("Bearer ", "").strip()
    payload = get_payload(token)
    jti = payload.get("jti")

    if not jti:
        return HTTPBadRequest(json_body={"error": "Invalid token structure"})

    existing = request.dbsession.query(RevokedToken).filter_by(jti=jti).first()
    if existing:
        return HTTPBadRequest(json_body={"error": "Token already revoked"})

    revoked = RevokedToken(jti=jti)
    request.dbsession.add(revoked)
    return {"message": "Logged out successfully"}
