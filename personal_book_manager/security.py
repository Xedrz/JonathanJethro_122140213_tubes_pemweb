from pyramid.httpexceptions import HTTPUnauthorized
import jwt, datetime

SECRET_KEY = 'rahasia-super-aman'
ALGORITHM = 'HS256'

def create_token(user_id):
    jti = f"{user_id}-{datetime.datetime.utcnow().isoformat()}"
    payload = {
        "sub": user_id,
        "jti": jti,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=4)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_payload(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPUnauthorized(json_body={"error": "Token expired"})
    except jwt.InvalidTokenError:
        raise HTTPUnauthorized(json_body={"error": "Invalid token"})


