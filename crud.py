from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book
from schemas import BookCreate


def create_book(book_data: BookCreate, db: Session = SessionLocal()):
    book = Book(**book_data.dict())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book