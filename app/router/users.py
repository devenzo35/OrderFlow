from fastapi import APIRouter
from app.db.database import SessionLocal

# from ..dependencies import get_token_header
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]
