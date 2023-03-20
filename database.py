from sqlalchemy import create_engine, MetaData

from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE = "postgresql://postgres:dobrysok@localhost/my_db"

engine = create_engine(DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


Base = declarative_base(metadata=metadata)

