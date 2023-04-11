from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# load_dotenv()
#
# SECRET_KEY = os.getenv("SECRET_KEY")
#
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({'exp': expire})
#     encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm='HS256')
#     return encoded_jwt
#
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


