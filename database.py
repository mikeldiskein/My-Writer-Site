from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)