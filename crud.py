from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book, Author


def create_book(title: str, author: Author, year: int, db: Session = SessionLocal()):
    book = Book(title=title, author=author, published_date=year)
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
