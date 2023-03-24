import hashlib
import jwt
from datetime import datetime, timedelta
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    salt = hashlib.sha256(SECRET_KEY.encode()).hexdigest().encode()
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(),
                                          salt, 100000)
    return hashed_password.hex()


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = hashlib.sha256(SECRET_KEY.encode()).hexdigest().encode()
    password_hash = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt,
                                        10000)
    return password_hash == bytes.fromhex(hashed_password)

