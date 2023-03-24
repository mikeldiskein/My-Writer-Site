from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from auth.auth import hash_password, create_access_token, verify_password
from crud import create_book, create_user
from models import Author, Book, User
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from schemas import UserBase

app = FastAPI()
db = SessionLocal()

# test_user = User(username='ppushkin500',
#                  first_name='Pavel',
#                  last_name='Pushkin',
#                  password='test_password')
# create_user(user=test_user, db=db)


@app.get('/registration', response_class=HTMLResponse)
def registration(request: Request):
    return templates.TemplateResponse('registration.html',
                                      {'request': request})


@app.post("/register")
async def register(request: Request):
    form_data = await request.form()
    user = UserBase(
        username=form_data["username"],
        first_name=form_data["first_name"],
        last_name=form_data["last_name"],
        password=form_data["password"],
        email=form_data["email"]
    )
    new_user = create_user(user, db=db)
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
