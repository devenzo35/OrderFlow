from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

if not os.getenv("CI"):
    from dotenv import load_dotenv
    load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("Database url not provided")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
