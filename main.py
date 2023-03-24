from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request

from auth.auth import hash_password, create_access_token, verify_password
from crud import create_book
from models import Author, Book, User
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
db = SessionLocal()


@app.post("/register")
def register(user: User):
    if db.exists(User.username == user.username):
        raise HTTPException(status_code=400, detail='Пользователь с таким именем уже существует')
    hashed_password = hash_password(user.password)
    new_user = db.create(User(**user.dict(), password=hashed_password))
    access_token = create_access_token(data={'sub': new_user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.post("/login")
def login(username: str, password: str):
    user = db.get(User, username=username)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Неверный пользователь или пароль')

    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/')
def read_root():
    return 'Hello, world!'


templates = Jinja2Templates(directory='templates')


@app.get("/books/", response_class=HTMLResponse)
def books(request: Request):
    books = db.query(Book).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books})


@app.get("/books/{book_id}", response_class=HTMLResponse)
def read_book(request: Request, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    return templates.TemplateResponse('book.html', {'request': request, 'book': book})



# created_book = create_book(
#     title='Спутник связи',
#     author=db.query(Author).get(1),
#     year=2020,
#     description='Мой второй и самый лучший рассказ',
#     db=db
# )