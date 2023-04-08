from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from auth.auth import hash_password, create_access_token, verify_password
from crud import create_book, create_user
from models import Author, Book, User
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from schemas import UserBase

app = FastAPI()
db = SessionLocal()
templates = Jinja2Templates(directory='templates')

# test_user = User(username='ppushkin500',
#                  first_name='Pavel',
#                  last_name='Pushkin',
#                  password='test_password')
# create_user(user=test_user, db=db)


@app.route('/main', methods=['GET', 'POST'])
def main(request: Request):
    if request.method == 'GET':
        context = {"request": request, "cookie_name": 'user_id'}
        return templates.TemplateResponse('main.html',
                                          context=context)
    elif request.method == 'POST':
        return templates.TemplateResponse('main.html',
                                          {'request': request})


@app.get('/registration', response_class=HTMLResponse)
def registration(request: Request):
    return templates.TemplateResponse('registration.html',
                                      {'request': request})


@app.post("/register")
async def register(request: Request):
    form_data = await request.form()
    hashed_password = hash_password(password=form_data['password'])
    user = UserBase(
        username=form_data["username"],
        first_name=form_data["first_name"],
        last_name=form_data["last_name"],
        password=hashed_password,
        email=form_data["email"]
    )
    new_user = create_user(user, db=db)
    access_token = create_access_token(data={'sub': new_user.username})
    response = RedirectResponse(url="/login?method=POST")
    response.set_cookie(key="access_token", value=access_token)
    return response


@app.route("/login", methods=["GET", "POST"])
def login(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse('login.html',
                                      {'request': request})
    elif request.method == 'POST':
        return templates.TemplateResponse('login.html',
                                          {'request': request})


@app.post("/loginer")
async def login(request: Request):
    form_data = await request.form()
    username = form_data['username']
    password = form_data['password']
    user = db.query(User).filter(User.username == username).first()
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Неверный пользователь или пароль')
    # access_token = create_access_token(data={'sub': user.username})
    response = RedirectResponse(url="/main?method=POST", status_code=303)
    response.set_cookie('user_id', str(user.id))
    return response


@app.post("/logout")
async def logout(request: Request, response: Response):
    response.delete_cookie('user_id')
    return RedirectResponse(url="/main")


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
