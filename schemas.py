from typing import Optional
from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    published_date: int
    description: Optional[str] = None