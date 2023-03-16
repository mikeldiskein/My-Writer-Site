from sqlalchemy import create_engine, MetaData

from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE = "postgresql://postgres:dobrysok@localhost/mydatabase"

engine = create_engine(DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


Base = declarative_base(metadata=metadata)


class Database:
    def __init__(self):
        self.engine = engine

    def get_db(self):
        db = Session(bind=self.engine)
        try:
            yield db
        finally:
            db.close()
