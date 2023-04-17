from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import DeclarativeBase
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

# This may have changed: https://docs.sqlalchemy.org/en/20/orm/session_basics.html#using-a-sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
