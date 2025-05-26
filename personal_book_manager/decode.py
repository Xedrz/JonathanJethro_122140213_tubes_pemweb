import jwt

SECRET = "dev-mode-super-secret-key-1234567890"
ALGORITHM = "HS256"

# Salin token hasil dari login (tanpa "Bearer ")
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwianRpIjoiMi0yMDI1LTA1LTI2VDA1OjQyOjE2LjI1MzI5OCIsImV4cCI6MTc0ODI0MTczNn0.QnjId8tFXhvFi_36NwL5ZWUe5XeeZbvqYdWeYlb7cKQ"

try:
    payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    print(" Token is valid.")
    print("Payload:", payload)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError as e:
    print("Invalid token:", str(e))
    
