from fastapi import FastAPI, Request
from models import Download
from sqlalchemy.orm import Session

db = Session()
app = FastAPI()


@app.get('/')
async def index():
    return 'Hello, world!'


@app.get('download/{book_id}')
async def download_book(book_id: int, request: Request):
    ip_address = request.client.host
    download = Download(book_id=book_id, ip_address=ip_address)
    db.add(download)
    db.commit()
    return {'message': f'Книга с ID {book_id} скачана пользователем с IP-адресом {ip_address}'}
