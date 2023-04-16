from sqlalchemy import String, Integer, Column, Text, Float, DateTime, ForeignKey, CheckConstraint, event, MetaData, \
    Table, Boolean
from passlib.context import CryptContext
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from database import SessionLocal, metadata


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

Base = declarative_base(metadata=metadata)
book_rating_association_table = Table('book_rating_association', Base.metadata,
                                      Column('book_id', Integer, ForeignKey('books.id')),
                                      Column('rating_id', Integer, ForeignKey('ratings.id')))


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')
    description = Column(Text)
    published_date = Column(Integer)
    cover_image = Column(String, nullable=True)
    book_file = Column(String, nullable=True)
    views = Column(Integer, default=0)
    downloads = relationship('Download', back_populates='book')
    avg_rating = Column(Float, default=0)
    comments = relationship("Comment", back_populates="book")
    ratings = relationship("Rating", secondary=book_rating_association_table, back_populates='books')


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, index=True, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    books = relationship('Book', back_populates='author')

    class Config:
        arbitrary_types_allowed = True


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    book_id = Column(Integer, ForeignKey('books.id'))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    book = relationship('Book', back_populates='comments')


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    registration_date = Column(DateTime, default=datetime.now())
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Download(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('Book', back_populates='downloads')
    downloaded_at = Column(DateTime, default=datetime.now(timezone.utc))


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    put_at = Column(DateTime, default=datetime.now(timezone.utc))
    comment = Column(Text, nullable=True)
    avg_rating = Column(Float, default=0)
    books = relationship("Book", secondary=book_rating_association_table, back_populates="ratings")

    @staticmethod
    def update_avg_rating(mapper, connection, target):
        book_id = target.book_id
        session = SessionLocal()
        ratings = session.query(Rating).filter_by(book_id=book_id).all()
        total = 0
        count = 0
        for rating in ratings:
            total += rating.value
            count += 1
        avg = total/count if count > 0 else 0
        session.query(Book).filter_by(id=book_id).update({'avg_rating': avg})
        session.commit()


event.listen(Rating, 'after_insert', Rating.update_avg_rating)
event.listen(Rating, 'after_update', Rating.update_avg_rating)




