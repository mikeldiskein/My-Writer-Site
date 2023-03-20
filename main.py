from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from crud import create_book
from models import Author, Book
from database import SessionLocal

app = FastAPI()
db = SessionLocal()


@app.get('/')
def read_root():
    return 'Hello, world!'


new_book = create_book(title='Харон', author=db.query(Author).get(1), year=2020, db=db)


# @app.get("/books/", response_model=List[Book])
# def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db())):
#     books = db.query(Book).offset(skip).limit(limit).all()
#     return books









