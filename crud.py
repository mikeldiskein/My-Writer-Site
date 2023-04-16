from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book, Author, User


def create_book(
        title: str,
        author: Author,
        year: int,
        description: str = 'Пока кукиш',
        db: Session = SessionLocal()):
    book = Book(title=title, author=author, published_date=year, description=description)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def create_author(first_name: str, last_name: str, db: Session = SessionLocal()):
    author = Author(first_name=first_name, last_name=last_name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_user(user: User, db: Session = SessionLocal):
    db_user = User(username=user.username,
                   password=user.password,
                   first_name=user.first_name,
                   last_name=user.last_name,
                   email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# created_book = create_book(
#     title='Спутник связи',
#     author=db.query(Author).get(1),
#     year=2020,
#     description='Мой второй и самый лучший рассказ',
#     db=db
# )