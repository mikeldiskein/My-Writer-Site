from fastapi import FastAPI, Depends
from fastapi_users import fastapi_users, FastAPIUsers
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from models import Author, Book, User
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
db = SessionLocal()
templates = Jinja2Templates(directory='templates')


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route(user: User = Depends(current_user)):
    return f"Hello, anonym"


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


@app.route("/login", methods=["GET", "POST"])
def login(request: Request):
    if request.method == 'GET':
        return templates.TemplateResponse('login.html',
                                      {'request': request})
    elif request.method == 'POST':
        return templates.TemplateResponse('login.html',
                                          {'request': request})


@app.get("/books/", response_class=HTMLResponse)
def view_books(request: Request, response: Response):
    if "access_token" in request.cookies:
        response.delete_cookie("user_id")
        response.delete_cookie("access_token")
    books = db.query(Book).all()
    return templates.TemplateResponse('books.html', {'request': request, 'books': books})


@app.get("/books/{book_id}", response_class=HTMLResponse)
def read_book(request: Request, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    return templates.TemplateResponse('book.html', {'request': request, 'book': book})

