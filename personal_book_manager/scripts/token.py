import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Ganti dengan secret key yang valid

# Contoh membuat token baru (bukan decode)
def create_token():
    payload = {
        'user_id': 1,
        'exp': datetime.utcnow() + timedelta(days=1)  # Expire dalam 1 hari
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

if __name__ == "__main__":
    token = create_token()
    print("Token baru:", token)