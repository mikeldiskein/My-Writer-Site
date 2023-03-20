from fastapi import FastAPI, Depends
from starlette.requests import Request

from models import Author, Book
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
db = SessionLocal()


@app.get('/')
def read_root():
    return 'Hello, world!'


templates = Jinja2Templates(directory='templates')


@app.get("/books/", response_class=HTMLResponse)
def books(request: Request):
    books = db.query(Book).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books})
