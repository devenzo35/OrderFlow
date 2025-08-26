from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

if not os.getenv("CI"):
    from dotenv import load_dotenv

    load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("Database url not provided")

asyncEngine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=asyncEngine
)


class Base(DeclarativeBase):
    pass
