import uuid
from typing import Optional

from fastapi_users import schemas

# def new_book(title: str, author: Author, year: int, description: str = 'Пока так',
#              cover_image: str = None, book_file: str = None):
#     return {
#         'title': title,
#         'author': author,
#         'published_date': year,
#         'description': description,
#         'cover_image': cover_image,
#         'book_file': book_file
#     }

# test_user = User(username='ppushkin500',
#                  first_name='Pavel',
#                  last_name='Pushkin',
#                  password='test_password')
# create_user(user=test_user, db=db)


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False




