from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from crud import create_book
from database import Database
from models import SessionLocal, Author, Book
from schemas import BookCreate

app = FastAPI()
db = Database()


@app.get('/')
def read_root():
    return 'Hello, world!'


new_book = BookCreate(title='Харон', author='Mikel Diskein', published_date=2020)
with SessionLocal() as session:
    created_book = create_book(book_data=new_book, db=session)


@app.get("/books/", response_model=List[Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db())):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books









