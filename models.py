from sqlalchemy import String, Integer, Column, Text, Float, DateTime, ForeignKey, CheckConstraint, event, MetaData, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, sessionmaker

DATABASE = "postgresql://postgres:dobrysok@localhost/mydatabase"

metadata = MetaData()
engine = create_engine(
    DATABASE, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(metadata=metadata)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_tables():
    Base.metadata.create_all(bind=engine)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(Text)
    published_date = Column(String)
    cover_image = Column(String)
    book_file = Column(String)
    views = Column(Integer, default=0)
    downloads = Column(Integer, default=0)
    comments_on_book = Column(Integer, default=0)
    avg_rating = Column(Float, default=0)

    ratings = relationship("Rating", back_populates="book")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, index=True, primary_key=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String)
    email = Column(String)
    registration_date = Column(DateTime, default=datetime.now(timezone.utc))
    comments_by_user = Column(Integer)
    average_grade = Column(Float)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(250))
    text = Column(Text(1000))
    book_id = Column(Integer, ForeignKey('books.id'))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    book = relationship('Book', back_populates='comments')


class Download(Base):
    __tablename__ = 'downloads'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    downloaded_at = Column(DateTime, default=datetime.now(timezone.utc))
    ip_address = Column(String(45))


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    put_at = Column(DateTime, default=datetime.now(timezone.utc))
    comment = Column(Text(1000), nullable=True)
    avg_rating = Column(Float, default=0)
    user = relationship('User', back_populates='ratings')
    book = relationship('Book', back_populates='ratings')

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





