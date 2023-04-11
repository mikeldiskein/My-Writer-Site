from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from models import Author, Book, User
from database import SessionLocal
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
db = SessionLocal()
templates = Jinja2Templates(directory='templates')
WHITELIST = ['/main', '/registration', '/login', '/books']

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

# created_book = create_book(
#     title='Спутник связи',
#     author=db.query(Author).get(1),
#     year=2020,
#     description='Мой второй и самый лучший рассказ',
#     db=db
# )
